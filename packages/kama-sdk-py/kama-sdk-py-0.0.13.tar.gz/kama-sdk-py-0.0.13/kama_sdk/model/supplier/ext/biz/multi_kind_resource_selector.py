from typing import List

from k8kat.res.base.kat_res import KatRes
from werkzeug.utils import cached_property

from kama_sdk.model.supplier.ext.biz import resource_selector
from kama_sdk.model.supplier.ext.biz.resource_selector import ResourceSelector


class MultiKindResourceSelector(ResourceSelector):

  @cached_property
  def res_kinds(self) -> List[str]:
    return self.get_attr(RES_KINDS_KEY, [])

  def query_cluster(self) -> List[KatRes]:
    results = []
    for res_kind in self.res_kinds:
      selector = self.synthesize_single_kind_sel(res_kind)
      results.extend(selector.query_cluster())
    return results

  def synthesize_single_kind_sel(self, res_kind: str) -> ResourceSelector:
    config = {
      resource_selector.RES_KIND_KEY: res_kind,
      resource_selector.RES_NS_KEY: self.res_namespace(),
      resource_selector.RES_NAME_KEY: self.res_name,
      resource_selector.LABEL_SEL_KEY: self.label_selector,
      resource_selector.NOT_LABEL_SEL_KEY: self.not_label_selector,
      resource_selector.FIELD_SEL_KEY: self.field_selector,
      resource_selector.PROP_SEL_KEY: self.kat_prop_selector
    }

    return self.inflate_child(
      ResourceSelector,
      kod=config
    )


RES_KINDS_KEY = 'res_kinds'

