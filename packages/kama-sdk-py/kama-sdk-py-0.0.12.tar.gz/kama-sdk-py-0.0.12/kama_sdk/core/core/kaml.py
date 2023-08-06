from typing import List, Dict, Type, Any

from typing_extensions import TypedDict

from kama_sdk.core.ktea.virtual_ktea_client import VirtualKteaClient
from kama_sdk.core.telem.telem_backend import TelemBackend
from kama_sdk.model.base.model import Model

class KamlDescriptor(TypedDict, total=False):
  id: str
  publisher_identifier: str
  app_identifier: str
  model_descriptors: List[Dict]
  asset_paths: List[str]
  model_classes: List[Type[Model]]
  virtual_kteas: List[Type[VirtualKteaClient]]
  telem_backend: Type[TelemBackend]
  shell_bindings: Dict[str, Any]
  verified: bool
  version: str


class KamlMeta(TypedDict):
  id: str
  publisher_identifier: str
  app_identifier: str
  version: str
