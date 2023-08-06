from typing import List, Optional

from kama_sdk.model.base.model import Model
from kama_sdk.model.concern.concern_panel_adapters import ConcernPanelAdapter
from kama_sdk.model.concern.concern_view_adapter import ConcernViewAdapter


class ConcernPageAdapter(Model):
  def panel_adapters(self) -> List[ConcernPanelAdapter]:
    return self.inflate_children(
      ConcernPanelAdapter,
      prop=PANELS_KEY
    )

  def compute_and_serialize_panel(self, adapter_id: str):
    finder = lambda p: p.get_id() == adapter_id
    pool = self.panel_adapters()
    if result := next(filter(finder, pool), None):
      panel: ConcernPanelAdapter = result
      return panel.compute_and_serialize()
    else:
      return None


class ConcernDetailAdapter(ConcernViewAdapter):

  def page_adapters(self) -> List[ConcernPageAdapter]:
    return self.inflate_children(
      ConcernPageAdapter,
      prop=PAGES_KEY
    )

  def page_adapter(self, page_id: str) -> Optional[ConcernPageAdapter]:
    finder = lambda p: p.get_id() == page_id
    return next(filter(finder, self.page_adapters()), None)

  def compute_and_serialize_panel(self, page_id: str, panel_id: str):
    if page_adapter := self.page_adapter(page_id):
      page: ConcernPageAdapter = page_adapter
      return page.compute_and_serialize_panel(panel_id)
    else:
      return None


PAGES_KEY = 'page_adapters'
PANELS_KEY = 'panel_adapters'
