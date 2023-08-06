from typing import Dict, List

import yaml

from kama_sdk.core.core import config_man as cm, utils
from kama_sdk.core.core import config_man as cman_module
from kama_sdk.core.core.config_man import config_man
from kama_sdk.core.core.types import ErrCapture
from kama_sdk.model.action.base.action import Action
from kama_sdk.model.action.base.action_errors import FatalActionError
from kama_sdk.model.base.model_decorators import model_attr


class PatchManifestVarsAction(Action):

  def get_title(self) -> str:
    return super().get_title() or f"Patch {self.target_key} values"

  def get_info(self) -> str:
    return super().get_title() or f"Merge new value into existing {self.target_key}"

  def values(self) -> Dict:
    return utils.flat2deep(self.get_attr(VALUES_KEY) or {})

  @model_attr
  def target_key(self) -> str:
    return self.get_attr(TARGET_KEY_KEY, cm.user_vars_key)

  def perform(self) -> None:
    source_key = self.target_key()
    values = self.values()
    log = f"patching {self.get_config_space()}/{source_key} with"
    self.add_logs([f"{log}", yaml.dump(values)])
    config_man.patch_into_deep_dict(
      source_key,
      values,
      **{cman_module.space_kwarg: self.get_config_space()}
    )


class UnsetManifestVarsAction(Action):

  def get_title(self) -> str:
    entry_key = self.get_entry_key()
    return super().get_title() or f"Unset entries in {entry_key}"

  def get_info(self) -> str:
    if explicit := super().get_title():
      return explicit
    else:
      entry_key = self.get_entry_key()
      return f"Delete entries from {entry_key}, " \
             f"allowing them to be overwritten"

  @model_attr
  def get_entry_key(self) -> str:
    return self.get_attr(TARGET_KEY_KEY, backup=cm.user_vars_key)

  @model_attr
  def victim_keys(self) -> List[str]:
    return self.get_attr(VICTIM_KEYS_KEY, [])

  def perform(self) -> None:
    self.victim_keys()
    source_key = self.get_entry_key()
    victim_keys = self.victim_keys()
    self.add_logs([f"unset {source_key}from  {victim_keys}"])
    config_man.unset_deep_vars(
      source_key,
      victim_keys,
      **{cman_module.space_kwarg: self.get_config_space()}
    )


class WriteManifestVarsAction(Action):

  def values(self) -> Dict:
    return self.get_attr(VALUES_KEY) or {}

  @model_attr
  def get_entry_key(self) -> str:
    return self.get_attr(TARGET_KEY_KEY)

  def perform(self) -> None:
    self.raise_if_illegal_source_key()
    config_man.write_typed_entry(
      self.get_entry_key(),
      self.values(),
      **{cman_module.space_kwarg: self.get_config_space()}
    )

  def raise_if_illegal_source_key(self):
    reason = None
    source_key = self.get_entry_key()
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
