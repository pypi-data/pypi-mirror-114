from werkzeug.utils import cached_property

from kama_sdk.model.base.model import Model


class VariableCategory(Model):

  @cached_property
  def graphic(self) -> str:
    return self.get_prop(GRAPHIC_KEY, 'tune')

  @cached_property
  def graphic_type(self) -> str:
    return self.get_prop(GRAPHIC_TYPE_KEY, 'icon')


GRAPHIC_KEY = 'graphic'
GRAPHIC_TYPE_KEY = 'graphic_type'
