from flask import Blueprint, jsonify

from kama_sdk.controllers import ctrl_utils
from kama_sdk.core.core import kaml_man
from kama_sdk.core.core.config_man import config_man
from kama_sdk.core.core import config_man as cman_mod
from kama_sdk.core.core.kaml import KamlMeta
from kama_sdk.core.core.utils import pwar

BASE = '/api/plugins'

controller = Blueprint('plugins_controller', __name__)


@controller.route(f"{BASE}/all")
def list_plugins():
  config_man.invalidate_cmap()
  serialized = list(map(serialize_config_space, kaml_man.kaml_ids()))
  return jsonify(data=serialized)


@controller.route(f"{BASE}/all/<plugin_id>/authorize", methods=['POST'])
def authorize_plugin(plugin_id: str):
  if plugin_id in kaml_man.kaml_ids():
    given_attrs = ctrl_utils.parse_json_body()

    raw_patch = {key: given_attrs.get(key) for key in auth_exp_keys}
    patch = {k: v for k, v in raw_patch.items() if v is not None}

    if not len(raw_patch) == len(patch):
      pwar(__name__, f"modified plugin auth {raw_patch} -> {patch}")

    config_man.write_typed_entries(patch, **{
      cman_mod.space_kwarg: plugin_id
    })
    return jsonify(data='success')
  else:
    return jsonify(error=f"no such kaml {plugin_id}"), 404


def serialize_config_space(kaml_id: str):
  kwargs = {
    cman_mod.space_kwarg: kaml_id,
    cman_mod.reload_kwarg: False
  }

  meta: KamlMeta = kaml_man.get_meta(kaml_id) or ''

  return {
    'id': kaml_id,
    'version':  meta.get('version'),
    'app_identifier': meta.get('app_identifier'),
    'publisher_identifier': meta.get('publisher_identifier'),
    'install_id': config_man.install_id(**kwargs),
    'install_token': config_man.install_token(**kwargs),
    'status': config_man.application_status(**kwargs),
    'ktea': config_man.read_ktea(**kwargs),
  }


auth_exp_keys = [
  cman_mod.install_id_key,
  cman_mod.install_token_key,
  cman_mod.ktea_config_key,
  cman_mod.kama_config_key,
  cman_mod.publisher_identifier_key,
  cman_mod.app_identifier_key
]
