from typing import List, TypeVar, Optional, Any

from werkzeug.utils import cached_property

from kama_sdk.core.core.types import PredEval
from kama_sdk.core.core.utils import any2bool, perr
from kama_sdk.model.base.model import Model
from kama_sdk.model.base.model_decorators import model_attr
from kama_sdk.model.input.generic_input import GenericInput
from kama_sdk.model.supplier.predicate import predicate as predicate_module
from kama_sdk.model.supplier.predicate.predicate import Predicate

T = TypeVar('T', bound='GenericVariable')

class GenericVariable(Model):

  @model_attr
  def get_default_value(self) -> Optional[Any]:
    default_value = self.get_attr(DEFAULT_VALUE_KEY)
    if default_value is None:
      if self.input_model:
        default_value = self.input_model.compute_inferred_default()
    return default_value

  @cached_property
  def input_model(self) -> GenericInput:
    return self.inflate_child(
      GenericInput,
      prop=INPUT_MODEL_KEY,
      safely=True
    ) or GenericInput({})

  def validation_predicates(self, value: Any) -> List[Predicate]:
    value = self.sanitize_for_validation(value)
    return self.inflate_children(
      Predicate,
      prop=VALIDATION_PREDS_KEY,
      resolve_kod=False,
      patches={
        predicate_module.CHALLENGE_KEY: value
      }
    )

  def validate(self, value: Any) -> PredEval:
    try:
      patched_predicates = self.validation_predicates(value)
      for predicate in patched_predicates:
        if not any2bool(predicate.resolve()):
          return PredEval(
            predicate_id=predicate.get_id(),
            met=False,
            reason=predicate.reason(),
            tone=predicate.tone()
          )
    except:
      perr(self, f"inflate/resolve failed for validators", True)
      return PredEval(
        met=False,
        tone='error',
        reason='error loading or running validator(s)'
      )
    return PredEval(
        met=True,
        tone='',
        reason=''
      )

  def current_or_default_value(self):
    return self.get_default_value()

  def sanitize_for_validation(self, value: Any) -> Any:
    return self.input_model.sanitize_for_validation(value)


DEFAULT_VALUE_KEY = 'default'
INPUT_MODEL_KEY = 'input'
VALIDATION_PREDS_KEY = 'validators'


COPYABLE_KEYS = [
  DEFAULT_VALUE_KEY,
  INPUT_MODEL_KEY,
  VALIDATION_PREDS_KEY
]
