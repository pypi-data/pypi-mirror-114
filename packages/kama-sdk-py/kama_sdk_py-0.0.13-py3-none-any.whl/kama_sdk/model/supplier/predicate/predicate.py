from typing import Dict, Any, Optional, TypeVar

from kama_sdk.core.core import utils
from kama_sdk.core.core.comparison import standard_comparison, list_like_comparison
from kama_sdk.model.base.model_decorators import model_attr
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

  def get_serializer_type(self) -> str:
    return supplier.SER_IDENTITY

  def get_many_policy(self) -> str:
    return self.get_attr(ON_MANY_KEY, lookback=0)

  @model_attr
  def get_challenge(self) -> Any:
    return self.get_attr(CHALLENGE_KEY, lookback=0)

  @model_attr
  def get_check_against(self) -> Optional[Any]:
    return self.get_attr(CHECK_AGAINST_KEY, lookback=0)

  def get_operator(self) -> str:
    return self.get_attr(OPERATOR_KEY, backup='==', lookback=0)

  def should_negate(self) -> bool:
    value = self.get_attr(NEGATE_KEY, lookback=False)
    return utils.any2bool(value)

  def is_optimist(self) -> bool:
    return self.get_attr(IS_OPTIMISTIC_KEY, backup=False)

  def is_pessimist(self) -> bool:
    return not self.is_optimist()

  def tone(self) -> str:
    return self.get_attr(TONE_KEY, backup='error')

  def reason(self) -> str:
    return self.get_attr(REASON_KEY, backup='')

  def _compute(self) -> bool:
    self.print_debug()

    challenge = self.get_challenge()
    check_against = self.get_check_against()

    if self.should_return_true_early():
      return True

    if self.should_return_false_early():
      return False

    return self.perform_comparison(
      self.get_operator(),
      challenge,
      check_against,
      self.get_many_policy()
    )

  def perform_comparison(self, operator, challenge, check_against, on_many):
    return perform_comparison(operator, challenge, check_against, on_many)

  def should_return_true_early(self):
    return self.get_attr(AUTO_TRUE_IF, lookback=0)

  def should_return_false_early(self):
    return self.get_attr(AUTO_FALSE_IF, lookback=0)

  def resolve(self) -> bool:
    result = self._compute()
    if self.should_negate():
      return utils.any2bool(not result)
    else:
      return result

  def error_extras(self) -> Dict:
    return self.get_attr(ERROR_EXTRAS_KEY, depth=100) or {}

  def explanation(self) -> str:
    return self.get_attr(EXPLAIN_KEY, backup='')

  def debug_bundle(self):
    keys = [
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
EXPLAIN_KEY = 'explain'
AUTO_TRUE_IF = 'early_true_if'
AUTO_FALSE_IF = 'early_false_if'
