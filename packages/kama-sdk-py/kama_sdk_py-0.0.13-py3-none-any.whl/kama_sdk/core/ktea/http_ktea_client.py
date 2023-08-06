from typing import Dict, List
from urllib.parse import quote_plus

import requests

from kama_sdk.core.core import consts, hub_api_client
from kama_sdk.core.core.config_man import config_man
from kama_sdk.core.core.types import K8sResDict
from kama_sdk.core.core.utils import perr
from kama_sdk.core.ktea.ktea_client import KteaClient


class HttpKteaClient(KteaClient):

  def load_default_values(self) -> Dict[str, str]:
    return self.http_get(f"/values?{self.any_cmd_args()}")

  def template_manifest(self, values: Dict) -> List[K8sResDict]:
    endpoint = f"/template?{self.template_cmd_args()}"
    return self.http_post(endpoint, values)

  def load_preset(self, name: str) -> Dict[str, str]:
    return self.http_get(f"/presets/{name}?{self.any_cmd_args()}")

  def gen_url_up_to_action(self):
    ktea = self.ktea
    version = ktea.get('version')
    version_part = f"/{version}" if version else ''

    if self.is_managed_server():
      app_id, pub_id = config_man.app_signature(**self.mk_space_kwargs())
      if app_id and pub_id:
        host = hub_api_client.backend_host()
        up_to_version_part = f"{host}/ktea/{pub_id}/{app_id}"
      else:
        perr(self, f"fatal no app sig for space {self.get_config_space()}")
        up_to_version_part = None
    else:
      up_to_version_part = ktea['uri']

    # print("URL")
    # print(f"{up_to_version_part}{version_part}")
    return f"{up_to_version_part}{version_part}"

  def http_post(self, endpoint, payload):
    url = f'{self.gen_url_up_to_action()}{endpoint}'
    response = requests.post(url, json=payload)
    return response.json().get('data')

  def http_get(self, endpoint):
    url = f'{self.gen_url_up_to_action()}{endpoint}'
    response = requests.get(url)
    return response.json().get('data')

  def any_cmd_args(self) -> str:
    args_str = super().any_cmd_args()
    if args_str:
      return f"args={quote_plus(args_str)}"
    return ''

  def is_managed_server(self):
    return self.ktea.get('type') == consts.managed_server_ktea

  def gen_headers(self):
    if self.is_managed_server():
      return

  def template_cmd_args(self, *args) -> str:
    std_part = self.any_cmd_args()
    if not self.release_name():
      print("[kama_sdk:ktea+client] fatal ns is blank")
    ns_part = f"release_name={self.release_name()}"
    std_part = f"&{std_part}" if std_part else ""
    return f"{ns_part}{std_part}"
