from typing import List, Optional, Union

from werkzeug.utils import cached_property

from kama_sdk.core.core.types import KoD, ErrCapture
from kama_sdk.core.core.utils import any2bool
from kama_sdk.model.action.base.action import Action, ActionError
from kama_sdk.model.action.base.multi_action import MultiAction
from kama_sdk.model.base import model
from kama_sdk.model.supplier.predicate.multi_predicate import MultiPredicate
from kama_sdk.model.supplier.predicate.predicate import Predicate

class RunPredicateAction(Action):

  def get_id(self) -> str:
    from_super = super().get_id()
    return from_super or self.predicate().get_id()

  @cached_property
  def abort_on_fail(self) -> bool:
    raw_value = self.get_attr('abort_on_fail', False)
    return any2bool(raw_value)

  def predicate(self) -> Predicate:
    return self.inflate_child(
      Predicate,
      prop=PREDICATE_KEY,
      resolve_kod=False
    )

  def get_title(self):
    return super().get_title() or self.predicate().get_title()

  @cached_property
  def info(self):
    return super().get_info() or self.predicate().get_info()

  def perform(self) -> None:
    predicate = self.predicate()
    if not any2bool(predicate.resolve()):
      raise ActionError(ErrCapture(
        fatal=self.abort_on_fail,
        type='negative_predicate',
        name=predicate.get_id(),
        reason=predicate.reason(),
        extras=dict(
          predicate_id=predicate.get_id(),
          predicate_kind=predicate.kind(),
          predicate_challlenge=predicate.get_challenge(),
          predicate_check_against=predicate.get_check_against(),
          **predicate.error_extras()
        )
      ))


class RunPredicatesAction(MultiAction):

  @cached_property
  def title(self) -> Optional[str]:
    return super().get_title() or 'Evaluate Predicates'

  @cached_property
  def info(self) -> Optional[str]:
    return super().get_info() or 'Run each predicate in the list before proceeding'

  def predicates(self) -> List[Predicate]:
    return self.inflate_children(
      Predicate,
      prop=PREDICATES_KEY,
      resolve_kod=False
    )

  @cached_property
  def sub_actions(self) -> List[Action]:
    kods = [predicate.serialize() for predicate in self.predicates()]
    return [self.pred_kod2action(kod) for kod in kods]

  def pred_kod2action(self, predicate_kod: KoD) -> RunPredicateAction:
    action = RunPredicateAction({PREDICATE_KEY: predicate_kod})
    action.parent = self
    return action

  @staticmethod
  def route(pred: Union[Predicate, MultiPredicate]) -> Optional[KoD]:
    if isinstance(pred, Predicate):
      base = {
        model.TITLE_KEY: pred.get_title(),
        model.INFO_KEY: pred.get_info(),
        model.KIND_KEY: RunPredicatesAction.__name__,
      }
      if isinstance(pred, MultiPredicate):
        pred: MultiPredicate = pred
        return {**base, PREDICATES_KEY: pred.sub_predicates_kods()}
      else:
        return {**base, PREDICATES_KEY: [pred.config]}


PREDICATES_KEY = 'predicates'
PREDICATE_KEY = 'predicate'
