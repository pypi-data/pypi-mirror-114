from typing import Dict, Any, Optional, TypeVar

from werkzeug.utils import cached_property

from kama_sdk.core.core import utils
from kama_sdk.core.core.comparison import standard_comparison, list_like_comparison
from kama_sdk.model.supplier.base import supplier
from kama_sdk.model.supplier.base.supplier import Supplier

T = TypeVar('T', bound='Predicate')

class Predicate(Supplier):

  @classmethod
  def inflate_with_literal(cls, expr: str, **kwargs) -> Optional[T]:
    operator, rest = expr.split("?")
    if '|' in rest:
      parts = rest.split('|')
      other_params = {
        CHECK_AGAINST_KEY: parts[1],
        CHALLENGE_KEY: parts[0]
      }
    else:
      other_params = {CHECK_AGAINST_KEY: rest}

    return cls.inflate_with_config({
      OPERATOR_KEY: operator,
      **other_params
    }, **kwargs)

  @cached_property
  def serializer_type(self) -> str:
    return supplier.SER_IDENTITY

  def many_policy(self) -> str:
    return self.resolve_prop(ON_MANY_KEY, lookback=0)

  def get_challenge(self) -> Any:
    return self.resolve_prop(CHALLENGE_KEY, lookback=0)

  def get_check_against(self) -> Optional[Any]:
    return self.resolve_prop(CHECK_AGAINST_KEY, lookback=0)

  def get_operator(self) -> str:
    return self.resolve_prop(OPERATOR_KEY, backup='==', lookback=0)

  def should_negate(self) -> bool:
    value = self.resolve_prop(NEGATE_KEY, lookback=False)
    return utils.any2bool(value)

  def is_optimist(self) -> bool:
    return self.get_prop(IS_OPTIMISTIC_KEY, False)

  def is_pessimist(self) -> bool:
    return not self.is_optimist()

  def tone(self) -> str:
    return self.get_prop(TONE_KEY, 'error')

  def reason(self) -> str:
    return self.get_prop(REASON_KEY, '')

  def _compute(self) -> bool:
    self.print_debug()
    challenge = self.get_challenge()
    check_against = self.get_check_against()

    self.patch({
      RESOLVED_CHALLENGE_KEY: challenge,
      RESOLVED_CHECK_AGAINST_KEY: check_against
    }, invalidate=False)

    if self.should_return_true_early():
      return True

    if self.should_return_false_early():
      return False

    return self.perform_comparison(
      self.get_operator(),
      challenge,
      check_against,
      self.many_policy()
    )

  def perform_comparison(self, operator, challenge, check_against, on_many):
    return perform_comparison(operator, challenge, check_against, on_many)

  def should_return_true_early(self):
    return self.resolve_prop(AUTO_TRUE_IF, lookback=0)

  def should_return_false_early(self):
    return self.resolve_prop(AUTO_FALSE_IF, lookback=0)

  def resolve(self) -> bool:
    result = self._compute()
    if self.should_negate():
      return utils.any2bool(not result)
    else:
      return result

  def error_extras(self) -> Dict:
    return self.resolve_prop(ERROR_EXTRAS_KEY, depth=100) or {}

  def explanation(self) -> str:
    return self.get_prop(EXPLAIN_KEY, '')

  def debug_bundle(self):
    keys = [
      RESOLVED_CHALLENGE_KEY,
      RESOLVED_CHECK_AGAINST_KEY,
      CHALLENGE_KEY,
      CHECK_AGAINST_KEY,
      OPERATOR_KEY,
      IS_OPTIMISTIC_KEY,
      ON_MANY_KEY
    ]
    return {k: v for k, v in self.config.items() if k in keys}


def perform_comparison(operator: str, challenge, against, on_many) -> bool:
  if utils.listlike(challenge) and on_many:
    return list_like_comparison(operator, challenge, against, on_many)
  else:
    return standard_comparison(operator, challenge, against)


CHALLENGE_KEY = 'challenge'
OPERATOR_KEY = 'operator'
CHECK_AGAINST_KEY = 'check_against'
ON_MANY_KEY = 'many_policy'
TONE_KEY = 'tone'
REASON_KEY = 'reason'
NEGATE_KEY = 'negate'
IS_OPTIMISTIC_KEY = 'optimistic'
TAGS = 'tags'
ERROR_EXTRAS_KEY = 'error_extras'
RESOLVED_CHALLENGE_KEY = 'resolved_challenge'
RESOLVED_CHECK_AGAINST_KEY = 'resolved_check_against'
EXPLAIN_KEY = 'explain'
AUTO_TRUE_IF = 'early_true_if'
AUTO_FALSE_IF = 'early_false_if'
