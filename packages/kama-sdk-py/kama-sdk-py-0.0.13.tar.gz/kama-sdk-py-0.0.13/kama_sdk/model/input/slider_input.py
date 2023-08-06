import traceback
from typing import Dict, Any

from werkzeug.utils import cached_property

from kama_sdk.model.input.generic_input import GenericInput


class SliderInput(GenericInput):
  @cached_property
  def min(self) -> int:
    return self.get_attr('min', 0)

  @cached_property
  def max(self) -> int:
    return self.get_attr('max', 10)

  @cached_property
  def step(self) -> int:
    return self.get_attr('step', 1)

  @cached_property
  def suffix(self):
    return self.get_attr('suffix', '')

  def get_extras(self) -> Dict[str, any]:
    return dict(
      min=self.min,
      max=self.max,
      step=self.step,
      suffix=self.suffix
    )

  def sanitize_for_validation(self, value: Any) -> Any:
    if value is not None and self.suffix:
      # noinspection PyBroadException
      try:
        return float(str(value).split(self.suffix)[0])
      except:
        print("[kama_sdk::slider_input] sanitize input failed:")
        print(traceback.format_exc())
        return value
    else:
      return value
