from typing import Dict

from kama_sdk.model.action.base.action import Action


def serialize_std(action: Action) -> Dict:
  return dict(
    id=action.id(),
    title=action.title,
    info=action.info,
    tags=action.tags,
    space=action.space
  )
