import base64
import json
from typing import Dict

from kama_sdk.model.base.model import Model
from kama_sdk.model.concern.concern_detail_adapter import ConcernDetailAdapter, ConcernPageAdapter
from kama_sdk.model.concern.concern_set import ConcernSetAdapter
from kama_sdk.model.concern.concern_table import ConcernTableAdapter
from kama_sdk.serializers import common_serializers


def encode_seed(seed_dict: Dict) -> str:
  utf_json = json.dumps(seed_dict)
  return base64.b64encode(utf_json)


def ser_simple_child(model: Model) -> Dict:
  return common_serializers.ser_meta(model)


def serialize_set_meta(concern_set: ConcernSetAdapter, seeds=False):
  bundle = {
    **ser_simple_child(concern_set),
    'one_shot': concern_set.is_one_shot,
    'view_type': concern_set.view_type()
  }

  serialized_cols = None
  serialized_seeds = None

  if isinstance(concern_set, ConcernTableAdapter):
    serialized_cols = concern_set.column_definitions

  if seeds and concern_set.is_one_shot:
    seeds = concern_set.compute_concern_seeds()
    serialized_seeds = list(map(encode_seed, seeds))

  bundle['columns'] = serialized_cols
  bundle['seeds'] = serialized_seeds

  return bundle


def ser_detail_meta(adapter: ConcernDetailAdapter) -> Dict:
  serd_pages = list(map(ser_simple_child, adapter.page_adapters()))
  return {
    **ser_simple_child(adapter),
    'pages': serd_pages
  }


def ser_page_meta(adapter: ConcernPageAdapter) -> Dict:
  panel_ids = [panel.id() for panel in adapter.panel_adapters()]
  return {
    **ser_simple_child(adapter),
    'panel_ids': panel_ids
  }
