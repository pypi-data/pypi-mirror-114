from typing import Dict, List

import yaml
from werkzeug.utils import cached_property

from kama_sdk.core.core import config_man as cm, utils
from kama_sdk.core.core.config_man import config_man
from kama_sdk.core.core import config_man as cman_module
from kama_sdk.core.core.types import ErrCapture
from kama_sdk.model.action.base.action import Action
from kama_sdk.model.action.base.action_errors import FatalActionError


class PatchManifestVarsAction(Action):

  @cached_property
  def title(self) -> str:
    return super().title or f"Patch {self.target_key} values"

  @cached_property
  def info(self) -> str:
    return super().title or f"Merge new value into existing {self.target_key}"

  def values(self) -> Dict:
    return utils.flat2deep(self.get_prop(VALUES_KEY) or {})

  def target_key(self) -> str:
    return self.get_prop(TARGET_KEY_KEY, cm.user_vars_key)

  def perform(self) -> None:
    source_key = self.target_key()
    values = self.values()
    log = f"patching {self.config_space}/{source_key} with"
    self.add_logs([f"{log}", yaml.dump(values)])
    config_man.patch_into_deep_dict(
      source_key,
      values,
      **{cman_module.space_kwarg: self.config_space}
    )


class UnsetManifestVarsAction(Action):

  @cached_property
  def title(self) -> str:
    return super().title or f"Unset entries in {self.target_key}"

  @cached_property
  def info(self) -> str:
    return super().title or f"Delete entries from {self.target_key}, " \
                            f"allowing them to be overwritten"

  def target_key(self) -> str:
    return self.get_prop('target_key', cm.user_vars_key)

  def victim_keys(self) -> List[str]:
    return self.get_prop(VICTIM_KEYS_KEY, [])

  def perform(self) -> None:
    source_key = self.target_key()
    victim_keys = self.victim_keys()
    self.add_logs([f"unset {source_key}from  {victim_keys}"])
    config_man.unset_deep_vars(
      source_key,
      victim_keys,
      **{cman_module.space_kwarg: self.config_space}
    )


class WriteManifestVarsAction(Action):

  def values(self) -> Dict:
    return self.get_prop('values') or {}

  def source_key(self) -> str:
    return self.get_prop(TARGET_KEY_KEY)

  def perform(self) -> None:
    self.raise_if_illegal_source_key()
    config_man.write_typed_entry(
      self.source_key(),
      self.values(),
      **{cman_module.space_kwarg: self.config_space}
    )

  def raise_if_illegal_source_key(self):
    reason = None
    source_key = self.source_key()
    if not source_key:
      reason = "source key must be explicit for dangerous action"
    elif source_key not in cm.manifest_var_keys:
      reason = f"source key {source_key} not in {cm.manifest_var_keys}"

    if reason:
      raise FatalActionError(ErrCapture(
        type='write_manifest_action_illegal_key',
        reason=reason
      ))


TARGET_KEY_KEY = 'target_key'
VICTIM_KEYS_KEY = 'victim_keys'
VALUES_KEY = 'values'
