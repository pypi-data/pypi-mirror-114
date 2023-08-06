from typing import Any

import requests
from werkzeug.utils import cached_property

from kama_sdk.model.supplier.base.supplier import Supplier


class HttpDataSupplier(Supplier):

  ENDPOINT_KEY = 'endpoint'

  @cached_property
  def endpoint(self):
    return self.get_attr(self.ENDPOINT_KEY, missing='warn')

  def get_output_format(self):
    super_value = super(HttpDataSupplier, self).get_output_format()
    return super_value or 'status_code'

  def _compute(self) -> Any:
    try:
      response = requests.get(self.endpoint)
      body_dict = {}
      try:
        body_dict = response.json()
      except:
        pass
      return dict(
        status_code=response.status_code,
        body=body_dict
      )
    except:
      return None
