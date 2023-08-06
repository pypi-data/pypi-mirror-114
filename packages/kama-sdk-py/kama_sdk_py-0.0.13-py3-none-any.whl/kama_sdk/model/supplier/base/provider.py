from werkzeug.utils import cached_property

from kama_sdk.model.supplier.base.supplier import Supplier


class Provider(Supplier):
  def get_serializer_type(self) -> str:
    return 'identity'
