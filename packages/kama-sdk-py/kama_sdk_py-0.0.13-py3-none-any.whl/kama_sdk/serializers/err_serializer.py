from typing import Dict

from kama_sdk.model.error.diagnosis_actionable import DiagnosisActionable
from kama_sdk.model.error.error_diagnosis import ErrorDiagnosis


def ser_err_diagnosis(diagnosis: ErrorDiagnosis) -> Dict:
  actionables = list(map(ser_embedded_actionable, diagnosis.actionables()))

  return dict(
    id=diagnosis.get_id(),
    title=diagnosis.get_title(),
    info=diagnosis.get_info(),
    actionables=actionables,
  )


def ser_embedded_actionable(actionable: DiagnosisActionable) -> Dict:
  return dict(
    id=actionable.get_id(),
    title=actionable.get_title(),
    info=actionable.get_info(),
    operation_id=actionable.operation_id,

  )
