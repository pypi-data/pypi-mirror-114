from copy import deepcopy
from typing import Optional, Dict, List

from kama_sdk.core.core import hub_api_client
from kama_sdk.core.core.types import ErrCapture, EventCapture
from kama_sdk.core.telem import flash_helper
from kama_sdk.core.telem.telem_backend import TelemBackend
from kama_sdk.model.base.model import models_man

synced_key = 'synced'
primary_key = '_id'

events_coll_id = 'events'
backups_coll_id = 'config_backups'
errors_coll_id = 'errors'


def handle_event(event: EventCapture):
  flash_helper.push_record(events_coll_id, event)


def handle_error(error: ErrCapture):
  flash_helper.push_record(errors_coll_id, error)


def flush_all():
  flush_flash()


def flush_flash():
  backend = get_backend()

  # print("BEFOORE FLUSH ERR PUSH")
  # print(flash_helper.read_collection(errors_coll_id))

  for collection_id in [events_coll_id, errors_coll_id]:
    # print(f"FLUSHING Q {collection_id}")
    # print(flash_helper.read_collection(collection_id))
    for record in flash_helper.read_collection(collection_id):
      is_synced = upload_item(collection_id, record)
      record[synced_key] = is_synced
      if backend:
        backend.create_record(collection_id, record)
    flash_helper.write_collection(collection_id, [])


def create_backup_record(backup: Dict) -> Optional[Dict]:
  if backend := get_backend():
    return backend.create_record(backups_coll_id, backup)


def flush_persistent_store():
  if backend := get_backend():
    for coll_id in [events_coll_id, errors_coll_id]:
      records = backend.query_collection(coll_id, {synced_key: False})
      for record in records:
        if upload_item(coll_id, record):
          record[synced_key] = True
          backend.update_record(coll_id, record)


def list_config_backups() -> List[Dict]:
  if backend := get_backend():
    return backend.query_collection(backups_coll_id, {})
  else:
    return []


def get_config_backup(_id: str) -> Optional[Dict]:
  if backend := get_backend():
    return backend.find_record_by_id(backups_coll_id, _id)
  else:
    return None


def supports_persistence() -> bool:
  # if backend := get_backend():
  #   return backend.is_enabled()
  # else:
  #   return False
  return True


def can_persist() -> bool:
  return False


def get_backend() -> Optional[TelemBackend]:
  return models_man.get_telem_backend()


def upload_item(collection_name: str, item) -> bool:
  hub_key = f'kama_{collection_name}'[0:-1]
  clean_item = deepcopy(item)
  clean_item.pop(primary_key, None)
  clean_item.pop(synced_key, None)
  resp = hub_api_client.post(f'/{hub_key}s', {hub_key: clean_item})
  return resp.status_code == 400
