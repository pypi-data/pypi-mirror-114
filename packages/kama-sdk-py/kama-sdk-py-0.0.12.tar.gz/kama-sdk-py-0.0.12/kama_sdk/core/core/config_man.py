import json
import traceback
from datetime import datetime
from json import JSONDecodeError
from typing import Optional, Dict, Any, List

from k8kat.res.config_map.kat_map import KatMap
from k8kat.utils.main.utils import deep_merge

from kama_sdk.core.core import config_man_helper as helper, consts
from kama_sdk.core.core import utils
from kama_sdk.core.core.types import KteaDict, KamaDict
from kama_sdk.core.core.utils import pwar, perr


class ConfigMan:
  def __init__(self):
    self._cmap: Optional[KatMap] = None
    self._ns: Optional[str] = None

  def invalidate_cmap(self):
    self._cmap = None

  def ns(self):
    if not self._ns:
      self._ns = read_ns()
      if not self._ns:
        print("[kama_sdk:config_man:ns] failed to read new NS")
    return self._ns

  def load_master_cmap(self, **kwargs) -> Optional[KatMap]:
    if self.ns():
      reload_strategy = kwargs.pop('reload', None)
      was_reloaded = False
      if self.should_reload_cmap(reload_strategy):
        was_reloaded = True
        fresh_cmap = KatMap.find(cmap_name, self.ns())
        if fresh_cmap:
          helper.track_cmap_read(self.ns())
        self._cmap = fresh_cmap

      if not self._cmap:
        if not was_reloaded:
          fresh_cmap = KatMap.find(cmap_name, self.ns())
          if fresh_cmap:
            helper.track_cmap_read(self.ns())
          self._cmap = fresh_cmap
        perr("config_man", f"dirty last hope getting cmap")

      if not self._cmap:
        cmap_id = f"[{self.ns()}/{cmap_name}]"
        details = f"reloaded={was_reloaded}"
        perr("config_man", f"load_master_cmap {cmap_id} nil. {details}", True)

      return self._cmap
    else:
      perr("config_man", f"load_master_cmap namespace is nil!")
      return None

  def read_space(self, **kwargs) -> Dict:
    if cmap := self.load_master_cmap(**kwargs):
      space_id = kwargs.get(space_kwarg) or consts.app_space
      json_enc_space = cmap.data.get(space_id) or '{}'

      if json_enc_space in ['{}', '', None]:
        sig = f"{type(json_enc_space)} {json_enc_space}!"
        pwar(self, f"read_space {space_id} was {sig}")
        for line in traceback.format_stack():
          print(line.strip())

      try:
        return json.loads(json_enc_space)
      except JSONDecodeError:
        pwar(self, f"read failed on corrupt space: {json_enc_space}")
        return {}
    else:
      perr(self, "read_space - master cmap was not, returning {}")
      return {}

  def write_space(self, new_value: Dict, **kwargs):
    if cmap := self.load_master_cmap(**kwargs):
      space_id = kwargs.get(space_kwarg) or consts.app_space
      try:
        json_encoded_space = json.dumps(new_value)
        cmap.raw.data[space_id] = json_encoded_space
        cmap.touch(save=True)
        helper.track_cmap_write(self.ns())
      except JSONDecodeError:
        pwar(self, f"write failed on corrupt space: {new_value}")

  def read_entry(self, key: str, **kwargs) -> Any:
    """
    Read in master ConfigMap from Kubernetes API or from
    cache, return entry in data.
    @param key: name of entry in ConfigMap.data
    @return: value at ConfigMap.data[key] or None
    """
    return self.read_space(**kwargs).get(key)

  def write_entry(self, key: str, serialized_value, **kwargs):
    self.write_entries({key: serialized_value}, **kwargs)

  def write_entries(self, serialized_assignments, **kwargs):
    space = self.read_space(**kwargs)
    updated_space = {**space, **serialized_assignments}
    self.write_space(updated_space, **kwargs)

  def write_typed_entries(self, assigns: Dict, **kwargs):
    func = type_serialize_entry
    ser_assignments = {k: func(k, v) for k, v in assigns.items()}
    self.write_entries(ser_assignments, **kwargs)

  def write_typed_entry(self, key: str, value: Any, **kwargs):
    self.write_typed_entries({key: value}, **kwargs)

  def read_typed_entry(self, key: str, **kwargs) -> Any:
    raw_value = self.read_entry(key, **kwargs)
    type_mapping = type_mappings.get(key)
    value = helper.parse_inbound(raw_value, type_mapping)
    if value is not None:
      return value
    else:
      backup = backup_mappings.get(type_mapping)
      return backup if backup is not None else value

  def read_dict(self, key: str, **kwargs) -> Dict:
    return self.read_entry(key, **kwargs) or {}

  def patch_into_deep_dict(self, dict_key: str, _vars: Dict, **kwargs):
    crt_dict = self.read_dict(dict_key, **kwargs)
    new_dict = deep_merge(crt_dict, _vars)
    self.write_typed_entry(dict_key, new_dict, **kwargs)

  def unset_deep_vars(self, dict_key: str, var_keys: List[str], **kwargs):
    crt_dict = self.read_dict(dict_key, **kwargs)
    flat_dict = utils.deep2flat(crt_dict)
    for victim_var_key in var_keys:
      flat_dict.pop(victim_var_key, None)
    updated_dict = utils.flat2deep(flat_dict)
    self.write_typed_entry(dict_key, updated_dict)

  def app_id(self, **kwargs) -> str:
    return self.read_typed_entry(app_id_key, **kwargs)

  def publisher_identifier(self, **kwargs) -> str:
    return self.read_typed_entry(publisher_identifier_key, **kwargs) or ''

  def app_identifier(self, **kwargs) -> str:
    return self.read_typed_entry(app_identifier_key, **kwargs) or ''

  def app_signature(self, **kwargs):
    return (
      self.app_identifier(**kwargs),
      self.publisher_identifier(**kwargs)
    )

  def install_id(self, **kwargs) -> str:
    return self.read_typed_entry(install_id_key, **kwargs)

  def install_token(self, **kwargs) -> str:
    return self.read_typed_entry(install_token_key, **kwargs)

  def friendly_name(self, **kwargs) -> str:
    return self.read_typed_entry(friendly_name_key, **kwargs)

  def application_status(self, **kwargs) -> str:
    return self.read_typed_entry(status_key, **kwargs)

  def prefs(self, **kwargs) -> Dict:
    return self.read_typed_entry(prefs_config_key, **kwargs)

  def read_ktea(self, **kwargs) -> KteaDict:
    return self.read_typed_entry(ktea_config_key, **kwargs)

  def read_kama(self, **kwargs) -> KamaDict:
    return self.read_typed_entry(kama_config_key, **kwargs) or {}

  def default_vars(self, **kwargs) -> Dict:
    return self.read_typed_entry(def_vars_key, **kwargs) or {}

  def vnd_inj_vars(self, **kwargs) -> Dict:
    return self.read_typed_entry(vndr_inj_vars_key, **kwargs) or {}

  def user_vars(self, **kwargs) -> Dict:
    return self.read_typed_entry(user_vars_key, **kwargs) or {}

  def last_updated(self, **kwargs) -> datetime:
    return self.read_typed_entry(key_last_updated, **kwargs)

  def manifest_variables(self, **kwargs) -> Dict:
    return utils.deep_merge(
      self.default_vars(**kwargs),
      self.vnd_inj_vars(**kwargs),
      self.user_vars(**kwargs),
    )

  def read_var(self, deep_key: str, **kwargs) -> Optional[Any]:
    deep_vars = self.manifest_variables(**kwargs)
    return utils.deep_get2(deep_vars, deep_key)

  def last_injected(self, **kwargs) -> datetime:
    result = self.read_typed_entry(key_last_synced, **kwargs)
    if result:
      return result
    else:
      use_backup = kwargs.pop('or_ancient', True)
      return helper.ancient_dt() if use_backup else None

  def unset_user_vars(self, var_keys: List[str], **kwargs):
    self.unset_deep_vars(user_vars_key, var_keys, **kwargs)

  def patch_user_vars(self, assignments: Dict[str, any], **kwargs):
    self.patch_into_deep_dict(user_vars_key, assignments, **kwargs)

  def patch_def_vars(self, assignments: Dict, **kwargs):
    self.patch_into_deep_dict(def_vars_key, assignments, **kwargs)

  def patch_vnd_inj_vars(self, assignments: Dict[str, any], **kwargs):
    self.patch_into_deep_dict(vndr_inj_vars_key, assignments, **kwargs)

  def patch_prefs(self, assignments: Dict[str, any], **kwargs):
    self.patch_into_deep_dict(prefs_config_key, assignments, **kwargs)

  def write_last_synced(self, timestamp: datetime, **kwargs):
    self.write_typed_entry(key_last_synced, timestamp, **kwargs)

  def write_last_injected(self, timestamp: datetime, **kwargs):
    self.write_typed_entry(key_last_synced, timestamp, **kwargs)

  def write_ktea(self, new_ktea: KteaDict, **kwargs):
    self.write_typed_entry(ktea_config_key, new_ktea, **kwargs)

  def write_status(self, new_status: str, **kwargs):
    self.write_typed_entry(status_key, new_status, **kwargs)

  def write_space_statuses(self, statuses: Dict):
    for space, status in statuses.items():
      self.write_last_synced(datetime.now(), space=space)
      self.write_status(status, space=space)

  def patch_ktea(self, partial_ktea: KteaDict, **kwargs):
    new_ktea = {**self.read_ktea(), **partial_ktea}
    self.write_ktea(new_ktea, **kwargs)

  def write_manifest_defaults(self, assigns: Dict, **kwargs):
    self.write_typed_entry(def_vars_key, assigns, **kwargs)

  def is_training_mode(self) -> bool:
    raw_val = self.read_entry(is_training_key)
    return raw_val in ['True', 'true', True]

  def is_real_deployment(self) -> bool:
    if utils.is_test():
      return False
    else:
      return not self.is_training_mode()

  def merged_manifest_vars(self, **kwargs) -> Dict:
    return {
      **self.default_vars(**kwargs),
      **self.vnd_inj_vars(**kwargs),
      **self.user_vars(**kwargs)
    }

  def should_reload_cmap(self, strategy: Optional[Any]) -> bool:
    if self._cmap:
      if strategy in [None, 'auto']:
        return helper.is_cmap_dirty(self.ns())
      elif strategy is True:
        return True
      elif strategy is False:
        return False
      else:
        print(f"[kama_sdk:config_man] bad cmap reload strategy {strategy}")
        return True
    else:
      return True


