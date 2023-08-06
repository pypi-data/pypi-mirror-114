from typing import Dict, List, Optional

from kama_sdk.core.core import config_man as cman_module, utils
from kama_sdk.core.core.config_man import user_vars_key, vndr_inj_vars_key, def_vars_key, config_man
from kama_sdk.model.input import input_serializer
from kama_sdk.model.variable import manifest_variable_dependency as mfd_module
from kama_sdk.model.variable.manifest_variable import ManifestVariable
from kama_sdk.model.variable.manifest_variable_dependency import ManifestVariableDependencyInstance, \
  ManifestVariableDependency
from kama_sdk.model.variable.variable_category import VariableCategory
from kama_sdk.serializers import common_serializers


def serialize_category(category: VariableCategory) -> Optional[Dict]:
  if category:
    return {
      **common_serializers.ser_meta(category),
      'graphic_type': category.graphic_type,
      'graphic': category.graphic
    }
  else:
    return None


def standard(variable: ManifestVariable, **kwargs):
  return dict(
    id=variable.flat_key(),
    title=variable.get_title(),
    is_user_writable=variable.is_user_writable(),
    info=variable.get_info(),
    category=serialize_category(variable.get_category()),
    value=variable.get_current_value(**kwargs),
    definitions=ser_definitions(variable),
    is_valid=variable.is_currently_valid(),
    config_space=variable.get_config_space()
  )


MVDI = ManifestVariableDependencyInstance
MVD = ManifestVariableDependency


def ser_definitions(variable: ManifestVariable) -> List[Dict]:
  ownership_levels = [user_vars_key, vndr_inj_vars_key, def_vars_key]

  def level2bundle(index: int) -> Dict:
    level_name = ownership_levels[index]
    source: Dict = config_man.read_typed_entry(level_name, **{
      cman_module.space_kwarg: variable.get_config_space()
    })

    flat_source = utils.deep2flat(source)
    is_present = variable.flat_key() in flat_source.keys()
    value = flat_source.get(variable.flat_key())

    return {
      'level_name': level_name,
      'level_number': index,
      'value': value,
      'is_present': is_present
    }

  return list(map(level2bundle, range(len(ownership_levels))))


def ser_dep_inst(dep_inst: MVDI, other_var: ManifestVariable) -> Dict:
  info = dep_inst.get_title() or dep_inst.get_info()
  return {
    'title': info,
    'info': info,
    'other_variable': {
      'id': other_var.get_id(),
      'space': other_var.get_space()
    },
    'effect': dep_inst.effect(),
    'is_active': dep_inst.is_active()
  }


def ser_dependency(direction: str, dep: MVD) -> List[Dict]:
  instances = dep.one_to_one_instances()

  results = []

  for instance in instances:
    if direction == 'in':
      other_var = instance.from_variable()
    else:
      other_var = instance.to_variable()

    results.append(ser_dep_inst(instance, other_var))

  is_duplicate = lambda b: utils.deep_get2(b, 'other_variable.id')
  return list(utils.unique(results, key=is_duplicate))


def ser_dependencies(direction, dependencies: List[MVD]) -> List[Dict]:
  nested = [ser_dependency(direction, d) for d in dependencies]
  return utils.flatten(nested)


def has_active_read_prevention(dicts: List[Dict]):
  def predicate(ser: Dict) -> bool:
    is_read_prevent = ser.get('effect') == mfd_module.prevents_read
    is_active = ser.get('is_active')
    return is_read_prevent and is_active
  return next(filter(predicate, dicts), None) is not None


def ser_predicates(variable: ManifestVariable) -> Dict:
  ser = common_serializers.ser_meta
  return {
    'health_predicates': list(map(ser, variable.health_predicates()))
  }


def full(variable: ManifestVariable) -> Dict:
  out_deps = ManifestVariableDependency.for_variable('out', variable)
  in_deps = ManifestVariableDependency.for_variable('in', variable)

  serd_out_deps = ser_dependencies('out', out_deps)
  serd_in_deps = ser_dependencies('in', in_deps)

  return {
    **standard(variable),
    **input_serializer.in_variable(variable.input_model),
    **ser_predicates(variable),
    'incoming_dependencies': serd_in_deps,
    'outgoing_dependencies': serd_out_deps,
    'is_preventing_read': has_active_read_prevention(serd_out_deps),
    'is_read_blocked': has_active_read_prevention(serd_in_deps)
  }
