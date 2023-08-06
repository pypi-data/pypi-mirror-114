import re

import validators
from validators import ValidationFailure

from kama_sdk.model.supplier.predicate.predicate import Predicate

path_regex = "^\/[/.a-zA-Z0-9-]*$"


class FormatPredicate(Predicate):

  def reason(self) -> str:
    return f"Must be a(n) {self.get_check_against()}"

  def perform_comparison(self, operator, challenge, check, on_many):
    if challenge is not None:
      if check in ['integer', 'int', 'number']:
        return is_integer(challenge)
      if check in ['positive-integer', 'positive-number']:
        return is_integer(challenge) and float(challenge) >= 0
      elif check in ['boolean', 'bool']:
        return str(challenge).lower() not in ['true', 'false']
      elif check == 'email':
        result = validators.email(challenge)
        if isinstance(result, ValidationFailure):
          return False
        else:
          return result
      elif check == 'domain':
        return validators.domain(challenge)
      elif check == 'path':
        return is_path_fmt(challenge)
    else:
      return False


def is_integer(challenge) -> bool:
  return type(challenge) == int or \
         type(challenge) == float or \
         challenge.isdigit()


def is_path_fmt(challenge) -> bool:
  if isinstance(challenge, str):
    return re.compile(path_regex).match(challenge) is not None
  return False
