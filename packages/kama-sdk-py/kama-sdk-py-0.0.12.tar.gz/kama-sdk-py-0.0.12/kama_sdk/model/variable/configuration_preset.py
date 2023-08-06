from functools import lru_cache
from typing import Dict

from kama_sdk.core.core import utils
from kama_sdk.core.core.utils import pwar
from kama_sdk.model.base.model import Model


class ConfigurationPreset(Model):

  @lru_cache
  def is_default(self) -> bool:
    value = self.resolve_prop(IS_DEFAULT_KEY, lookback=False)
    return utils.any2bool(value)

  @lru_cache
  def variables(self) -> Dict:
    try:
      return self.resolve_prop(VARIABLES_KEY, depth=100)
    except:
      pwar(self, f"{self.id()} get variables raised:", True)
      return {}


VARIABLES_KEY = 'variables'
IS_DEFAULT_KEY = 'default'
