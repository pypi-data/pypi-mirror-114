from typing import Optional

from werkzeug.utils import cached_property

from kama_sdk.core.core import updates_man, hub_api_client
from kama_sdk.core.core.types import ReleaseDict, ErrCapture
from kama_sdk.model.action.base.action import Action
from kama_sdk.model.action.base.action_errors import FatalActionError


class FetchUpdateAction(Action):

  def update_id(self) -> str:
    return self.get_attr('update_id')

  def perform(self, **kwargs) -> Optional[ReleaseDict]:
    update = updates_man.fetch_update(self.update_id())
    self.raise_if_none(update)
    return dict(update=update)

  def raise_if_none(self, update: Optional[ReleaseDict]) -> None:
    if not update:
      host = hub_api_client.backend_host()
      update_id = self.update_id()
      raise FatalActionError(ErrCapture(
        type='fetch_update',
        name='could_not_fetch',
        reason=f"fetch failed update id={update_id} host {host}",
        extras=dict(host=host, update_id=update_id)
      ))


class CommitKteaFromUpdateAction(Action):

  @cached_property
  def update(self) -> ReleaseDict:
    return self.get_attr('update')

  def perform(self):
    updates_man.commit_new_ktea(self.update)


KTEA_KEY = 'ktea'
