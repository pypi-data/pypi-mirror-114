from typing import List

from kama_sdk.core.core import utils
from kama_sdk.core.core.types import KDLoS
from kama_sdk.model.supplier.predicate.predicate import Predicate, OPERATOR_KEY


class MultiPredicate(Predicate):

  def sub_predicates_kods(self) -> List[KDLoS]:
    return self.config.get(PREDICATES_KEY, [])

  def get_operator(self):
    return self.get_attr(OPERATOR_KEY, backup='and')

  def resolve(self) -> bool:
    operator = self.get_operator()
    for sub_pred_kod in self.sub_predicates_kods():
      eval_or_literal = self.get_attr_value(sub_pred_kod)
      resolved_to_true = utils.any2bool(eval_or_literal)

      if operator == 'or':
        if resolved_to_true:
          return True
      elif operator == 'and':
        if not resolved_to_true:
          return False
      else:
        print(f"[kama_sdk::multi_pred] illegal operator {operator}")
        return False
    return operator == 'and'


PREDICATES_KEY = 'predicates'
