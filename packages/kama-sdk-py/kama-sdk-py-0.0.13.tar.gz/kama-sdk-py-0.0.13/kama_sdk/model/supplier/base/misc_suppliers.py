from datetime import datetime
from typing import List, Dict, Any, Optional
from dateutil.parser import parse as parse_date
from werkzeug.utils import cached_property

from kama_sdk.core.core import utils
from kama_sdk.model.supplier.base.supplier import Supplier


class SumSupplier(Supplier):
  def _compute(self) -> float:
    values = self.get_source_data()
    cleanser = lambda val: float(val or 0)
    return sum(map(cleanser, values))


class ListFlattener(Supplier):
  def _compute(self) -> List:
    source = self.get_source_data()
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
      return list(filter(filterer, self.get_source_data()))
    else:
      return []


class ListPluck(Supplier):

  def make_flat(self) -> bool:
    return self.get_attr('flat', False)

  def resolve(self) -> List[Any]:
    included = []
    for it in self._compute():
      predicate_kod, value = it.get('include'), it.get('value')
      predicate_outcome = self.get_attr_value(predicate_kod)
      if utils.any2bool(predicate_outcome):
        if self.make_flat() and utils.listlike(value):
          included += value
        else:
          included.append(value)
    return included


class JoinSupplier(Supplier):

  def items(self) -> List:
    items = self.get_attr("items", lookback=False, backup=[])
    if isinstance(items, list):
      return items
    else:
      utils.pwar(self, f"{items} is {type(items)}, not list, return []")
      return []

  def separator(self) -> str:
    return self.get_attr("separator", lookback=False, backup=',')

  def _compute(self) -> str:
    if items := self.items():
      return self.separator().join(items)
    else:
      return ""


class MergeSupplier(Supplier):

  def get_source_data(self) -> List[Dict]:
    dicts = super(MergeSupplier, self).get_source_data()
    return [d or {} for d in dicts]

  def _compute(self) -> Any:
    result = utils.deep_merge(*self.get_source_data())
    return result


class UnsetSupplier(Supplier):

  def victim_keys(self) -> List[str]:
    return self.get_attr('victim_keys', [])

  def _compute(self) -> Any:
    victim_keys = self.victim_keys()
    source_dict = self.get_source_data() or {}
    return utils.deep_unset(source_dict, victim_keys)


class FormattedDateSupplier(Supplier):

  def get_source_data(self) -> Optional[datetime]:
    value = super(FormattedDateSupplier, self).get_source_data()
    parse = lambda: parse_date(value)
    return utils.safely(parse) if type(value) == str else value

  def get_output_format(self):
    return super().get_output_format() or "%b %d at %I:%M%p %Z"

  def resolve(self) -> Any:
    source = self.get_source_data()
    if type(source) == datetime:
      return source.strftime(self.get_output_format())
    else:
      return None

class IfThenElse(Supplier):

  def on_true(self) -> Any:
    return self.get_attr('if_true')

  def on_false(self) -> Any:
    return self.get_attr('if_false')

  def _compute(self) -> Any:
    resolved_to_truthy = self.get_attr('source', lookback=False)
    return self.on_true() if resolved_to_truthy else self.on_false()
