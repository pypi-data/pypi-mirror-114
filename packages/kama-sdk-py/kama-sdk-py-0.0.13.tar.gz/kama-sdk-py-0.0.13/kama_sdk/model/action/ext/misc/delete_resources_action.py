from typing import List, Optional

from k8kat.res.base.kat_res import KatRes
from werkzeug.utils import cached_property

from kama_sdk.core.core import utils
from kama_sdk.core.core.types import ErrCapture
from kama_sdk.model.action.base.action import Action, ActionError
from kama_sdk.model.action.base.multi_action import MultiAction
from kama_sdk.model.supplier.ext.biz.resource_selector import ResourceSelector


class DeleteResourceAction(Action):

  @cached_property
  def is_absent_res_fatal(self) -> bool:
    raw = self.get_attr(TREAT_MISSING_AS_FATAL_KEY, lookback=False)
    return utils.any2bool(raw)

  @cached_property
  def wait_until_gone(self) -> bool:
    value = self.get_attr(WAIT_TIL_GONE_KEY, backup=True)
    return utils.any2bool(value)

  def get_title(self) -> str:
    if self.kat_res:
      res = self.kat_res
      return f"Delete {res.kind}/{res.name}"
    else:
      return "Victim resource does not exist"

  @cached_property
  def info(self) -> str:
    verb = "" if self.wait_until_gone else "do not"
    return f"Delete the resource, {verb} wait until it is destroyed"

  @cached_property
  def selector(self) -> ResourceSelector:
    return self.inflate_child(ResourceSelector, prop='selector')

  @cached_property
  def kat_res(self) -> Optional[KatRes]:
    _kat_res = self.config.get('kat_res')
    if not _kat_res:
      q_results = self.selector.query_cluster()
      _kat_res = q_results[0] if len(q_results) > 0 else None
    return _kat_res

  def perform(self) -> None:
    if victim := self.kat_res:
      victim.delete(wait_until_gone=self.wait_until_gone)
    else:
      raise ActionError(ErrCapture(
        fatal=self.is_absent_res_fatal,
        reason="Resource to be deleted did not exist in the first place",
        type='delete_event_no_res'
      ))


class DeleteResourcesAction(MultiAction):

  def get_selectors(self) -> List[ResourceSelector]:
    return self.inflate_children(
      ResourceSelector,
      prop=RESOURCE_SELECTORS_KEY
    )

  @cached_property
  def title(self) -> Optional[str]:
    explicit = super(DeleteResourcesAction, self).get_title()
    return explicit or "Delete selected resources"

  @cached_property
  def info(self) -> Optional[str]:
    explicit = super(DeleteResourcesAction, self).get_info()
    return explicit or "Delete resources one by one, wait for non-existence"

  @cached_property
  def sub_actions(self) -> List[Action]:
    resources = self.selected_resources()
    deletion_actions = [self.kat_rest2action(r) for r in resources]
    return deletion_actions

  def selected_resources(self) -> List[KatRes]:
    results = [s.query_cluster() for s in self.get_selectors()]
    return utils.flatten(results)

  def kat_rest2action(self, kat_res: KatRes) -> DeleteResourceAction:
    config = {
      'id': f"{self.get_id()}.{kat_res.kind}.{kat_res.name}",
      KAT_RES_KEY: kat_res,
      TREAT_MISSING_AS_FATAL_KEY: self.config.get(TREAT_MISSING_AS_FATAL_KEY),
      WAIT_TIL_GONE_KEY: self.config.get(WAIT_TIL_GONE_KEY)
    }
    return self.inflate_child(DeleteResourceAction, kod=config)


RESOURCE_SELECTORS_KEY = 'selectors'
WAIT_TIL_GONE_KEY = 'wait_until_gone'
TREAT_MISSING_AS_FATAL_KEY = 'missing_is_fatal'
KAT_RES_KEY = 'kat_res'
