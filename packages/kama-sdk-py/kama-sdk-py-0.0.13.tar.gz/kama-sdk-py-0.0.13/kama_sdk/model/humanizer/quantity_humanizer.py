from abc import ABC
from functools import lru_cache

from kama_sdk.core.core.utils import pwar
from kama_sdk.model.base.model import Model


class QuantityHumanizer(Model, ABC):

  @lru_cache
  def rounding(self):
    return self.get_attr(ROUNDING_KEY, 0)

  @lru_cache
  def prefix(self):
    return self.get_attr(PREFIX_KEY, '')

  @lru_cache
  def suffix(self):
    return self.get_attr(SUFFIX_KEY, '')

  def humanize_quantity(self, raw_quantity: float) -> float:
    try:
      better_quantity = self._humanize_quantity(raw_quantity)
      if self.rounding() > 0:
        return round(better_quantity, self.rounding())
      else:
        return int(better_quantity)
    except:
      pwar(self, f"humanize_quantity {raw_quantity}")
      return raw_quantity

  def humanize_expr(self, raw_value: float) -> str:
    better_expr = self._humanize_expr(raw_value)
    return f"{self.prefix()}{better_expr}{self.suffix()}"

  def _humanize_expr(self, raw_value: float) -> str:
    return str(self.humanize_quantity(raw_value))

  def unit(self, raw_value):
    pass

  @staticmethod
  def _humanize_quantity(value: float) -> float:
    return value


ROUNDING_KEY = 'rounding'
PREFIX_KEY = 'prefix'
SUFFIX_KEY = 'suffix'
