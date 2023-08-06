from typing import List, Optional, Dict

from kama_sdk.core.core import utils, job_client
from kama_sdk.core.core.config_man import config_man
from kama_sdk.model.action.base import action
from kama_sdk.model.base import model
from kama_sdk.model.variable.configuration_preset import ConfigurationPreset
from kama_sdk.model.variable.manifest_variable import ManifestVariable


def ser_preset(preset: ConfigurationPreset, var_models: List[ManifestVariable]):
  assignments = preset.variables()
  flat_assigns = utils.deep2flat(assignments)

  def find_var(key: str) -> Optional[ManifestVariable]:
    disc = lambda _model: _model.id() == key
    return next(filter(disc, var_models), None)

  var_bundles = []
  for k, v in flat_assigns.items():
    var_model = find_var(k)
    var_bundles.append(dict(
      id=k,
      info=var_model.info if var_model else None,
      new_value=v,
      old_value=var_model.current_value(reload=False) if var_model else None
    ))

  return dict(
    id=preset.id(),
    title=preset.title,
    info=preset.info,
    variables=var_bundles
  )


def load_all(space: str):
  config_man.invalidate_cmap()
  presets = ConfigurationPreset.inflate_all(q=space_q(space))
  var_models = ManifestVariable.inflate_all(q=space_q(space))
  return [ser_preset(p, var_models) for p in presets]


def load_and_start_apply_job(preset_id: str, space: str, whitelist: List[str]):
  config_man.invalidate_cmap()
  preset = ConfigurationPreset.inflate(preset_id, q=space_q(space))

  if preset.is_default():
    assignments = {}
  else:
    flat_assigns: Dict = utils.deep2flat(preset.variables())
    if whitelist:
      flat_assigns = {k: v for k, v in flat_assigns.items() if k in whitelist}
    assignments = utils.flat2deep(flat_assigns)

  return job_client.enqueue_action(
    'sdk.action.safely_apply_application_manifest_e2e_action',
    values=assignments,
    **{action.TELEM_EVENT_TYPE_KEY: action.SET_VAR_EVENT_TYPE}
  )
  # return job_client.enqueue_action(
  #   {'kind': 'WaitAction', 'duration_seconds': 1},
  #   # values=assignments,
  #   **{action.TELEM_EVENT_TYPE_KEY: action.SET_VAR_EVENT_TYPE}
  # )


def space_q(space: str) -> Dict:
  return {model.SPACE_KEY: space}
