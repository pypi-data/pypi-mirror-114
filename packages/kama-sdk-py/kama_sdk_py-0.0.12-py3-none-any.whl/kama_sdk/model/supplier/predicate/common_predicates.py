from kama_sdk.model.supplier.predicate.predicate import Predicate


class TruePredicate(Predicate):

  def id(self) -> str:
    return 'sdk.predicate.true'

  def perform_comparison(self, operator, challenge, check_against, on_many):
    return True


class FalsePredicate(Predicate):

  def id(self) -> str:
    return 'sdk.predicate.false'

  def perform_comparison(self, operator, challenge, check_against, on_many):
    return False
