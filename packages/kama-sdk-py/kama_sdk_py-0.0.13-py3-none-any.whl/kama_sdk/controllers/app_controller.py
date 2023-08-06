from flask import Blueprint, jsonify

from kama_sdk.controllers import ctrl_utils
from kama_sdk.controllers.ctrl_utils import parse_json_body
from kama_sdk.core.core import job_client, presets_man, status_man
from kama_sdk.core.core.config_man import config_man
from kama_sdk.model.base import pure_provider_ids
from kama_sdk.model.supplier.base.provider import Provider

controller = Blueprint('app_controller', __name__)

BASE_PATH = '/api/app'


@controller.route(f'{BASE_PATH}/presets', methods=['GET', 'POST'])
def list_presets():
  space = ctrl_utils.space_id(True, True)
  serialized_presets = presets_man.load_all(space)
  return jsonify(data=serialized_presets)


@controller.route(f'{BASE_PATH}/presets/<_id>/commit-apply', methods=['POST'])
def commit_apply_preset(_id: str):
  space = ctrl_utils.space_id(True, True)
  if whitelist := parse_json_body().get('whitelist'):
    job_id = presets_man.load_and_start_apply_job(_id, space, whitelist)
    return jsonify(job_id=job_id)
  else:
    return jsonify(error='whitelist empty/absent'), 400


@controller.route(f'{BASE_PATH}/run-installation-preflight', methods=['POST'])
def run_global_preflight():
  action_id = "action.predicate.install-preflight"
  job_id = job_client.enqueue_action(action_id)
  return jsonify(data={'job_id': job_id})


@controller.route(f'{BASE_PATH}/compute-and-sync-statuses', methods=['POST'])
def compute_and_sync_status():
  statuses = status_man.compute_all_statuses()
  config_man.write_space_statuses(statuses)
  status_man.upload_all_statuses()
  return jsonify(statuses=statuses)


@controller.route(f'{BASE_PATH}/sync-status-hub', methods=['POST'])
def sync_status_hub():
  outcomes = status_man.upload_all_statuses()
  return jsonify(success=outcomes.get('app'))


@controller.route(f'{BASE_PATH}/uninstall-spec')
def uninstall_victims():
  spec_id = pure_provider_ids.deletion_spec_id
  provider: Provider = Provider.inflate(spec_id)
  spec = provider.resolve() if provider else None
  return jsonify(data=spec)


@controller.route(f'{BASE_PATH}/master_config')
def get_master_config():
  space = ctrl_utils.space_id(True, True)
  return jsonify(data=config_man.read_space(space=space))


@controller.route(f'{BASE_PATH}/deletion_selectors')
def deletion_selectors():
  deletion_map = 3
  return jsonify(data=deletion_map)


@controller.route(f'{BASE_PATH}/jobs/<job_id>/status')
def job_progress(job_id):
  status_wrapper = job_client.job_status(job_id)
  return jsonify(
    data=dict(
      status=status_wrapper.status(),
      progress=status_wrapper.progress_bundle,
      result=status_wrapper.result
    )
  )
