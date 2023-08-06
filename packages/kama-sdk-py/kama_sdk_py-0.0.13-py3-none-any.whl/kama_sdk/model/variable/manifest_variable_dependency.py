from __future__ import annotations
from functools import lru_cache
from typing import List, Tuple

from kama_sdk.core.core import utils
from kama_sdk.model.base import model
from kama_sdk.model.base.model import Model
from kama_sdk.model.base.model_decorators import model_attr
from kama_sdk.model.variable.manifest_variable import ManifestVariable

FROM_SINGLE_KEY = 'from_variable'
TO_SINGLE_KEY = 'to_variable'


class ManifestVariableDependencyInstance(Model):

  @lru_cache
  def is_active(self) -> bool:
    result = self.get_attr(IS_ACTIVE_KEY, depth=0)
    return utils.any2bool(result)

  @lru_cache
  def effect(self) -> str:
    return self.get_attr(EFFECT_KEY) or prevents_read

  @model_attr(key=FROM_SINGLE_KEY)
  def from_variable(self) -> ManifestVariable:
    return self.config.get(FROM_SINGLE_KEY)

  @model_attr(key=TO_SINGLE_KEY)
  def to_variable(self) -> ManifestVariable:
    return self.config.get(TO_SINGLE_KEY)


MVar = ManifestVariable
DepInst = ManifestVariableDependencyInstance


class ManifestVariableDependency(Model):

  @classmethod
  def for_variable(cls, direction: str, variable: MVar) -> List[VarDep]:
    all_dependencies = ManifestVariableDependency.inflate_all(**{
      model.query_kw: {model.SPACE_KEY: variable.get_space()}
    })

    variable_dependencies = []

    for dependency in all_dependencies:
      if direction == 'out':
        other_var_ids = [v.get_id() for v in dependency.from_variables()]
      else:
        other_var_ids = [v.get_id() for v in dependency.to_variables()]
      if variable.flat_key() in other_var_ids:
        variable_dependencies.append(dependency)

    return variable_dependencies

  @staticmethod
  def effects(deps: List[VarDep], active: List[bool] = None) -> List[str]:
    nested_list = []
    for dependency in deps:
      for instance in dependency.one_to_one_instances():
        if active is None or active == [True, False]:
          nested_list.append(instance.effect())
        elif instance.is_active() in active:
          nested_list.append(instance.effect())
    return list(set(nested_list))

  @lru_cache
  def one_to_one_instances(self) -> List[DepInst]:
    results = []
    for from_variable in self.from_variables():
      for to_variable in self.to_variables():
        dependency_instance = DepInst.inflate({
          model.TITLE_KEY: self.get_title(),
          model.INFO_KEY: self.get_info(),
          FROM_SINGLE_KEY: from_variable,
          TO_SINGLE_KEY: to_variable,
          IS_ACTIVE_KEY: self.config.get(IS_ACTIVE_KEY)
        })
        dependency_instance.set_parent(self)
        results.append(dependency_instance)
    return results

  @lru_cache
  def from_variables(self) -> List[ManifestVariable]:
    from kama_sdk.model.variable.manifest_variable import ManifestVariable
    return self.inflate_children(ManifestVariable, prop=FROM_KEY)

  @lru_cache
  def to_variables(self) -> List[ManifestVariable]:
    from kama_sdk.model.variable.manifest_variable import ManifestVariable
    return self.inflate_children(ManifestVariable, prop=TO_KEY)


VarDep = ManifestVariableDependency

FROM_KEY = 'from'
TO_KEY = 'to'
EFFECT_KEY = 'effect'
IS_ACTIVE_KEY = 'active'

prevents_read = 'prevents_read'
compels_defined = 'compels_defined'
