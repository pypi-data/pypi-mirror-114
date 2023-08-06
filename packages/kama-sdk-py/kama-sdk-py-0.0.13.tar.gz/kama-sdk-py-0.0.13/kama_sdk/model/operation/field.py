from typing import List, TypeVar, Dict

from kama_sdk.core.core import consts
from kama_sdk.core.core.utils import any2bool
from kama_sdk.model.base.model import Model, INFO_KEY, TITLE_KEY
from kama_sdk.model.base.model_decorators import model_attr
from kama_sdk.model.variable import generic_variable
from kama_sdk.model.variable.generic_variable import GenericVariable

T = TypeVar('T', bound='Field')

class Field(Model):

  @model_attr
  def get_variable(self) -> GenericVariable:
    """
    Inflate child variable using 'variable' KoD. If not present,
    construct synthetic GenericVariable using own config.
    @return: GenericVariable instance
    """
    return self.inflate_child(
      GenericVariable,
      prop=VARIABLE_KEY,
      safely=True
    ) or self.inflate_child(
      GenericVariable,
      kod=self.variable_bound_config_subset()
    )

  def get_title(self) -> str:
    if value := self.get_attr(TITLE_KEY, lookback=0):
      return value
    else:
      return self.get_variable().get_title()

  def get_info(self) -> str:
    if value := self.get_attr(INFO_KEY, lookback=0):
      return value
    else:
      return self.get_variable().get_info()

  @model_attr
  def get_bucket_type(self):
    return self.get_attr(TARGET_KEY, backup=consts.DEFAULT_TARGET)

  def variable_bound_config_subset(self):
    relevant = generic_variable.COPYABLE_KEYS
    config = {k: self.config.get(k) for k in relevant}
    return config

  def get_visibility(self) -> bool:
    result = self.get_attr(VISIBLE_KEY, backup=True)
    return any2bool(result)

  def serialize_options(self) -> List[Dict]:
    return self.get_variable().input_model.serialize_options()

  def is_manifest_bound(self) -> bool:
    return self.is_chart_var() or self.is_inline_chart_var()

  def is_inline_chart_var(self) -> bool:
    return self.get_bucket_type() == consts.TARGET_INLIN

  def is_chart_var(self) -> bool:
    return self.get_bucket_type() == consts.TARGET_STANDARD

  def is_state_var(self) -> bool:
    return self.get_bucket_type() == consts.TARGET_STATE


TARGET_KEY = 'target'
VARIABLE_KEY = 'variable'
VISIBLE_KEY = 'visible'
