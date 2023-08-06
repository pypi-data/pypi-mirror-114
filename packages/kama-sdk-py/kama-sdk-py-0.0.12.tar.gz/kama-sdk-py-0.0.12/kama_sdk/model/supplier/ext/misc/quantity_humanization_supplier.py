from werkzeug.utils import cached_property

from kama_sdk.model.humanizer.quantity_humanizer import QuantityHumanizer
from kama_sdk.model.supplier.base import supplier
from kama_sdk.model.supplier.base.supplier import Supplier


class QuantityHumanizationSupplier(Supplier):

  def backend(self) -> QuantityHumanizer:
    return self.inflate_child(
      QuantityHumanizer,
      prop=BACKEND_KEY
    )

  @cached_property
  def output_format(self):
    return self.resolve_prop(
      supplier.OUTPUT_FMT_KEY,
      backup=QUANT_AND_UNIT_FLAG,
      lookback=0
    )

  def resolve(self) -> str:
    quantity = coerce_quant(self.get_prop(supplier.SRC_DATA_KEY))
    if backend := self.backend():
      return thing(self.output_format, quantity, backend)
    else:
      return str(quantity)


def coerce_quant(raw_quant) -> float:
  try:
    return float(raw_quant)
  except:
    return 0.0


def thing(flag, quantity, humanizer: QuantityHumanizer):
  if flag == QUANT_ONLY_FLAG:
    return humanizer.humanize_quantity(quantity)
  elif flag == UNIT_ONLY_FLAG:
    return humanizer.unit(quantity)
  elif flag == QUANT_AND_UNIT_FLAG:
    return humanizer.humanize_expr(quantity)
  else:
    print(f"danger bad humanization type {flag}")


BACKEND_KEY = 'backend'
QUANT_ONLY_FLAG = 'quantity'
UNIT_ONLY_FLAG = 'unit'
QUANT_AND_UNIT_FLAG = 'quantity-and-unit'
