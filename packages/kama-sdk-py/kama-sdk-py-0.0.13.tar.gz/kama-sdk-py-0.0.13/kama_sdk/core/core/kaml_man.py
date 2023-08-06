import importlib
from typing import List, Optional

from kama_sdk.core.core.config_man import config_man
from kama_sdk.core.core.utils import pwar, perr

from kama_sdk.core.core.kaml import KamlDescriptor, KamlMeta
from kama_sdk.model.base.model import models_man


_kaml_metas: List[KamlMeta] = []


def kaml_ids() -> List[str]:
  return [m['id'] for m in _kaml_metas]


def read_pipfile():
  with open('Pipfile', 'r') as file:
    print(file.read())


def get_meta(_id: str) -> Optional[KamlMeta]:
  finder = lambda meta: meta['id'] == _id
  return next(filter(finder, _kaml_metas), None)


def registered_kamls_ids() -> List[str]:
  def is_registered(_id: str) -> bool:
    return config_man.install_token(space=_id) is not None
  return list(filter(is_registered, kaml_ids()))


def load_package_module(package_name: str) -> KamlDescriptor:
  if package_name not in kaml_ids():
    module_fqdn = f"{package_name}.kaml"
    try:
      loaded_package = importlib.import_module(package_name)
      loaded_module = importlib.import_module(module_fqdn)
      describe_method = getattr(loaded_module, 'describe_self')
      descriptor = describe_method()

      version = '0.0.0'
      if hasattr(loaded_package, '__version__'):
        version = loaded_package.__version__

      descriptor['version'] = version

      if not descriptor.get('id'):
        descriptor['id'] = package_name
      return descriptor
    except:
      pt2 = "or does not have a module a 'kaml' that "
      pt3 = "responds to 'describe_self() -> KamlDescriptor'"
      perr(__name__, f"error loading {package_name}", True)
      pwar(__name__, f"package {package_name} does not exist {pt2} {pt3}")
  else:
    pwar(__name__, f"kaml {package_name} was already registered!")


def dangerously_register_kaml(descriptor: KamlDescriptor):
  _id = descriptor['id']
  version = descriptor.get('version')

  app_identifier = descriptor.get('app_identifier')
  org_identifier = descriptor.get('publisher_identifier')

  model_descriptors = descriptor.get('model_descriptors', [])
  model_classes = descriptor.get('model_classes', [])
  telem_backend = descriptor.get('telem_backend')
  asset_paths = descriptor.get('asset_paths', [])

  models_man.add_any_descriptors(model_descriptors, _id)
  models_man.add_models(model_classes)
  models_man.add_asset_dir_paths(asset_paths)

  if telem_backend:
    models_man.set_telem_backend(telem_backend)

  _kaml_metas.append(KamlMeta(
    id=_id,
    app_identifier=app_identifier,
    publisher_identifier=org_identifier,
    version=version
  ))
  

def register_kaml(package_name: str):
  if descriptor := load_package_module(package_name):
    dangerously_register_kaml(descriptor)
  else:
    pwar(__name__, f"{package_name} was not registered; see logs ^")
