from functools import cached_property
from typing import Optional

from k8kat.res.base.kat_res import KatRes

from kama_sdk.model.action.base.action import Action
from kama_sdk.model.supplier.ext.biz.resource_selector import ResourceSelector


class PatchResourceAction(Action):

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

  @cached_property
  def patch_contents(self):
    return self.get_attr(PATCH_KEY, lookback=False) or {}

  def perform(self):
    if resource := self.kat_res:

      def modify():
        pass

      resource.patch(modify)


PATCH_KEY = 'patch'
