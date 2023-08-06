from typing import Dict

from k8kat.res.svc.kat_svc import KatSvc

from kama_sdk.model.concern.concern import Concern
from kama_sdk.model.concern.concern_card_adapter import ConcernCardAdapter
from kama_sdk.model.supplier.ext.misc.port_forward_spec_supplier import PortForwardSpecSupplier


class MonitoringConcernCardAdapter(ConcernCardAdapter):

  def concern(self) -> Concern:
    return self.get_prop('concern')

  def mon_config(self) -> Dict:
    return self.concern().get_prop('config')

  def svc(self) -> KatSvc:
    return self.concern().get_prop('svc')

  # @helper_prop(key='access')
  def access_helper(self):
    if self.concern().get_prop('is_online'):
      config = self.mon_config()
      is_in_cluster = config.get('relative_to_cluster') == 'in'
      is_proxy = config.get("proxy")
      svc = self.svc()
      pf_spec = PortForwardSpecSupplier({'source': svc})
      if is_in_cluster and is_proxy and pf_spec:
        name = f"localhost:{svc.first_tcp_port_num()}"
        action = {'type': 'port_forward', 'uri': pf_spec}
        return make_it("Port Forward", name, action)


def make_it(title, name, action):
  return {
    'type': 'Line',
    'elements': [
      {
        'type': ''
      }
    ]

  }