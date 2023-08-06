from typing import Dict

from kama_sdk.model.concern.concern import Concern
from kama_sdk.model.concern.concern_view_adapter import ConcernViewAdapter
from kama_sdk.model.supplier.base.provider import Provider


class ConcernCardAdapter(ConcernViewAdapter):

  def compute(self) -> Dict:
    return self.get_attr('spec', depth=100)


class PluginsCardAdapter(ConcernCardAdapter):

  def compute(self) -> Dict:
    return {
      'type': 'Block',
      'elements': [
        {
          'type': 'Section',
          'width': 2,
          'elements': [
          ]
        }
      ]
    }

  def compute_prom_header(self):
    concern = Concern.inflate("nmachine.prom.concern.card")
    view = Provider.inflate("nmachine.prom.view.prom-header", patches={
      'concern': concern
    })
