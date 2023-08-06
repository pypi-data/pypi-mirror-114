from flask import Blueprint, jsonify

from kama_sdk.controllers import ctrl_utils
from kama_sdk.core.core import job_client, updates_man, kaml_man

controller = Blueprint('releases_controller', __name__)

BASE_PATH = '/api/releases'


@controller.route(BASE_PATH)
def get_all_releases():
  spaces = ctrl_utils.space_id(False, False)
  if not spaces:
    spaces = ['app', *kaml_man.registered_kamls_ids()]
  releases = updates_man.fetch_all(spaces)
  return jsonify(data=releases or [])


@controller.route(f'{BASE_PATH}/next-available')
def fetch_next_available():
  update_or_none = updates_man.next_available()
  return jsonify(data=update_or_none)


@controller.route(f'{BASE_PATH}/<release_id>')
def show_update(release_id):
  space = ctrl_utils.space_id(True, True)
  if update := updates_man.fetch_update(release_id, space):
    return jsonify(data=update)
  else:
    return jsonify(error='release does not exist'), 400


@controller.route(f'{BASE_PATH}/<release_id>/preview')
def preview_update(release_id):
  space = ctrl_utils.space_id(True, True)
  if release := updates_man.fetch_update(release_id, space):
    preview_bundle = updates_man.preview(release, space)
    return jsonify(preview_bundle)
  else:
    return jsonify(error='release does not exist'), 400


@controller.route(f'{BASE_PATH}/<update_id>/apply', methods=['POST'])
def install_update(update_id):
  job_id = job_client.enqueue_action(
    'sdk.action.apply_update_e2e_action',
    update_id=update_id
  )
  return jsonify(data=(dict(job_id=job_id)))