config_man = ConfigMan()


def read_ns() -> Optional[str]:
  """
  Reads application namespace from a file. If in-cluster, path
  will be Kubernetes default
  /var/run/secrets/kubernetes.io/serviceaccount/namespace. Else,
  wiz must be running in dev or training mode and tmp path will be used.
  @return: name of new namespace
  """
  path = ns_path if utils.is_in_cluster() else dev_ns_path
  try:
    with open(path, 'r') as file:
      value = file.read()
      if value:
        value = value.strip()
      else:
        print(f"[kama_sdk::configmap] FATAL ns empty at {path}")
      return value
  except FileNotFoundError:
    print(f"[kama_sdk::configmap] FATAL read failed")
    print(traceback.format_exc())
    return None


def coerce_ns(new_ns: str):
  """
  For out-of-cluster Dev mode only. Changes global ns variable
  to new val, and also writes new val to file so that other processes
  (e.g worker queues) use the same value.
  @param new_ns: name of new namespace
  """
  if utils.is_out_of_cluster():
    config_man._ns = new_ns
    with open(dev_ns_path, 'w') as file:
      file.write(new_ns)
  else:
    print(f"[kama_sdk::configman] illegal ns coerce!")


def type_serialize_entry(key: str, value: Any):
  if expected_type := type_mappings.get(key):
    if helper.does_type_match(value, expected_type):
      serialized_value = helper.serialize_outbound(value, expected_type)
      return serialized_value
    else:
      reason = f"[{key}]={value} must be {expected_type} " \
               f"but was {type(value)}"
      raise RuntimeError(f"[kama_sdk:config_man] {reason}")
  else:
    raise RuntimeError(f"[kama_sdk:config_man] illegal key {key}")


