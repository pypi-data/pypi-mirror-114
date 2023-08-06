import json
from datetime import datetime
from functools import lru_cache
from typing import Dict, Any, List, Optional, TypeVar

from inflection import underscore
from rq import get_current_job
from rq.job import Job
from werkzeug.utils import cached_property

from kama_sdk.core.core import utils, consts, job_client
from kama_sdk.core.core.types import ActionStatusDict, ErrCapture, EventCapture
from kama_sdk.core.core.utils import perr
from kama_sdk.core.telem import tabs_man
from kama_sdk.model.action.base.action_errors import ActionErrOrException, ActionError
from kama_sdk.model.base.model import Model
from kama_sdk.model.error.action_error_remediation_option import ActionErrorRemediationOption

T = TypeVar('T', bound='Action')

RemOption = ActionErrorRemediationOption

class Action(Model):

  status: str
  err_capture: Optional[ErrCapture]
  telem_vid: str
  logs: List[str]

  def __init__(self, config: Dict):
    super().__init__(config)
    self.status = 'idle'
    self.logs = []
    self.err_capture = None
    self.telem_vid = utils.gen_uuid()

  def run(self) -> Any:
    outcome: Optional[Any]
    exception: Optional[Exception]
    err_capture: Optional[ErrCapture] = None
    should_raise: bool = False

    try:
      self.set_running()
      outcome = self.perform()
      exception = None
    except Exception as _exception:
      perr(self, "Action runtime exception", True)
      outcome = None
      exception = _exception

    if exception:
      status = consts.neg
      err_capture = exception2capture(self.telem_vid, exception)
      should_raise = err_capture['fatal']
      self.add_logs(err_capture.get('logs'))
    else:
      status = consts.pos

    self.err_capture = err_capture
    self.set_status(status)
    self.handle_telem()

    if should_raise:
      raise ActionError(err_capture, is_original=False)

    return outcome

  def parent_telem_event_id(self):
    return self.get_attr(KEY_PARENT_EVENT_VID)

  def get_event_type(self):
    return self.get_attr(
      TELEM_EVENT_TYPE_KEY,
      lookback=0,
      backup=DEFAULT_EVENT_TYPE
    )

  @lru_cache
  def get_debug_attr_keys(self) -> List[str]:
    return self.get_attr(DEBUG_PROPS_KEY, backup=[])

  @cached_property
  def telem_enabled(self) -> List[str]:
    return self.get_attr(TELEM_ENABLED_KEY, backup=True)

  def gen_backup_event_name(self):
    return underscore(self.__class__.__name__)

  def handle_telem(self):
    tabs_man.handle_event(self.gen_telem_bundle())

    if self.err_capture and self.err_capture['is_original']:
      # print("-----MOVE ERR TO FLASH")
      # print(self.err_capture)
      tabs_man.handle_error(self.err_capture)

    if self.am_root_action():
      if not utils.is_test():
        job_client.enqueue_telem_func(tabs_man.flush_flash)

  def gen_telem_bundle(self) -> EventCapture:
    parent_action = self.parent_action()
    parent_vid = parent_action.telem_vid if parent_action else None
    return EventCapture(
      vid=self.telem_vid,
      parent_vid=parent_vid,
      type=self.get_event_type(),
      name=self.get_id() or self.gen_backup_event_name(),
      status=self.status,
      logs=self.logs,
      occurred_at=str(datetime.now())
    )

  def set_running(self):
    self.set_status(consts.rng)

  def set_positive(self):
    self.set_status(consts.pos)

  def set_negative(self):
    self.set_status(consts.neg)

  def set_status(self, status):
    assert status in consts.statuses
    self.status = status
    self.notify_job()

  def perform(self) -> Optional[Dict]:
    raise NotImplementedError

  def add_logs(self, new_logs: Optional[List[str]]) -> None:
    new_logs = new_logs or []
    self.logs = [*self.logs, *new_logs]

  def parent_action(self) -> Optional[T]:
    if self.parent:
      if issubclass(self.parent.__class__, Action):
        return self.parent
    return None

  def am_sub_action(self) -> bool:
    return issubclass(self.parent.__class__, Action)

  def am_root_action(self):
    return not self.am_sub_action()

  def find_root_action(self) -> Optional:
    if self.am_root_action():
      return self
    elif parent_action := self.parent_action():
      return parent_action.find_root_action()
    else:
      return None

  def notify_job(self):
    job: Job = get_current_job()
    if job:
      action_root = self.find_root_action()
      if action_root:
        progress_bundle = action_root.serialize_progress()
        job.meta['progress'] = json.dumps(progress_bundle)
        job.save_meta()
      else:
        print(f"[action:{self.get_id}] danger root not found")

  def gen_debug_dump(self) -> Dict:
    bundle = {}
    for attr_name in self.get_debug_attr_keys():
      try:
        bundle[attr_name] = self.get_attr(attr_name)
      except RuntimeError as e:
        bundle[attr_name] = f"[error] {str(e)}"
    return bundle

  def serialize_progress(self) -> ActionStatusDict:
    return dict(
      id=self.get_id(),
      title=self.get_title(),
      info=self.get_info(),
      status=self.status,
      sub_items=[],
      logs=self.logs,
      debug=self.gen_debug_dump(),
      error=err2client_facing(self.err_capture)
    )

  @cached_property
  def expected_run_args(self) -> List[str]:
    return self.get_attr(EXPECTED_RUN_ARGS_KEY, backup=[])


