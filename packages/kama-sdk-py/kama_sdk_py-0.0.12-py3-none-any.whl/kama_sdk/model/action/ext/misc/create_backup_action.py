from datetime import datetime

from kama_sdk.core.core.config_man import config_man
from kama_sdk.core.core.types import ErrCapture
from kama_sdk.core.telem import tabs_man
from kama_sdk.model.action.base.action import Action
from kama_sdk.model.action.base.action_errors import ActionError


class CreateBackupAction(Action):
  def perform(self) -> None:
    if tabs_man.supports_persistence():
      try:
        space = self.config_space or 'app'
        config = config_man.read_space(space=space)
        tabs_man.create_backup_record(dict(
          trigger='backup_action',
          space=space,
          config=config,
          timestamp=datetime.now()
        ))
      except Exception as e:
        raise ActionError(ErrCapture(
          name='Telem backend failure',
          reason=str(e),
          type='backup_telem_failure'
        ))
