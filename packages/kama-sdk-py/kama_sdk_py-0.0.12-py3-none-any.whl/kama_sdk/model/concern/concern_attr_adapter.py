from typing import Optional, Any

from werkzeug.utils import cached_property

from kama_sdk.core.core.types import ConcernAttrMeta
from kama_sdk.core.core.utils import perr
from kama_sdk.model.base.model import Model


class ConcernAttrAdapter(Model):

  def compute(self):
    pass

  @cached_property
  def label(self) -> str:
    return self.get_prop(LABEL_KEY) or self.id()

  @cached_property
  def value_info(self) -> str:
    return self.get_prop(VALUE_INFO_KEY)

  def compute_value(self) -> Optional[Any]:
    # print(f"its me {self.id()}")
    # print(self.config)
    # print(self.get_prop('concern'))

    if VALUE_KEY in self.config.keys():
      return self.resolve_prop(VALUE_KEY, depth=100)
    elif LABEL_KEY in self.config.keys():
      synth_name = f"get::props {CONCERN_KEY}=>{self.label}"
      return self.resolve_prop_value(synth_name, depth=100)
    else:
      perr(self, "given neither label or value!")
      return None

  def as_meta(self) -> ConcernAttrMeta:
    return ConcernAttrMeta(
      title=self.title,
      label=self.label
    )


VALUE_KEY = "value"
LABEL_KEY = "label"
CONCERN_KEY = 'concern'
SET_ID_KEY = 'set_id'
VALUE_INFO_KEY = 'value_info'
