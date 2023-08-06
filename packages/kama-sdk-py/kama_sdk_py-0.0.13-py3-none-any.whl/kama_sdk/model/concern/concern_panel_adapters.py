from typing import List, Dict

from werkzeug.utils import cached_property

from kama_sdk.core.core.types import KoD
from kama_sdk.model.base.model import Model
from kama_sdk.model.concern.concern_attr_adapter import ConcernAttrAdapter
from kama_sdk.model.concern.concern_table import ConcernTableAdapter
from kama_sdk.model.concern.field_set import FieldSet
from kama_sdk.serializers import variables_ser
from kama_sdk.serializers.step_serial import ser_embedded_field


class ConcernPanelAdapter(Model):

  def compute_and_serialize(self) -> Dict:
    return {
      'id': self.get_id(),
      'title': self.get_title(),
      'info': self.get_info(),
      'naked': self.render_naked,
      'type': self.view_type(),
      'panel_options': self.panel_options
    }

  @cached_property
  def render_naked(self) -> bool:
    return self.get_attr(RENDER_NAKED_KEY, lookback=False)

  @cached_property
  def panel_options(self):
    return self.get_attr(PANEL_OPTIONS_KEY, lookback=0)

  @classmethod
  def view_type(cls):
    return None


class ConcernTablePanelAdapter(ConcernPanelAdapter):
  def table_adapter(self) -> ConcernTableAdapter:
    return self.inflate_child(
      ConcernTableAdapter,
      prop=TABLE_ADAPTER_KEY
    )

  def compute_and_serialize(self) -> Dict:
    table = self.table_adapter()
    return {
      **super(ConcernTablePanelAdapter, self).compute_and_serialize(),
      'columns': table.column_definitions,
      'data': table.one_shot_compute()
    }

  @classmethod
  def view_type(cls):
    return 'table'


class ConcernValuePanelAdapter(ConcernPanelAdapter):
  def compute_and_serialize(self) -> Dict:
    value = self.get_attr(VALUE_KEY, lookback=0, depth=100)
    return {
      **super(ConcernValuePanelAdapter, self).compute_and_serialize(),
      'value': value
    }

  @classmethod
  def view_type(cls):
    return 'value'


class ConcernAttrPanelAdapter(ConcernPanelAdapter):

  @cached_property
  def under_view_descriptor(self) -> Dict:
    return self.get_attr(UNDER_VIEW_DESC_KEY, depth=100)

  def attr_adapters(self) -> List[ConcernAttrAdapter]:
    return self.inflate_children(
      ConcernAttrAdapter,
      prop=ATTRS_ADAPTERS_KEY
    )

  def compute_and_serialize(self):
    attrs = self.attr_adapters()
    serialized = list(map(ser_concern_attr_meta, attrs))
    return {
      **super(ConcernAttrPanelAdapter, self).compute_and_serialize(),
      'attributes': serialized,
      'under': self.under_view_descriptor
    }

  @classmethod
  def view_type(cls):
    return 'attributes'


class ConcernFieldSetAdapter(ConcernPanelAdapter):

  @cached_property
  def field_set(self) -> FieldSet:
    return self.inflate_child(FieldSet, prop=FIELD_SET_KEY)

  def compute_and_serialize(self) -> Dict:
    field_set = self.field_set
    sered_fields = list(map(ser_embedded_field, field_set.fields))
    return {
      **super(ConcernFieldSetAdapter, self).compute_and_serialize(),
      'fields': sered_fields,
      'buttons': field_set.button_descriptors()
    }

  @classmethod
  def view_type(cls):
    return 'fields'


class AsyncPredicatesPanelAdapter(ConcernPanelAdapter):

  def predicate_kods(self) -> List[KoD]:
    return self.config.get('predicates') or []

  def compute_and_serialize(self) -> Dict:
    return {
      **super(AsyncPredicatesPanelAdapter, self).compute_and_serialize(),
      'predicates': self.predicate_kods()
    }

  @classmethod
  def view_type(cls):
    return 'async-predicates'


class ActionsPanelAdapter(ConcernPanelAdapter):
  def operations(self):
    from kama_sdk.model.operation.operation import Operation
    return self.inflate_children(Operation, prop='operations')

  def actions(self):
    from kama_sdk.model.action.base.action import Action
    return self.inflate_children(Action, prop='actions')

  def compute_and_serialize(self) -> Dict:
    return {
      **super(ActionsPanelAdapter, self).compute_and_serialize(),
      'operations': list(map(ser_action_like, self.operations())),
      'actions': list(map(ser_action_like, self.actions()))
    }

  @classmethod
  def view_type(cls):
    return 'actions'


class ManifestVariablesPanelAdapter(ConcernPanelAdapter):

  def variables(self):
    from kama_sdk.model.variable.manifest_variable import ManifestVariable
    return self.inflate_children(ManifestVariable, prop='variables')

  def compute_and_serialize(self) -> Dict:
    return {
      **super(ManifestVariablesPanelAdapter, self).compute_and_serialize(),
      'variables': list(map(variables_ser.full, self.variables()))
    }

  @classmethod
  def view_type(cls):
    return 'variables'


def ser_action_like(action) -> Dict:
  return {
    'id': action.get_id(),
    'title': action.get_title(),
    'info': action.get_info(),
    'space': action.get_space()
  }

def ser_concern_attr_meta(attr: ConcernAttrAdapter) -> Dict:
  value = attr.compute_value()
  return {
    'id': attr.get_id(),
    'title': attr.get_title(),
    'info': attr.get_info(),
    'label': attr.label,
    'value': value
  }


TABLE_ADAPTER_KEY = 'table_adapter'
ATTR_PANEL_DESCRIPTORS_KEY = 'attribute_panels'
ATTRS_ADAPTERS_KEY = 'attribute_adapters'
UNDER_VIEW_DESC_KEY = 'under'
FIELD_SET_KEY = 'field_set'
ACTION_KEY = 'action'
VALUE_KEY = 'value'
PANEL_OPTIONS_KEY = 'panel_options'
RENDER_NAKED_KEY = 'naked'
