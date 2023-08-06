from typing import Type

from kama_sdk.core.core import consts
from kama_sdk.core.core.config_man import config_man
from kama_sdk.core.ktea.http_ktea_client import HttpKteaClient
from kama_sdk.core.ktea.ktea_client import KteaClient
from kama_sdk.core.ktea.local_exec_ktea_client import LocalExecKteaClient
from kama_sdk.core.ktea.virtual_ktea_client import vktea_clients_man


def ktea_client(**kwargs) -> KteaClient:
  space = kwargs.get('space')
  ktea = kwargs.get('ktea')

  if not ktea:
    space = space or consts.app_space
    ktea = config_man.read_ktea(space=space)

  client_class = find_client_class(ktea)
  return client_class(ktea, space)

def find_client_class(ktea) -> Type[KteaClient]:
  ktea_type = ktea['type']

  if ktea_type in server_types:
    return HttpKteaClient
  elif ktea_type == consts.local_exec_ktea:
    return LocalExecKteaClient
  elif ktea_type == consts.virtual_ktea:
    klass_or_name = ktea['uri']
    if type(klass_or_name) == type:
      klass = klass_or_name
    elif type(klass_or_name) == str:
      klass = vktea_clients_man.find_client(name=klass_or_name)
    else:
      raise Exception(f"[ktea_provider] invalid ktea uri {klass_or_name}")
    return klass
  else:
    raise RuntimeError(f"Illegal KTEA type {ktea_type}")


server_types = [consts.static_server_ktea, consts.managed_server_ktea]
