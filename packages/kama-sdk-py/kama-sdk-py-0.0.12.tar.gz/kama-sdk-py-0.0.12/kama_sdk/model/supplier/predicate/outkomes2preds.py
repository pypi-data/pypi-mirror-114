from typing import List, Optional

from kama_sdk.core.core import utils, consts
from kama_sdk.core.core.types import KAO
from kama_sdk.model.base import model
from kama_sdk.model.supplier.ext.biz import resources_supplier as res_sup
from kama_sdk.model.supplier.ext.biz import resource_selector as res_sel
from kama_sdk.model.supplier.base import supplier as sup
from kama_sdk.model.supplier.predicate.predicate import Predicate
from kama_sdk.model.supplier.predicate import predicate as pred


def outkome_discriminator(outkome: Optional[KAO]) -> bool:
  return outkome and not outkome.get('verb') == 'unchanged'


def outkomes2preds(outkomes: List[KAO]) -> List[Predicate]:
  predicates = dict(positive=[], negative=[])
  for ktl_outcome in list(filter(outkome_discriminator, outkomes)):
    if not ktl_outcome['verb'] == 'unchanged':
      for charge in [consts.pos, consts.neg]:
        predicate = outkome2charged_pred(ktl_outcome, charge)
        predicates[charge].append(predicate)
  return utils.flatten(predicates.values())


def outkome2charged_pred(ktl_out: KAO, charge):
  from kama_sdk.model.supplier.ext.biz.resources_supplier import ResourcesSupplier

  kind = ktl_out.get('kind')
  name = ktl_out.get('name')

  selector = {
    res_sel.RES_KIND_KEY: kind,
    res_sel.RES_NAME_KEY: name,
    'api_group': ktl_out['api_group']
  }

  word = "settled" if charge == consts.pos else 'broken'
  check_part = f"Check {word}: {kind}/{name}.status"
  challenge_part = f"${{get::props {pred.RESOLVED_CHALLENGE_KEY}}}"
  whole = f"{check_part} = {challenge_part}"

  return Predicate({
    model.KIND_KEY: Predicate.__name__,
    model.ID_KEY: f"{kind}/{name}-{charge}",
    model.TITLE_KEY: f"{kind}/{name} is {charge}",
    pred.CHECK_AGAINST_KEY: charge,
    pred.IS_OPTIMISTIC_KEY: charge == consts.pos,
    pred.OPERATOR_KEY: '=',
    pred.ON_MANY_KEY: 'each_true',
    pred.EXPLAIN_KEY: whole,
    pred.CHALLENGE_KEY: {
      model.KIND_KEY: ResourcesSupplier.__name__,
      sup.OUTPUT_FMT_KEY: 'ternary_status',
      sup.SERIALIZER_KEY: 'legacy',
      sup.IS_MANY_KEY: True,
      res_sup.RESOURCE_SELECTOR_KEY: selector
    },
    pred.ERROR_EXTRAS_KEY: dict(
      resource_signature=dict(kind=kind, name=name),
      resource={
        model.KIND_KEY: ResourcesSupplier.__name__,
        res_sup.RESOURCE_SELECTOR_KEY: selector,
        sup.IS_MANY_KEY: False
      }
    )})
