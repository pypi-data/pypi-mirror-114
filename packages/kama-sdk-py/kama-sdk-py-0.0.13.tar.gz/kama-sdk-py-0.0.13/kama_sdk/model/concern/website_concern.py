from k8kat.res.svc.kat_svc import KatSvc

from kama_sdk.model.concern.concern import Concern


class WebsiteConcern(Concern):
  def svc(self) -> KatSvc:
    return self.get_attr(SVC_KEY)

  def best_url(self) -> str:
    pass


SVC_KEY = 'svc'
PORT_FORWARD_SPEC_KEY = 'port_forward_spec'