def err2client_facing(err_capt: ErrCapture) -> Optional[Dict]:
  if err_capt:
    return dict(
      fatal=err_capt.get('fatal', True),
      type=err_capt.get('type') or 'unknown_type',
      name=err_capt.get('name'),
      reason=err_capt.get('reason') or 'Unknown Reason',
      logs=err_capt.get('logs', []),
      remediation_options=serialize_remediation_options(err_capt)
    )
  else:
    return None


def serialize_remediation_options(err_capture: ErrCapture) -> List[Dict]:
  rems: List[RemOption] = RemOption.matching_error_capture(err_capture)
  return [rem.serialize_for_client() for rem in rems]


def exception2capture(vid: str, exception: ActionErrOrException) -> ErrCapture:
  err_capture: Optional[ErrCapture] = None

  if issubclass(exception.__class__, ActionError):
    err_capture = exception.err_capture

  if not err_capture:
    err_capture = ErrCapture(
      fatal=True,
      name=exception.__class__.__name__,
      reason=str(exception),
      logs=utils.exception2trace(exception)
    )

  if not err_capture.get('type'):
    err_capture['type'] = 'internal_error'

  if not err_capture.get('name'):
    err_capture['name'] = exception.__class__.__name__

  if 'is_original' not in err_capture.keys():
    err_capture['is_original'] = True

  err_capture['occurred_at'] = str(datetime.now())

  err_capture['event_vid'] = vid
  return err_capture


DEBUG_PROPS_KEY = 'debug_props'
TELEM_ENABLED_KEY = 'telem'
TELEM_PROPS_KEY = 'telem_props'
ERROR_TELEM_PROPS_KEY = 'error_telem_props'
ERROR_TELEM_KEY = 'error_telem'
TELEM_EVENT_TYPE_KEY = 'telem_type'

KEY_PARENT_EVENT_VID = 'parent_event_virtual_id'
KEY_PARENT_EVENT_ID = 'parent_event_id'
EXPECTED_RUN_ARGS_KEY = 'expects_run_args'

DEFAULT_EVENT_TYPE = 'action'
OP_STEP_EVENT_TYPE = 'operation_step'
PREFLIGHT_EVENT_TYPE = 'preflight_check'
SYS_CHECK_EVENT_TYPE = 'system_check'
SET_VAR_EVENT_TYPE = 'set_var'
UNSET_VAR_EVENT_TYPE = 'unset_var'
