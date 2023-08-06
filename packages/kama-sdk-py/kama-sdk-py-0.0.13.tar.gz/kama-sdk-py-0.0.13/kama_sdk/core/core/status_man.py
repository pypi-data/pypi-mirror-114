from typing import Optional, Dict

from kama_sdk.core.core import hub_api_client, kaml_man, consts, utils
from kama_sdk.core.core.config_man import config_man
from kama_sdk.core.core.utils import pwar, perr
from kama_sdk.model.base import model
from kama_sdk.model.supplier.base.supplier import Supplier


def compute_all_statuses() -> Dict[str, str]:
  statuses = {}
  for space_id in [consts.app_space, *kaml_man.kaml_ids()]:
    status = compute_space_status(space_id)
    statuses[space_id] = status
  return statuses


def compute_space_status(space_id) -> str:
  if computer := space_status_computer(space_id):
    try:
      computed_outcome = computer.resolve()
    except Exception:
      perr(__name__, f"status comp for space {space_id}", True)
      return consts.brk

    positive = utils.any2bool(computed_outcome)
    return consts.rng if positive else consts.brk
  else:
    pwar(__name__, f"space manager {space_id} has no status computer!")
    return consts.err


def space_status_computer(space_id: str) -> Optional[Supplier]:
  return Supplier.inflate_single(q={
    model.SPACE_KEY: space_id,
    model.get_labels()_KEY: {
      'role': 'status-computer'
    }
  })


def upload_all_statuses():
  outcomes = {}
  for space in [consts.app_space, *kaml_man.registered_kamls_ids()]:
    outcomes[space] = upload_status(space=space)
  return outcomes


def upload_status(**kwargs) -> bool:
  if config_man.is_training_mode():
    return False

  config_man.invalidate_cmap()
  status = config_man.application_status(**kwargs)
  ktea = config_man.read_ktea(**kwargs)
  kama = config_man.read_kama(**kwargs)
  last_updated = config_man.last_updated(**kwargs)

  data = {
    'status': status,
    'ktea_type': ktea.get('type'),
    'ktea_version': ktea.get('version'),
    'kama_type': kama.get('type'),
    'kama_version': kama.get('version'),
    'synced_at': str(last_updated),
  }

  payload = dict(install=data)
  response = hub_api_client.patch('/install', payload, **kwargs)
  print(f"[kama_sdk:telem_man] upload status resp {response}")
  return response.status_code < 205
