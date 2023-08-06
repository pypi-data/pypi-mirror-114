from typing import List

from werkzeug.utils import cached_property

from kama_sdk.model.base.model import Model
from kama_sdk.model.operation.field import Field


class FieldSet(Model):

  @cached_property
  def fields(self) -> List[Field]:
    return self.inflate_children(
      Field,
      prop=FIELDS_KEY
    )

  def button_descriptors(self) -> List:
    return self.resolve_prop(
      'buttons',
      lookback=False,
      depth=100,
      backup=[]
    )


FIELDS_KEY = 'fields'
ACTION_KEY = 'action'
