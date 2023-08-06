from datetime import datetime
from typing import List, Dict, Any, Optional
from dateutil.parser import parse as parse_date
from werkzeug.utils import cached_property

from kama_sdk.core.core import utils
from kama_sdk.model.supplier.base.supplier import Supplier


class SumSupplier(Supplier):
  def _compute(self) -> float:
    values = self.source_data()
    cleanser = lambda val: float(val or 0)
    return sum(map(cleanser, values))


class ListFlattener(Supplier):
  def _compute(self) -> List:
    source = self.source_data()
    cleaner = lambda raw: raw if utils.listlike(raw) else [raw]
    return utils.flatten(list(map(cleaner, source)))


class ListFilter(Supplier):

  def predicate(self):
    from kama_sdk.model.supplier.predicate.predicate import Predicate
    return self.inflate_child(
      Predicate,
      prop='predicate',
      resolve_kod=False
    )

  @staticmethod
  def decide_sub_item(_predicate, sub_item: Any) -> bool:
    from kama_sdk.model.supplier.predicate.predicate import Predicate
    typed_predicate: Predicate = _predicate
    from kama_sdk.model.supplier.predicate import predicate
    primed_predicate: Predicate = typed_predicate.clone().patch({
      'subject': sub_item,
      predicate.CHALLENGE_KEY: sub_item
    })
    return primed_predicate.resolve()

  def _compute(self) -> List[Any]:
    if predicate := self.predicate():
      filterer = lambda item: self.decide_sub_item(predicate, item)
      return list(filter(filterer, self.source_data()))
    else:
      return []


class ListPluck(Supplier):

  def make_flat(self) -> bool:
    return self.get_prop('flat', False)

  def resolve(self) -> List[Any]:
    included = []
    for it in self._compute():
      predicate_kod, value = it.get('include'), it.get('value')
      predicate_outcome = self.resolve_prop_value(predicate_kod)
      if utils.any2bool(predicate_outcome):
        if self.make_flat() and utils.listlike(value):
          included += value
        else:
          included.append(value)
    return included


class JoinSupplier(Supplier):

  def items(self) -> List:
    items = self.resolve_prop("items", lookback=False, backup=[])
    if isinstance(items, list):
      return items
    else:
      utils.pwar(self, f"{items} is {type(items)}, not list, return []")
      return []

  def separator(self) -> str:
    return self.resolve_prop("separator", lookback=False, backup=',')

  def _compute(self) -> str:
    if items := self.items():
      return self.separator().join(items)
    else:
      return ""


class MergeSupplier(Supplier):

  def source_data(self) -> List[Dict]:
    dicts = super(MergeSupplier, self).source_data()
    return [d or {} for d in dicts]

  def _compute(self) -> Any:
    result = utils.deep_merge(*self.source_data())
    return result


class UnsetSupplier(Supplier):

  def victim_keys(self) -> List[str]:
    return self.get_prop('victim_keys', [])

  def _compute(self) -> Any:
    victim_keys = self.victim_keys()
    source_dict = self.source_data() or {}
    return utils.deep_unset(source_dict, victim_keys)


class FormattedDateSupplier(Supplier):

  def source_data(self) -> Optional[datetime]:
    value = super(FormattedDateSupplier, self).source_data()
    parse = lambda: parse_date(value)
    return utils.safely(parse) if type(value) == str else value

  @cached_property
  def output_format(self):
    return super().output_format or "%b %d at %I:%M%p %Z"

  def resolve(self) -> Any:
    source = self.source_data()
    if type(source) == datetime:
      return source.strftime(self.output_format)
    else:
      return None

class IfThenElse(Supplier):

  def on_true(self) -> Any:
    return self.resolve_prop('if_true')

  def on_false(self) -> Any:
    return self.resolve_prop('if_false')

  def _compute(self) -> Any:
    resolved_to_truthy = self.resolve_prop('source', lookback=False)
    return self.on_true() if resolved_to_truthy else self.on_false()
