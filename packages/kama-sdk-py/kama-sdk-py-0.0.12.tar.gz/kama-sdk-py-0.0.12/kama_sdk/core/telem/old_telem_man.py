# import json
# from copy import deepcopy
# from typing import Optional, Dict, List
#
# from bson import ObjectId
# from pymongo.database import Database
# from pymongo.results import InsertOneResult
#
# from kama_sdk.core.core import hub_api_client, utils, status_man
# from kama_sdk.core.core.config_man import config_man
# from kama_sdk.core.core.types import ErrCapture, EventCapture
# from kama_sdk.core.telem.telem_flash_storage import TelemFlashStorage
# from kama_sdk.model.base.model import models_man
#
#
# def database() -> Optional[Database]:
#   return connection_obj[key_conn_obj_db]
#
#
# def create_session_if_none() -> Optional[Database]:
#   if not database():
#     if backend := models_man.get_telem_backend():
#       connection_obj[key_conn_obj_db] = backend.connect()
#     return database()
#
#
# def clear_session():
#   del connection_obj[key_conn_obj_db]
#
#
# def is_db_avail() -> bool:
#   return True if create_session_if_none() else False
#
#
# def parametrized(dec):
#   def layer(*args, **kwargs):
#     def repl(f):
#       return dec(f, *args, **kwargs)
#     return repl
#   return layer
#
#
# @parametrized
# def connected_and_enabled(func, backup=None):
#   def aux(*xs, **kws):
#     if create_session_if_none():
#       return func(*xs, **kws)
#     else:
#       return backup
#   return aux
#
#
# flash_storage = TelemFlashStorage()
#
# flash_events: List[EventCapture] = []
# flash_errors: List[ErrCapture] = []
#
#
# def store_event(event: EventCapture) -> InsertOneResult:
#   return store_list_element(EVENTS_COLLECTION_NAME, event)
#
#
# def store_config_backup(outcome: Dict) -> InsertOneResult:
#   return store_list_element(BACKUPS_COLLECTION_KEY, outcome)
#
#
# def list_errors():
#   return list_records(ERRORS_COLLECTION_NAME)
#
#
# def list_events():
#   return list_records(EVENTS_COLLECTION_NAME)
#
#
# def list_config_backups():
#   return list_records(BACKUPS_COLLECTION_KEY)
#
#
# def find_event(query: Dict) -> Optional[EventCapture]:
#   return find_record(EVENTS_COLLECTION_NAME, query)
#
#
# def find_error(query: Dict) -> Optional[ErrCapture]:
#   return find_record(ERRORS_COLLECTION_NAME, query)
#
#
# def get_config_backup(record_id) -> Optional[Dict]:
#   return find_record_by_id(BACKUPS_COLLECTION_KEY, record_id)
#
#
# @connected_and_enabled(backup=None)
# def store_list_element(coll_id: str, item: Dict) -> InsertOneResult:
#   item = {**item, synced_key: False}
#   return database()[coll_id].insert_one(item)
#
#
# @connected_and_enabled(backup=[])
# def list_records(coll_id: str):
#   return list(database()[coll_id].find())
#
#
# @connected_and_enabled(backup=[])
# def purge_all():
#   for collection in database().list_collections():
#     database()[collection['name']].drop()
#
#
# @connected_and_enabled(backup=None)
# def find_record(collection_id: str, query: Dict):
#   collection = database()[collection_id]
#   return collection.find_one(query)
#
#
# @connected_and_enabled(backup=None)
# def find_record_by_id(collection_id, record_id):
#   return find_record(collection_id, {'_id': ObjectId(record_id)})
#
#
# def upload_all_meta():
#   status_man.upload_all_statuses()
#   upload_events_and_errors()
#
#
# @connected_and_enabled(backup=None)
# def upload_events_and_errors():
#   if config_man.is_training_mode():
#     return False
#
#   if utils.is_test():
#     return False
#
#   session = create_session_if_none()
#
#   if not session:
#     return False
#
#   for collection_name in [ERRORS_COLLECTION_NAME, EVENTS_COLLECTION_NAME]:
#     collection = session[collection_name]
#     items = collection.find({synced_key: False})
#     for item in items:
#       hub_key = f'kama_{collection_name}'[0:-1]
#       clean_item = deepcopy(item)
#       clean_item.pop(primary_key, None)
#       clean_item.pop(synced_key, None)
#       resp = hub_api_client.post(f'/{hub_key}s', {hub_key: clean_item})
#       if not resp.status_code == 400:
#         query = {primary_key: item[primary_key]}
#         patch = {'$set': {synced_key: True}}
#         collection.update_one(query, patch)
#
#
# key_conn_obj_db = 'db'
#
#
# connection_obj = {key_conn_obj_db: None}
