from typing import Any, Optional
from werkzeug.utils import cached_property
from kama_sdk.core.core.config_man import config_man
from kama_sdk.core.core import config_man as cman_module
from kama_sdk.model.supplier.base.supplier import Supplier


class ConfigSupplier(Supplier):

  @cached_property
  def field_key(self) -> str:
    return self.get_attr(FIELD_KEY) or cman_module.user_vars_key

  @cached_property
  def reload_cmap(self) -> Optional[bool]:
    return self.get_attr(RELOAD_CMAP_KEY, None)

  def _compute(self) -> Any:
    if self.field_key == 'ns':
      return config_man.ns()
    else:
      result = config_man.read_typed_entry(
        self.field_key,
        **{
          cman_module.reload_kwarg: self.reload_cmap,
          cman_module.space_kwarg: self.get_config_space()
        }
      )
      return result


class MergedVariablesSupplier(Supplier):
  def _compute(self) -> Any:
    return config_man.manifest_variables(**{
      cman_module.space_kwarg: self.get_config_space()
    })


class DefaultVariablesSupplier(Supplier):
  def _compute(self) -> Any:
    return config_man.default_vars(**{
      cman_module.space_kwarg: self.get_config_space()
    })


FIELD_KEY = 'field_key'
RELOAD_CMAP_KEY = 'reload'
