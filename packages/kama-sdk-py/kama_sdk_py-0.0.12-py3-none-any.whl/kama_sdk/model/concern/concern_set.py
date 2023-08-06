from typing import Dict, List

from werkzeug.utils import cached_property

from kama_sdk.model.base.model import Model


class ConcernSetAdapter(Model):

  @cached_property
  def is_one_shot(self) -> bool:
    return self.get_prop(ONE_SHOT_KEY, True)

  def compute_concern_seeds(self):
    return self.get_prop(CONCERN_SEEDS_KEY) or []

  def one_shot_compute(self) -> List[Dict]:
    return []

  @classmethod
  def view_type(cls) -> str:
    return ''


ONE_SHOT_KEY = 'one_shot'
CONCERN_SEEDS_KEY = 'concern_seeds'
