from typing import Dict

from kama_sdk.model.base.model import Model


def ser_meta(model: Model) -> Dict:
  return {
    'id': model.id(),
    'title': model.title,
    'info': model.info
  }
