from typing import List, Dict

from werkzeug.utils import cached_property

from kama_sdk.core.core.types import ConcernAttrMeta
from kama_sdk.model.concern import concern_attr_adapter
from kama_sdk.model.concern.concern import Concern
from kama_sdk.model.concern.concern_attr_adapter import ConcernAttrAdapter
from kama_sdk.model.concern.concern_set import ConcernSetAdapter


class ConcernTableAdapter(ConcernSetAdapter):

  @cached_property
  def concern_shell(self) -> Concern:
    shell = self.inflate_child(
      Concern,
      prop=CONCERN_SHELL_KEY,
      safely=True
    )
    return shell or Concern({})

  def concern_constructors(self) -> List[Dict]:
    return self.get_prop(CONCERN_CONSTRUCTORS_KEY) or []

  @cached_property
  def is_one_shot(self) -> bool:
    return True

  @cached_property
  def attr_adapters(self) -> List[ConcernAttrAdapter]:
    return self.inflate_children(
      ConcernAttrAdapter,
      prop=COLUMNS_KEY
    )

  @cached_property
  def column_definitions(self) -> List[ConcernAttrMeta]:
    return [a.as_meta() for a in self.attr_adapters]

  def concern_constructor_to_row(self, constructor:  Dict) -> Dict:
    concern_instance: Concern = self.concern_shell.clone().patch(constructor)
    row_data = {}
    for adapter_shell in self.attr_adapters:
      adapter = adapter_shell.clone().patch({
        concern_attr_adapter.CONCERN_KEY: concern_instance,
        concern_attr_adapter.SET_ID_KEY: self.id()
      })
      row_data[adapter.label] = adapter.compute_value()
    return row_data

  def one_shot_compute(self) -> List[Dict]:
    constructors = self.concern_constructors()
    rows = []
    for constructor in constructors:
      row = self.concern_constructor_to_row(constructor)
      rows.append(row)
    return rows

  @classmethod
  def view_type(cls) -> str:
    return 'table'


CONCERN_CONSTRUCTORS_KEY = 'concern_constructors'
COLUMNS_KEY = 'columns'
CONCERN_SHELL_KEY = "concern_shell"
