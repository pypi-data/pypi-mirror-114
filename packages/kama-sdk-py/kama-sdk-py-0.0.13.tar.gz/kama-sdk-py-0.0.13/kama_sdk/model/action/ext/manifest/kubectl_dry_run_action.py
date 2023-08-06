from typing import Dict, List

from kama_sdk.core.core.types import ErrCapture
from kama_sdk.core.ktea.ktea_client import KteaClient
from kama_sdk.model.action.base.action import Action
from kama_sdk.model.action.base.action_errors import FatalActionError


class KubectlDryRunAction(Action):

  def res_descs(self) -> List[Dict]:
    return self.get_attr('res_descs', backup=[])

  def perform(self) -> None:
    res_descs = self.res_descs()
    raise_if_res_descs_none(res_descs)
    if len(res_descs) > 0:
      success, logs = KteaClient.kubectl_dry_run(res_descs)
      self.add_logs(logs)
      raise_on_dry_run_err(success, logs)
    else:
      self.add_logs(['WARN zero resources passed to kubectl'])


def raise_on_dry_run_err(success: bool, logs):
  if not success:
    raise FatalActionError(ErrCapture(
      type='kubectl_dry_run_failed',
      name=f"manifest was rejected",
      reason='kubectl dry_run failed for one or more resource.',
      logs=logs
    ))


def raise_if_res_descs_none(res_descs: List[Dict]):
  if res_descs is None:
    raise FatalActionError(ErrCapture(
      type='kubectl_apply',
      name='res_descs undefined',
      reason='action does not know what to pass to kubectl',
      logs=['res_descs undefined']
    ))
