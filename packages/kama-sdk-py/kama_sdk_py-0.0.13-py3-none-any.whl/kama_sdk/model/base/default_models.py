def default_model_classes():
  from kama_sdk.model.supplier.base.misc_suppliers import FormattedDateSupplier
  from kama_sdk.model.variable.manifest_variable import ManifestVariable
  from kama_sdk.model.input.generic_input import GenericInput
  from kama_sdk.model.supplier.ext.misc.latest_vendor_injection_supplier import LatestVendorInjectionSupplier
  from kama_sdk.model.input.slider_input import SliderInput
  from kama_sdk.model.operation.operation import Operation
  from kama_sdk.model.operation.stage import Stage
  from kama_sdk.model.operation.step import Step
  from kama_sdk.model.operation.field import Field
  from kama_sdk.model.variable.generic_variable import GenericVariable
  from kama_sdk.model.supplier.ext.biz.resource_selector import ResourceSelector
  from kama_sdk.model.operation.operation_run_simulator import OperationRunSimulator
  from kama_sdk.model.action.base.multi_action import MultiAction
  from kama_sdk.model.input.checkboxes_input import CheckboxesInput
  from kama_sdk.model.input.checkboxes_input import CheckboxInput
  from kama_sdk.model.supplier.predicate.multi_predicate import MultiPredicate
  from kama_sdk.model.supplier.base.supplier import Supplier
  from kama_sdk.model.supplier.ext.misc.http_data_supplier import HttpDataSupplier
  from kama_sdk.model.supplier.ext.biz.resources_supplier import ResourcesSupplier
  from kama_sdk.model.input.checkboxes_input import SelectInput
  from kama_sdk.model.supplier.ext.misc.random_string_supplier import RandomStringSupplier
  from kama_sdk.model.supplier.ext.biz.config_supplier import ConfigSupplier
  from kama_sdk.model.action.base.action import Action
  from kama_sdk.model.humanizer.quantity_humanizer import QuantityHumanizer
  from kama_sdk.model.humanizer.cores_humanizer import CoresHumanizer
  from kama_sdk.model.humanizer.bytes_humanizer import BytesHumanizer
  from kama_sdk.model.action.ext.manifest.await_outkomes_settled_action import AwaitOutkomesSettledAction
  from kama_sdk.model.action.ext.manifest.await_predicates_settled_action import AwaitPredicatesSettledAction
  from kama_sdk.model.action.ext.manifest.kubectl_apply_action import KubectlApplyAction
  from kama_sdk.model.action.ext.manifest.template_manifest_action import TemplateManifestAction
  from kama_sdk.model.action.ext.update.update_actions import FetchUpdateAction
  from kama_sdk.model.action.ext.update.update_actions import CommitKteaFromUpdateAction
  from kama_sdk.model.action.ext.misc.run_predicates_action import RunPredicateAction
  from kama_sdk.model.action.ext.misc.run_predicates_action import RunPredicatesAction

  from kama_sdk.model.action.ext.misc.wait_action import WaitAction
  from kama_sdk.model.action.ext.misc.delete_resources_action import DeleteResourceAction
  from kama_sdk.model.action.ext.misc.delete_resources_action import DeleteResourcesAction
  from kama_sdk.model.action.ext.manifest.kubectl_dry_run_action import KubectlDryRunAction
  from kama_sdk.model.action.ext.misc.create_backup_action import CreateBackupAction
  from kama_sdk.model.supplier.base.props_supplier import PropsSupplier
  from kama_sdk.model.supplier.base.switch import Switch
  from kama_sdk.model.action.ext.update.fetch_latest_injection_action import FetchLatestInjectionsAction
  from kama_sdk.model.supplier.predicate.format_predicate import FormatPredicate
  from kama_sdk.model.supplier.predicate.common_predicates import TruePredicate
  from kama_sdk.model.supplier.predicate.common_predicates import FalsePredicate
  from kama_sdk.model.supplier.predicate.predicate import Predicate
  from kama_sdk.model.supplier.base.misc_suppliers import SumSupplier
  from kama_sdk.model.supplier.base.misc_suppliers import MergeSupplier
  from kama_sdk.model.supplier.base.misc_suppliers import ListFlattener
  from kama_sdk.model.supplier.base.misc_suppliers import ListPluck
  from kama_sdk.model.supplier.base.misc_suppliers import IfThenElse
  from kama_sdk.model.supplier.ext.misc.redactor import Redactor
  from kama_sdk.model.supplier.ext.vis.series_summary_supplier import SeriesSummarySupplier
  from kama_sdk.model.supplier.ext.vis.pod_statuses_supplier import PodStatusSummariesSupplier
  from kama_sdk.model.supplier.base.provider import Provider
  from kama_sdk.model.supplier.base.misc_suppliers import ListFilter
  from kama_sdk.model.concern.concern import Concern
  from kama_sdk.model.concern.concern_table import ConcernTableAdapter

  from kama_sdk.model.concern.concern_set import ConcernSetAdapter
  from kama_sdk.model.concern.concern_view_adapter import ConcernViewAdapter
  from kama_sdk.model.concern.concern_card_adapter import ConcernCardAdapter
  from kama_sdk.model.concern.concern_detail_adapter import ConcernDetailAdapter
  from kama_sdk.model.concern.concern_super_set import ConcernSuperSet
  from kama_sdk.model.concern.concern_grid import ConcernGridAdapter
  from kama_sdk.model.concern.concern_attr_adapter import ConcernAttrAdapter

  from kama_sdk.model.supplier.base.misc_suppliers import UnsetSupplier
  from kama_sdk.model.action.ext.manifest.manifest_var_actions import PatchManifestVarsAction
  from kama_sdk.model.action.ext.manifest.manifest_var_actions import WriteManifestVarsAction
  from kama_sdk.model.action.ext.manifest.manifest_var_actions import UnsetManifestVarsAction
  from kama_sdk.model.supplier.ext.misc.port_forward_spec_supplier import PortForwardSpecSupplier
  from kama_sdk.model.concern.monitoring_concern import MonitoringConcernCardAdapter
  from kama_sdk.model.supplier.ext.misc.quantity_humanization_supplier import QuantityHumanizationSupplier
  from kama_sdk.model.supplier.ext.misc.percentage_supplier import PercentageSupplier

  from kama_sdk.model.concern.concern_panel_adapters import ConcernPanelAdapter
  from kama_sdk.model.concern.concern_panel_adapters import ConcernTablePanelAdapter
  from kama_sdk.model.concern.concern_panel_adapters import ConcernValuePanelAdapter
  from kama_sdk.model.concern.concern_panel_adapters import ConcernAttrPanelAdapter
  from kama_sdk.model.concern.concern_panel_adapters import ConcernFieldSetAdapter
  from kama_sdk.model.concern.field_set import FieldSet
  from kama_sdk.model.supplier.ext.biz.image_src_supplier import ImageSrcSupplier
  from kama_sdk.model.supplier.ext.biz.preset_assignments_supplier import PresetAssignmentsSupplier
  from kama_sdk.model.variable.variable_category import VariableCategory
  from kama_sdk.model.input.checkboxes_input import OnOffInput
  from kama_sdk.model.supplier.ext.biz.multi_kind_resource_selector import MultiKindResourceSelector
  from kama_sdk.model.supplier.ext.misc.fresh_defaults_supplier import FreshDefaultsSupplier
  from kama_sdk.model.supplier.ext.misc.timeseries_aggregation_supplier import TimeseriesAggregationSupplier
  from kama_sdk.model.supplier.ext.misc.vars2attr_adapters import Vars2AttrAdaptersSupplier
  from kama_sdk.model.supplier.base.props_supplier import SelfSupplier
  from kama_sdk.model.supplier.base.consts_supplier import Consts
  from kama_sdk.model.supplier.base.props_supplier import DelayedInflateSupplier
  from kama_sdk.model.supplier.ext.misc.resource_count_predicate import ResourceCountPredicate
  from kama_sdk.model.variable.manifest_variable_dependency import ManifestVariableDependency
  from kama_sdk.model.variable.configuration_preset import ConfigurationPreset
  from kama_sdk.model.supplier.ext.biz.config_supplier import MergedVariablesSupplier
  from kama_sdk.model.supplier.ext.biz.config_supplier import DefaultVariablesSupplier
  from kama_sdk.model.concern.concern_panel_adapters import AsyncPredicatesPanelAdapter
  from kama_sdk.model.concern.concern_panel_adapters import ActionsPanelAdapter
  from kama_sdk.model.concern.concern_panel_adapters import ManifestVariablesPanelAdapter
  from kama_sdk.model.supplier.ext.misc.pod_shell_exec_supplier import PodShellExecOutputSupplier
  from kama_sdk.model.action.ext.misc.pod_shell_exec_action import PodShellExecAction
  from kama_sdk.model.supplier.base.misc_suppliers import JoinSupplier
  from kama_sdk.model.supplier.ext.misc.site_access_node import SiteAccessNode
  from kama_sdk.model.supplier.ext.misc.site_access_node import SimpleIngressSiteAccessNode
  from kama_sdk.model.supplier.ext.misc.site_access_node import SimpleServiceSiteAccessNode
  from kama_sdk.model.supplier.ext.misc.site_access_node import BestSiteEndpointSupplier
  from kama_sdk.model.supplier.ext.misc.site_access_node import SiteAccessNodesSerializer
  from kama_sdk.model.error.action_error_remediation_option import ActionErrorRemediationOption
  return [
    Operation,
    Stage,
    Step,
    Field,

    VariableCategory,
    GenericVariable,
    ManifestVariable,
    ManifestVariableDependency,
    ResourceSelector,
    MultiKindResourceSelector,
    ConfigurationPreset,

    GenericInput,
    SliderInput,
    SelectInput,
    CheckboxesInput,
    CheckboxInput,
    OnOffInput,

    Predicate,
    FormatPredicate,
    MultiPredicate,
    TruePredicate,
    FalsePredicate,
    ActionErrorRemediationOption,

    Supplier,
    Consts,
    SelfSupplier,
    DelayedInflateSupplier,
    Provider,
    PropsSupplier,
    Vars2AttrAdaptersSupplier,
    FormattedDateSupplier,
    MergedVariablesSupplier,
    DefaultVariablesSupplier,
    ResourceCountPredicate,
    Switch,
    PodShellExecOutputSupplier,
    MergeSupplier,
    UnsetSupplier,
    HttpDataSupplier,
    ResourcesSupplier,
    FreshDefaultsSupplier,
    RandomStringSupplier,
    ConfigSupplier,
    SumSupplier,
    LatestVendorInjectionSupplier,
    ListFlattener,
    ListFilter,
    ListPluck,
    IfThenElse,
    Redactor,

    ImageSrcSupplier,
    QuantityHumanizationSupplier,
    PercentageSupplier,
    JoinSupplier,
    PortForwardSpecSupplier,
    PresetAssignmentsSupplier,
    TimeseriesAggregationSupplier,

    SeriesSummarySupplier,
    PodStatusSummariesSupplier,

    SiteAccessNode,
    SimpleIngressSiteAccessNode,
    SimpleServiceSiteAccessNode,
    BestSiteEndpointSupplier,
    SiteAccessNodesSerializer,

    Action,
    MultiAction,
    RunPredicateAction,
    RunPredicatesAction,
    WaitAction,

    FetchLatestInjectionsAction,
    AwaitOutkomesSettledAction,
    AwaitPredicatesSettledAction,

    DeleteResourceAction,
    DeleteResourcesAction,
    KubectlDryRunAction,
    CreateBackupAction,
    PodShellExecAction,

    KubectlApplyAction,
    TemplateManifestAction,
    FetchUpdateAction,
    CommitKteaFromUpdateAction,

    PatchManifestVarsAction,
    WriteManifestVarsAction,
    UnsetManifestVarsAction,

    Concern,
    ConcernSuperSet,
    ConcernSetAdapter,
    ConcernTableAdapter,
    ConcernGridAdapter,
    ConcernViewAdapter,
    ConcernCardAdapter,
    AsyncPredicatesPanelAdapter,
    ManifestVariablesPanelAdapter,
    ActionsPanelAdapter,
    ConcernDetailAdapter,
    ConcernAttrAdapter,
    ConcernPanelAdapter,
    ConcernTablePanelAdapter,
    ConcernValuePanelAdapter,
    ConcernAttrPanelAdapter,
    ConcernFieldSetAdapter,
    FieldSet,

    MonitoringConcernCardAdapter,

    QuantityHumanizer,
    BytesHumanizer,
    CoresHumanizer,

    OperationRunSimulator
  ]
