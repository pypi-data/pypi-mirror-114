from typing import List

from werkzeug.utils import cached_property

from kama_sdk.model.base.model import Model
from kama_sdk.model.concern.concern_set import ConcernSetAdapter


class ConcernSuperSet(Model):

  @cached_property
  def concern_sets(self) -> List[ConcernSetAdapter]:
    return self.inflate_children(
      ConcernSetAdapter,
      prop=SETS_KEY,
    )

  @cached_property
  def slug(self) -> str:
    return self.resolve_prop(LABEL_KEY, lookback=0) or self.id()


LABEL_KEY = 'label'
SETS_KEY = 'sets'
