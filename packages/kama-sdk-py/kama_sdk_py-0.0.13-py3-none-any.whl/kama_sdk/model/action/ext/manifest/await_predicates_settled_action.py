import time
from typing import List

from werkzeug.utils import cached_property

from kama_sdk.core.core import consts
from kama_sdk.core.core.types import ErrCapture
from kama_sdk.core.core.utils import pwar
from kama_sdk.model.action.base.action import Action
from kama_sdk.model.action.base.action_errors import FatalActionError
from kama_sdk.model.action.base.multi_action import MultiAction
from kama_sdk.model.operation.predicate_statuses_computer import PredicateStatusesComputer
from kama_sdk.model.supplier.predicate.predicate import Predicate


class AwaitPredicatesSettledAction(MultiAction):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._predicates_hack: List[Predicate] = []
    self._sub_actions_hack: List[Action] = []

  def predicates(self) -> List[Predicate]:
    return self.inflate_children(
      Predicate,
      prop=PREDICATES_KEY,
      resolve_kod=False
    )

  @cached_property
  def timeout_seconds(self) -> int:
    return self.get_attr(TIMEOUT_SECONDS_KEY, backup=180)

  def final_sub_actions(self) -> List[Action]:
    return self._sub_actions_hack

  def perform(self) -> None:
    computer = PredicateStatusesComputer(self.predicates())

    optimists = computer.optimist_predicates
    self._sub_actions_hack = list(map(self.pred2action, optimists))

    start_ts = time.time()
    did_time_out = True
    iteration = 1

    while time.time() - start_ts < self.timeout_seconds:
      computer.perform_iteration()
      self.update_actions(computer)
      self.add_logs(computer.explanations)
      self.raise_for_negative_outcomes(computer)

      if computer.did_finish():
        did_time_out = False
        break
      else:
        iteration += 1
        time.sleep(2)

    raise_for_timeout(did_time_out)

  def find_action_by_pred(self, predicate_id: str) -> Action:
    finder = lambda action: action.config['predicate_id'] == predicate_id
    return next(filter(finder, self.final_sub_actions()))

  def update_actions(self, computer: PredicateStatusesComputer):
    for predicate in computer.optimist_predicates:
      evaluation = computer.find_eval(predicate.get_id())
      if action := self.find_action_by_pred(predicate.get_id()):
        if evaluation.get('met'):
          action.set_status(consts.pos)
        else:
          pessimistic_twin_eval_id = twin_flip(predicate.get_id())
          pessimistic_twin = computer.find_eval(pessimistic_twin_eval_id)
          if pessimistic_twin:
            # print(f"twin({predicate.id()}) => {pessimistic_twin_eval_id}")
            if pessimistic_twin.get('met'):
              action.set_status(consts.neg)
            else:
              action.set_status(consts.rng)
          else:
            pwar(self, f"{predicate.get_id()} has no twin")
      else:
        pwar(self, f"{predicate.get_id()} has no twin")

    if computer.did_fail():
      for sub in self.final_sub_actions():
        if sub.status == consts.rng:
          sub.set_status(consts.idl)

  def pred2action(self, predicate: Predicate) -> Action:
    action = Action(dict(
      id=predicate.get_id(),
      title=predicate.get_title(),
      info=predicate.get_info(),
      predicate_id=predicate.get_id()
    ))
    action.parent = self
    return action

  @staticmethod
  def raise_for_negative_outcomes(computer: PredicateStatusesComputer):
    if computer.did_fail():
      predicate = computer.culprit_predicate()
      prefix = "raise_for_negative_outcomes predicate"
      pwar(None, f"{prefix}: {predicate.debug_bundle()}")

      raise FatalActionError(ErrCapture(
        name=f"\"{predicate.get_title()}\" failure status",
        type='predicate_settle_negative',
        reason=predicate.reason(),
        extras=dict(
          predicate_id=predicate.get_id(),
          predicate_kind=predicate.kind(),
          **predicate.error_extras()
        )
      ))


def raise_for_timeout(timed_out: bool):
  if timed_out:
    raise FatalActionError(ErrCapture(
      name='Timeout',
      type='predicate_settle_timeout',
      reason='The predicates being evaluated did not reach '
             'a positive status in time.'
    ))


def twin_flip(pred_id: str) -> str:
  if pred_id.endswith(f"-{consts.neg}"):
    return pred_id.replace(f"-{consts.neg}", f"-{consts.pos}")
  else:
    return pred_id.replace(f"-{consts.pos}", f"-{consts.neg}")


PREDICATES_KEY = 'predicates'
TIMEOUT_SECONDS_KEY = 'timeout_seconds'
