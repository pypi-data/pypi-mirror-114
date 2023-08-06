from functools import lru_cache
from typing import List, Optional

from kama_sdk.core.core.types import KoD
from kama_sdk.model.action.base import action as act_mod
from kama_sdk.model.action.ext.misc.run_predicates_action import RunPredicatesAction
from kama_sdk.model.base.model import Model
from kama_sdk.model.operation.stage import Stage
from kama_sdk.model.supplier.predicate.predicate import Predicate


class Operation(Model):

  @lru_cache
  def get_stages(self) -> List[Stage]:
    """
    Loads the Stages associated with the Operation.
    :return: list of Stage instances.
    """
    return self.inflate_children(Stage, prop=STAGES_KEY)

  def find_stage(self, stage_id: str) -> Stage:
    """
    Finds the Stage by key and inflates (instantiates) into a Stage instance.
    :param stage_id: identifier for desired Stage.
    :return: Stage instance.
    """
    matcher = lambda stage: stage.get_id() == stage_id
    return next(filter(matcher, self.get_stages()), None)

  def preflight_predicate(self) -> Optional[Predicate]:
    return self.inflate_child(
      Predicate,
      prop=PREFLIGHT_PREDICATE_KEY,
      resolve_kod=False,
      safely=True
    )

  def get_preflight_action_kod(self) -> Optional[KoD]:
    if predicate := self.preflight_predicate():
      synth_action_kod = RunPredicatesAction.route(predicate)
      action = self.inflate_child(RunPredicatesAction, kod={
        **synth_action_kod,
        **telem_patch
      })
      return action.serialize()
    else:
      return None


telem_patch = {act_mod.TELEM_EVENT_TYPE_KEY: act_mod.PREFLIGHT_EVENT_TYPE}
STAGES_KEY = 'stages'
PREFLIGHT_PREDICATE_KEY = 'preflight_predicate'
