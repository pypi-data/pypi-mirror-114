from functools import lru_cache
from typing import Optional, Dict, List

from kama_sdk.core.core.structured_search import is_query_match
from kama_sdk.core.core.types import ErrCapture
from kama_sdk.model.base.model import Model


class ActionErrorRemediationOption(Model):

  @lru_cache
  def matcher(self) -> Dict:
    return self.resolve_prop(PRED_MATCHER_KEY, depth=0)

  def matches_error_capture(self, error_capture: ErrCapture) -> bool:
    if self.matcher():
      return is_query_match(self.matcher(), error_capture)
    else:
      return False

  @lru_cache
  def button_action_desc(self) -> Optional[Dict]:
    return self.resolve_prop(BUTTON_KEY, lookback=False, depth=100)

  @classmethod
  def matching_error_capture(cls, err_capture: ErrCapture):
    self_instances: List[cls] = cls.inflate_all()
    decider = lambda inst: inst.matches_error_capture(err_capture)
    return list(filter(decider, self_instances))

  def serialize_for_client(self) -> Dict:
    return {
      'title': self.title,
      'info': self.info,
      'button_action': self.button_action_desc()
    }


BUTTON_KEY = 'button_action'
PRED_MATCHER_KEY = 'match'
