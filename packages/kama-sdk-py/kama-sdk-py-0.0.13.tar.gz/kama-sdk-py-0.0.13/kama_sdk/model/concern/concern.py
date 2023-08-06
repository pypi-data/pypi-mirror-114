from typing import List, Dict

from kama_sdk.model.action.base.action import Action
from kama_sdk.model.base.model import Model
from kama_sdk.model.operation.operation import Operation
from kama_sdk.model.supplier.base.supplier import Supplier


class Concern(Supplier):

  attr_values: Dict

  def subject(self):
    pass

  def actions(self) -> List[Action]:
    pass

  def operations(self) -> List[Operation]:
    pass


res_constructor_supplier = \
  "sdk.supplier.concern.resource_selector_to_constructors"

ATTR_METAS_KEY = 'attr_metas'
SEED_KEY = 'seed'
