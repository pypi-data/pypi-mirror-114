from typing import Any, Optional

from werkzeug.utils import cached_property

from kama_sdk.model.supplier.base import supplier
from kama_sdk.model.supplier.base.supplier import Supplier


class PropsSupplier(Supplier):

  def orig_output_format(self) -> Optional[str]:
    return self.config.get('output')

  def get_source_data(self) -> Optional[Any]:
    output_fmt = self.orig_output_format()
    if jq_accessor_token in output_fmt:
      master_key = output_fmt.split(jq_accessor_token)[0]
    elif legacy_accessor_token in output_fmt:
      master_key = output_fmt.split(legacy_accessor_token)[0]
    else:
      master_key = output_fmt
    return self.get_attr(master_key)

  def get_output_format(self):
    orig = self.orig_output_format()
    if orig and type(orig) == str:
      if jq_accessor_token in orig:
        return orig.split(jq_accessor_token)[1]
      elif legacy_accessor_token in orig:
        return orig.split(legacy_accessor_token)[1]
      else:
        return None
    else:
      return orig

  def get_serializer_type(self) -> str:
    if legacy_accessor_token in self.orig_output_format():
      return 'legacy'
    else:
      return 'jq'


class SelfSupplier(Supplier):
  def get_source_data(self) -> Optional[any]:
    return self


class DelayedInflateSupplier(Supplier):
  def get_source_data(self) -> Optional[any]:
    return self.config.get(supplier.SRC_DATA_KEY)

  def _compute(self) -> Any:
    return self.inflate_child(
      Supplier,
      kod=self.get_source_data(),
      safely=True
    )


jq_accessor_token = '->'
legacy_accessor_token = '=>'
