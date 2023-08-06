from typing import Dict

from cachetools.func import lru_cache
from k8kat.res.pod.kat_pod import KatPod
from kama_sdk.core.core import utils
from kama_sdk.model.action.base.action import Action
from kama_sdk.model.action.base.action_errors import FatalActionError
from werkzeug.utils import cached_property


class PodShellExecAction(Action):

  @cached_property
  def title(self) -> str:
    return "Execute command in shell pod"

  @cached_property
  def info(self) -> str:
    return "Execute command in shell pod"

  @lru_cache
  def command(self):
    return self.get_prop(CMD_KEY, '')

  @lru_cache
  def pod(self) -> KatPod:
    return self.resolve_prop(POD_KEY)

  def perform(self) -> Dict:
    if pod := self.pod():
      command = self.command()
      # print("FINAL COMMAND")
      # print(command)
      self.add_logs([command])
      result = pod.shell_exec(command)
      logs = utils.clean_log_lines(result)
      self.add_logs(logs)
      return dict(output=result)
    else:
      raise_on_pod_missing()


def raise_on_pod_missing():
  raise FatalActionError({
    'type': "no_pod_for_shell_exec",
    'reason': "Command could not be run as pod does not exist"
  })


POD_KEY = "pod"
CMD_KEY = 'command'
