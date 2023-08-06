from typing import List, Dict

from werkzeug.utils import cached_property

from kama_sdk.core.core.types import Reconstructor
from kama_sdk.model.concern import concern_set
from kama_sdk.model.concern.concern_view_adapter import ConcernViewAdapter
from kama_sdk.model.concern.concern_card_adapter import ConcernCardAdapter
from kama_sdk.model.concern.concern_set import ConcernSetAdapter


class ConcernGridAdapter(ConcernSetAdapter):

  @cached_property
  def is_one_shot(self) -> bool:
    return self.get_prop(concern_set.ONE_SHOT_KEY, False)

  @classmethod
  def view_type(cls) -> str:
    return 'grid'

  def compute_all_data(self) -> List[Dict]:
    seeds = self.compute_concern_seeds()
    data: List[Dict] = []
    for seed in seeds:
      adapter: ConcernCardAdapter = ConcernCardAdapter.reconstruct(seed)
      data.append(adapter.compute())
    return data

  def one_shot_compute(self) -> List[Dict]:
    if self.is_one_shot:
      return self.compute_all_data()
    else:
      return self.compute_concern_seeds()
