from typing import Any, Dict, Union, Optional, List

import jq

from kama_sdk.core.core import utils
from kama_sdk.core.core.utils import listlike, pwar, perr
from kama_sdk.model.base.model import Model
from kama_sdk.model.supplier.base.expr2config import expr2config


class Supplier(Model):

  def get_output_format(self):
    return self.get_attr(OUTPUT_FMT_KEY, lookback=0)

  def get_source_data(self) -> Optional[any]:
    return self.get_attr(SRC_DATA_KEY, lookback=0)

  def get_serializer_type(self) -> str:
    return self.get_attr(SERIALIZER_KEY, backup='jq', lookback=0)

  def should_treat_as_list(self) -> bool:
    value = self.get_attr(IS_MANY_KEY, lookback=0)
    return value

  def get_attrs_to_print(self) -> List[str]:
    return self.config.get(PRINT_DEBUG_KEY, [])

  def print_debug(self):
    attr_keys = self.get_attrs_to_print()
    for attr_key in attr_keys:
      value = self.get_attr(attr_key)
      pwar(self, f"[{self.get_id()}] {attr_key} = {value}")

  def resolve(self) -> Any:
    self.print_debug()
    computed_value = self._compute()
    serializer_type = self.get_serializer_type()

    if serializer_type == SER_OBJ:
      serialized_value = self.serialize_computed_value_legacy(computed_value)
    elif serializer_type == SER_JQ:
      serialized_value = self.jq_serialize(computed_value)
    elif serializer_type == SER_MODEL:
      serialized_value = self.attr_serialize(computed_value)
    elif serializer_type == SER_IDENTITY:
      serialized_value = computed_value
    else:
      pt1 = f"treating unknown ser {self.get_serializer_type}"
      print(f"[kama_sdk:supplier] {pt1} as {SER_IDENTITY}")
      serialized_value = computed_value

    return serialized_value

  def attr_serialize(self, computed_value) -> Any:
    if isinstance(computed_value, Model):
      key = self.get_output_format()
      return computed_value.get_attr(key)
    else:
      exp = f"{computed_value} as a model; its is a {type(computed_value)}"
      perr(self, f"Cannot access {exp}. returning None")
      return None

  def jq_serialize(self, value: Any) -> Any:
    if self.get_output_format() and value is not None:
      try:
        expression = jq.compile(self.get_output_format())
        if self.should_treat_as_list():
          return expression.input(value).all()
        else:
          return expression.input(value).first()
      except Exception as e:
        print(f"[kama_sdk] danger JQ compile failed: {str(e)}")
        return None
    else:
      return value

  def serialize_computed_value_legacy(self, computed_value) -> Any:
    treat_as_list = self.should_treat_as_list()

    if treat_as_list in [None, 'auto']:
      treat_as_list = listlike(computed_value)

    if treat_as_list and not self.get_output_format() == '__count__':
      if listlike(computed_value):
        return [self.serialize_item(item) for item in computed_value]
      else:
        return [self.serialize_item(computed_value)]
    else:
      if not listlike(computed_value) or self.get_output_format() == '__count__':
        return self.serialize_item(computed_value)
      else:
        item = computed_value[0] if len(computed_value) > 0 else None
        return self.serialize_item(item) if item else None

  def _compute(self) -> Any:
    return self.get_source_data()

  def serialize_item(self, item: Any) -> Union[Dict, str]:
    fmt = self.get_output_format()
    if not fmt or type(fmt) == str:
      return self.serialize_item_prop(item, fmt)
    elif type(fmt) == dict:
      return self.serialize_dict_item(item)
    else:
      return ''

  def serialize_dict_item(self, item):
    fmt: Dict = self.get_output_format()
    serialized = {}
    for key, value in list(fmt.items()):
      serialized[key] = self.serialize_item_prop(item, value)
    return serialized

  # noinspection PyBroadException
  @staticmethod
  def serialize_item_prop(item: Any, prop_name: Optional[str]) -> Optional[Any]:
    if prop_name:
      if prop_name == '__identity__':
        return item
      elif prop_name == '__count__':
        try:
          return len(item)
        except:
          return 0
      else:
        try:
          return utils.pluck_or_getattr_deep(item, prop_name)
        except:
          return None
    else:
      return item

  @classmethod
  def expr2kod(cls, expr: str) -> Dict:
    parts = expr.split(" ")
    identity_expr = parts[0]

    if identity_expr == 'props':
      from kama_sdk.model.supplier.base.props_supplier import PropsSupplier
      return {
        'kind': PropsSupplier.__name__,
        'output': " ".join(parts[1:])
      }
    elif identity_expr == 'ns':
      return {'inherit': 'sdk.supplier.config.ns'}
    else:
      result = expr2config(identity_expr)
      return result


SER_JQ = 'jq'
SER_OBJ = 'legacy'
SER_IDENTITY = 'identity'
SER_MODEL = 'model'

IS_MANY_KEY = 'many'
OUTPUT_FMT_KEY = 'output'
ON_RAISE_KEY = 'on_error'
SRC_DATA_KEY = 'source'
SERIALIZER_KEY = 'serializer'
PRINT_DEBUG_KEY = 'print_debug'
