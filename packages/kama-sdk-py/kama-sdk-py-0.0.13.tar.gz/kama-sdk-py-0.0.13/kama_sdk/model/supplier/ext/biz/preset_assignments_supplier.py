from typing import Any

from kama_sdk.core.core.types import KteaDict
from kama_sdk.core.ktea.ktea_provider import ktea_client
from kama_sdk.model.supplier.base.supplier import Supplier


class PresetAssignmentsSupplier(Supplier):

  def optional_ktea_desc(self) -> KteaDict:
    return self.get_attr(
      KTEA_KEY,
      depth=100,
      lookback=False
    )

  def _compute(self) -> Any:
    client_inst = ktea_client(
      space=self.get_config_space(),
      ktea=self.optional_ktea_desc()
    )
    return client_inst.load_preset(self.get_source_data())


KTEA_KEY = 'ktea'
