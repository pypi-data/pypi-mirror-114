from __future__ import annotations
from functools import lru_cache
from typing import Optional, List

from werkzeug.utils import cached_property

from kama_sdk.core.core import config_man as cman_module, utils
from kama_sdk.core.core.config_man import config_man
from kama_sdk.core.core import config_man as config_man_mod
from kama_sdk.model.base import model
from kama_sdk.model.base.model_decorators import model_attr
from kama_sdk.model.supplier.predicate.predicate import Predicate
from kama_sdk.model.variable.generic_variable import GenericVariable
from kama_sdk.model.variable.variable_category import VariableCategory


class ManifestVariable(GenericVariable):

  def get_level(self) -> str:
    return self.get_attr(OWNER_KEY, backup=config_man_mod.user_vars_key)

  def flat_key(self) -> str:
    explicit = self.get_attr(VARIABLE_KEY_KEY, lookback=False)
    return explicit or self.get_id()

  @model_attr
  def get_default_value(self) -> str:
    return config_man.read_var(self.flat_key(), **{
      cman_module.space_kwarg: self.get_config_space()
    })

  @model_attr
  def get_category(self) -> VariableCategory:
    return self.inflate_child(
      VariableCategory,
      prop=CATEGORY_KEY,
      safely=True
    )

  def is_user_writable(self) -> bool:
    return self.get_level() == config_man_mod.user_vars_key

  def is_safe_to_set(self) -> bool:
    return self.is_user_writable()

  def effects_felt(self) -> List[str]:
    from kama_sdk.model.variable.manifest_variable_dependency \
      import ManifestVariableDependency
    in_deps = ManifestVariableDependency.for_variable('in', self)
    return ManifestVariableDependency.effects(in_deps, [True])

  def is_read_blocked(self) -> bool:
    from kama_sdk.model.variable import manifest_variable_dependency
    effects = self.effects_felt()
    return manifest_variable_dependency.prevents_read in effects

  @lru_cache
  def health_predicates(self) -> List[Predicate]:
    return self.inflate_children(
      Predicate,
      prop=CORRECTNESS_PREDICATES_KEY
    )

  @lru_cache
  def problems(self) -> List[Predicate]:
    failed_predicates = []
    for predicate in self.health_predicates():
      if not predicate.resolve():
        failed_predicates.append(predicate)
    return failed_predicates

  def has_problems(self) -> bool:
    return len(self.problems()) > 0

  def is_correct(self) -> bool:
    return not self.has_problems()

  @model_attr
  def get_current_value(self, **kwargs) -> Optional[str]:
    result = config_man.read_var(
      self.flat_key(),
      **{
        cman_module.space_kwarg: self.get_config_space(),
        **kwargs
      }
    )
    return result

  def current_or_default_value(self):
    return self.get_current_value() or self.get_default_value()

  def is_currently_valid(self) -> bool:
    variables = config_man.manifest_variables(**{
      cman_module.space_kwarg: self.get_config_space()
    })
    is_defined = self.flat_key() in utils.deep2flat(variables).keys()
    crt_val = utils.deep_get2(variables, self.flat_key())
    return self.validate(crt_val)['met'] if is_defined else True

  # noinspection PyBroadException
  @classmethod
  def find_or_synthesize(cls, flat_key: str, space_id: str) -> ManifestVariable:
    pool = cls.inflate_all(selector=dict(space=space_id))
    finder = lambda m: m.flat_key() == flat_key
    if inst := next(filter(finder, pool), None):
      return inst
    else:
      return cls.synthesize_var_model(flat_key, space_id)

  @staticmethod
  def synthesize_var_model(key: str, space_id: str):
    return ManifestVariable.inflate({
      'id': key,
      OWNER_KEY: config_man_mod.user_vars_key,
      model.SPACE_KEY: space_id,
      model.TITLE_KEY: '',
      model.INFO_KEY: ''
    })


OWNER_KEY = 'owner'
VARIABLE_KEY_KEY = 'key'
CATEGORY_KEY = 'category'
CORRECTNESS_PREDICATES_KEY = 'health_predicates'