space_kwarg = 'space'
reload_kwarg = 'reload'

cmap_name = 'master'
spaces_key = 'spaces'

is_training_key = 'is_dev'
app_id_key = 'app_id'
install_id_key = 'install_id'
install_token_key = 'install_token'
status_key = 'status'
ktea_config_key = 'ktea'
kama_config_key = 'kama'

friendly_name_key = 'friendly_name'
publisher_identifier_key = 'publisher_identifier'
app_identifier_key = 'app_identifier'

def_vars_key = 'default_vars'
vndr_inj_vars_key = 'vendor_injection_vars'
user_inj_vars_key = 'user_injection_vars'
user_vars_key = 'user_vars'
prefs_config_key = 'prefs'

key_last_updated = 'last_updated'
key_last_synced = 'last_synced'
update_checked_at_key = 'update_checked_at'

install_token_path = '/etc/sec/install_token'
mounted_cmap_root_path = '/etc/master_config'
ns_path = '/var/run/secrets/kubernetes.io/serviceaccount/namespace'
dev_ns_path = '/tmp/kama_sdk-dev-ns'
iso8601_time_fmt = '%Y-%m-%d %H:%M:%S.%f'


type_mappings = {
  def_vars_key: dict,
  vndr_inj_vars_key: dict,
  user_vars_key: dict,
  user_inj_vars_key: dict,
  prefs_config_key: dict,
  ktea_config_key: dict,
  kama_config_key: dict,

  key_last_updated: datetime,
  key_last_synced: datetime,
  update_checked_at_key: datetime,

  is_training_key: bool,

  app_id_key: str,
  install_id_key: str,
  install_token_key: str,
  status_key: str,
  friendly_name_key: str,
  publisher_identifier_key: str,
  app_identifier_key: str

}

backup_mappings = {
  dict: {},
  str: ''
}

manifest_var_keys = [
  user_vars_key,
  vndr_inj_vars_key,
  user_inj_vars_key,
  def_vars_key
]
