from __future__ import annotations

import inspect
import os
from copy import deepcopy

from os.path import isfile
from typing import Type, Optional, Dict, Union, List, TypeVar, Any, Tuple, Callable

import yaml
# noinspection PyUnresolvedReferences
from typing_extensions import TypedDict
from werkzeug.utils import cached_property, invalidate_cached_property

from kama_sdk.core.core import utils, consts, str_sub, structured_search
from kama_sdk.core.core.types import KoD
from kama_sdk.core.core.utils import perr, pwar
from kama_sdk.core.telem.telem_backend import TelemBackend
from kama_sdk.model.base import model_decorators
from kama_sdk.model.base.default_models import default_model_classes
from kama_sdk.model.base.exceptions import InflateModelError
from kama_sdk.model.base.model_decorators import ModelCacheApi

T = TypeVar('T', bound='Model')


ConfigLookup = Tuple[bool, Any]


class ModelsMan:
  _descriptors: List[Dict]
  _classes: List[Type[T]]
  _asset_paths: List[str]
  _telem_backend: Optional[TelemBackend]

  def __init__(self):
    self._descriptors = []
    self._classes = []
    self._asset_paths = []
    self._telem_backend = None

  def add_descriptors(self, descriptors: List[Dict]):
    self.add_any_descriptors(descriptors, consts.app_space)

  def add_any_descriptors(self, descriptors: List[Dict], space=None):
    for descriptor in descriptors:
      if isinstance(descriptor, dict):

        if descriptor.get(LABELS_KEY) is None:
          descriptor[LABELS_KEY] = {}

        if space:
          if not descriptor.get(SPACE_KEY):
            descriptor[SPACE_KEY] = space

          if not descriptor.get(CONFIG_SPACE_KEY):
            descriptor[CONFIG_SPACE_KEY] = space

        # self._descriptors.insert(0, descriptor)
        self._descriptors.append(descriptor)
      else:
        pwar(self, f"DANGER non-Dict descriptor {descriptor}")

  def add_models(self, model_classes: List[Type[T]]):
    self._classes.extend(model_classes)

  def add_asset_dir_paths(self, paths: List[str]):
    self._asset_paths.extend(paths)

  def set_telem_backend(self, backend: Type[TelemBackend]):
    self._telem_backend = backend()

  def get_telem_backend(self) -> Optional[TelemBackend]:
    return self._telem_backend

  def add_defaults(self):
    self.add_any_descriptors(default_descriptors())
    self.add_models(default_model_classes())
    self.add_asset_dir_paths(default_asset_paths())

  def clear(self, restore_defaults=True):
    self._descriptors = []
    self._classes = []
    if restore_defaults:
      self.add_defaults()

  def query_descriptors(self, query_expr=None) -> List[Dict]:
    return structured_search.query(query_expr, self._descriptors)

  def descriptors(self, selector=None) -> List[Dict]:
    if selector:
      def discriminator(descriptor: Dict) -> bool:
        labels = descriptor.get(LABELS_KEY) or {}
        return utils.selects_labels(selector, labels)
      return list(filter(discriminator, self._descriptors))
    else:
      return self._descriptors

  def classes(self) -> List[Type[T]]:
    return self._classes

  def asset_dir_paths(self) -> List[str]:
    return self._asset_paths


models_man = ModelsMan()


class Model:

  config: Dict[str, Any]
  parent: Optional[T]
  cached_results: Dict[str, Any]
  _attr_helper_map: Dict[str, Callable]

  def __init__(self, config: Dict):
    self.config = config
    self.parent = None
    self.cached_results = {}
    self.config[KIND_KEY] = self.__class__.__name__
    self._attr_helper_map = self._gen_attr_helper_map()

  def get_id(self) -> str:
    return self.config.get(ID_KEY)

  def get_kind(self) -> str:
    return self.config.get(KIND_KEY)

  def sig(self):
    return f"{self.get_kind()}/{self.get_id() or self.get_title()}"

  def patch(self, new_props: Dict[str, any], invalidate=True) -> T:
    self.config = {**self.config, **new_props}
    if invalidate:
      for key in self.config.keys():
        if key in self.__dict__:
          invalidate_cached_property(self, key)
    return self

  def nth_parent(self, n: int) -> T:
    if n == 0:
      return self
    else:
      return self.parent.nth_parent(n - 1) if self.parent else None

  def first_parent_of_type(self, cls_type: Type[T]) -> T:
    if isinstance(self, cls_type):
      return self
    else:
      return self.first_parent_of_type(cls_type)

  def set_parent(self, parent: T):
    self.parent = parent

  def get_title(self) -> Optional[str]:
    return self.get_attr(TITLE_KEY, lookback=0)

  @cached_property
  def is_lazy(self) -> bool:
    return self.config.get(LAZY_KEY, False)

  def get_info(self) -> Optional[str]:
    return self.get_attr(INFO_KEY, lookback=0)

  def get_synopsis(self) -> str:
    return self.get_attr(SYNOPSIS_KEY, lookback=0)

  def get_tags(self) -> List[str]:
    return self.get_attr(TAGS_KEY, lookback=0, backup=[])

  def get_labels(self) -> Dict:
    return self.get_attr(LABELS_KEY, lookback=0) or {}

  def get_lookback(self) -> Union[int, bool]:
    return self.config.get(LOOKBACK_KEY, True)

  def get_space(self):
    return self.get_attr(SPACE_KEY)

  def get_config_space(self) -> str:
    # ideally safe to return None though
    if explicit := self.get_attr(CONFIG_SPACE_KEY):
      value = explicit
    else:
      value = self.get_space()
    return value or consts.app_space

  def to_dict(self):
    return dict(
      id=self.get_id(),
      title=self.get_title(),
      info=self.get_info()
    )

  def selectable_by(self, selector: Dict) -> bool:
    return utils.selects_labels(selector, self.get_labels())

  def update_attrs(self, config: Dict):
    for key, value in config.items():
      setattr(self, key, value)

  def get_attr(self, key: str, **kwargs) -> Any:
    handled, value = self.do_local_config_lookup(key, **kwargs)

    if handled:
      depth = kwargs.pop('depth', 100)
      return self.get_attr_value(value, depth) if value else value
    else:
      backup_handled, backup_value = resolve_backup(**kwargs)
      if backup_handled:
        return backup_value
      else:
        if on_miss := kwargs.pop('missing', None):
          msg = f"required prop {key} not supplied"
          error = f"[kama_sdk:{self.__class__.__name__}] {msg}"
          if on_miss == 'warn':
            print(error)
          if on_miss == 'raise':
            raise RuntimeError(error)
        return None

  def do_local_config_lookup(self, key: str, **kwargs) -> ConfigLookup:
    """
    Reads a value from the main config dicts, applies all possible
    resolution transformations to obtain its final value. This includes
    1) IFTT resolution, 2) ValueSupplier resolution, and
    3) string substitutions.
    @param key:
    @param kwargs:
    @return: fully resolved property value or backup if given
    """
    value = None

    prevent_aliasing = kwargs.pop(PREVENT_ALIASING_KEY, False)
    standard_keys = self.config.keys()
    as_new = lambda k: f"{NEW_PROP_PREF}{k}"

    if prevent_aliasing:
      if handled := key in self.config.keys():
        value = self.config.get(key)
    elif as_new(key) in standard_keys and not key.startswith(NEW_PROP_PREF):
      value = self.config[as_new(key)]
      handled = True
    elif key in standard_keys:
      value = self.config[key]
      handled = True
    elif key in self._attr_helper_map.keys():
      value = self.invoke_attr_helper(key)
      handled = True
    elif key.startswith(OLD_PROP_PREF):
      value = self.get_attr(
        key.replace(OLD_PROP_PREF, ""),
        **kwargs,
        **{PREVENT_ALIASING_KEY: True},
      )
      handled = True
    else:
      handled, value = self.resolve_from_cache(key)

    if not handled:
      handled, value = self.do_ancestral_config_lookup(
        key,
        **{PREVENT_ALIASING_KEY: prevent_aliasing},
        **kwargs,
      )

    return handled, value

  def user_props_cache(self) -> Dict:
    return self.config.get(CACHED_KEY, {})

  def resolve_from_cache(self, key: str) -> ConfigLookup:
    in_config_cache_def = key in self.user_props_cache().keys()
    in_cache = self.is_attr_cached(key)

    if in_config_cache_def or in_cache:
      if in_cache:
        return True, self.cached_results[key]
      else:
        unresolved_value = self.user_props_cache()[key]
        resolved_value = self.get_attr_value(unresolved_value)
        # resolved_value = unresolved_value
        self.cached_results[key] = resolved_value
        return True, resolved_value
    else:
      return False, None

  def is_attr_cached(self, key: str) -> bool:
    return key in self.cached_results.keys()

  def do_ancestral_config_lookup(self, key: str, **kwargs) -> ConfigLookup:
    explicit_lookback_req = kwargs.pop(LOOKBACK_KEY, None)
    lookback = self.lookback2int(explicit_lookback_req)

    if self.parent and lookback > 0:
      return self.parent.do_local_config_lookup(
        key,
        **{LOOKBACK_KEY: lookback - 1},
        **kwargs
      )
    else:
      return False, None

  def invoke_attr_helper(self, attr_key: str) -> Optional[Any]:
    if method := self._attr_helper_map.get(attr_key):
      return method(self)

  def get_attr_value(self, value: Any, depth=0) -> Optional[Any]:
    if isinstance(value, str):
      return self.resolve_str_like_prop_value(value)
    elif isinstance(value, list):
      return self.resolve_list_like_prop_value(value, depth)
    elif isinstance(value, dict):
      return self.resolve_dict_like_prop_value(value, depth)
    else:
      return value

  def resolve_str_like_prop_value(self, value: Any):
    if value in NULLISH_ALIASES:
      return None
    else:
      value = self.supplier_resolve_or_identity(value)
      value = self.interpolate_prop(value)
      return self.try_read_from_asset(value)

  def resolve_list_like_prop_value(self, value: List, depth=0):
    resolved_sub_values = []
    for sub_value in value:
      if type(sub_value) == str and sub_value.startswith(SPLATTER_STR):
        resolvable_part = sub_value.split(SPLATTER_STR)[1]
        resolved_sub_value = self.get_attr_value(resolvable_part, depth)
        if utils.listlike(resolved_sub_value):
          resolved_sub_values.extend(resolved_sub_value)
        elif resolved_sub_value is not None:
          tp = type(resolved_sub_value)
          pwar(self, f"danger cannot splatter {tp} {resolved_sub_value}")
      else:
        resolved_sub_value = self.get_attr_value(sub_value, depth)
        resolved_sub_values.append(resolved_sub_value)
    return resolved_sub_values

  def resolve_dict_like_prop_value(self, value: Dict, depth=0):
    txd_value = self.supplier_resolve_or_identity(value)
    if type(txd_value) == dict and int(depth or 0) > 0:
      perf = lambda v: self.get_attr_value(v, depth - 1)
      return {k: perf(v) for (k, v) in txd_value.items()}
    else:
      return txd_value

  def interpolate_prop(self, value: str) -> Any:
    """
    Performs string substitutions on input. Combines substitution context
    from instance's self.context and any additional context passed as
    parameters. Returns unchanged input if property is not a string.
    @param value: value of property to interpolate
    @return: interpolated string if input is string else unchanged input
    """
    if value and type(value) == str:
      def resolve(expr: str):
        ret = self.supplier_resolve_or_identity(expr)
        return str(ret) if ret else ''
      return str_sub.interpolate(value, resolve)
    else:
      return value

  @classmethod
  def kind(cls):
    return cls.__name__

  def serialize(self) -> Dict[str, Any]:
    src_items = list(self.config.items())
    no_copy = ['cache']
    return {k: v for k, v in src_items if k not in no_copy}

  def clone(self) -> T:
    new_model = self.__class__(self.serialize())
    new_model.parent = self.parent
    return new_model

  def inflate_children(self, child_cls: Type[T], **kwargs) -> List[T]:
    """
    Bottleneck function for a parent model to inflate a list of children.
    In the normal case, kods_or_provider_kod is a list of WizModels KoDs.
    In the special case, kods_or_provider_kod is ListGetter model
    that produces the actual children.
    case,
    @param child_cls: class all children must a subclass of
    @return: resolved list of WizModel children
    """
    kods_or_supplier = self.resolve_child_ref_kod(
      kod=kwargs.pop('kod', None),
      prop=kwargs.pop('prop', None),
      resolve_kod=kwargs.pop(RESOLVE_CHILD_KOD_FLAG, False)
    ) or []

    kod2child = lambda obj: self.kod2child(obj, child_cls, **kwargs)

    if utils.listlike(kods_or_supplier):
      children_kods: List[KoD] = kods_or_supplier
      return list(map(kod2child, children_kods))
    elif type(kods_or_supplier) in [str, dict]:
      supplier_kod = kods_or_supplier
      from kama_sdk.model.supplier.base.supplier import Supplier

      children_kods = self.supplier_resolve_or_identity(supplier_kod)
      if isinstance(children_kods, list):
        return list(map(kod2child, children_kods))
      elif isinstance(children_kods, dict):
        query_dict = children_kods
        child_instances = child_cls.inflate_all(**{
          query_kw: query_dict
        })
        [c.set_parent(self) for c in child_instances]
        return child_instances
      else:
        err = f"children must be list or supplier not {supplier_kod}"
        raise RuntimeError(f"[Model] {err}")

  def inflate_child(self, child_cls: Type[T], **kwargs) -> Optional[T]:
    child_kod: KoD = self.resolve_child_ref_kod(
      kod=kwargs.pop('kod', None),
      prop=kwargs.pop('prop', None),
      resolve_kod=kwargs.pop(RESOLVE_CHILD_KOD_FLAG, True)
    )
    return self.kod2child(child_kod, child_cls, **kwargs)

  def resolve_child_ref_kod(self, **kwargs) -> Union[List[KoD], KoD]:
    if explicit_kod := kwargs.get('kod'):
      return explicit_kod
    elif prop_name := kwargs.get('prop'):
      if kwargs.get(RESOLVE_CHILD_KOD_FLAG, True):
        return self.get_attr(prop_name, lookback=0)
      else:
        # return self.get_attr(prop_name, lookback=0, depth=0)
        return self.config.get(prop_name)
    else:
      base = f"child ref from {self.sig()} must include kod or prop"
      perr(self, f"{base} , neither found in {kwargs}")

  def kod2child(self, kod: KoD, child_cls: Type[T], **kwargs) -> T:
    try:
      down_kw = {**kwargs, 'mute': True}
      inflated = child_cls.inflate(kod, **down_kw)
      if inflated:
        inflated.parent = self
      return inflated
    except Exception as e:
      exp_child_kind = child_cls.__name__ if isinstance(child_cls, type) else '?'
      child_part = f"child {exp_child_kind} = {kod}"
      perr(self, f"parent {self.sig()} failed to inflate {child_part}")
      raise e

  def prop_inheritance_pool(self):
    return self.config

  def lookback2int(self, override: Union[bool, int]) -> int:
    overridden = override is not None
    lookback = override if overridden else self.get_lookback()
    if type(lookback) == int:
      return lookback
    else:
      return 1000 if lookback else 0

  @classmethod
  def inflate_single(cls: T, **kwargs) -> Optional[Model]:
    models = cls.inflate_all(**kwargs)
    if (count := len(models)) > 1:
      sel_part = f"(sel={kwargs.get('selector')})"
      pwar(cls, f"expected 1 result, got {count} {sel_part}")
    return models[0] if len(models) > 0 else None

  @classmethod
  def inflate_all(cls, **kwargs) -> List[T]:
    query_expr = kwargs.pop(query_kw, None)
    cls_pool = cls.lteq_classes(models_man.classes())
    config_pool = models_man.query_descriptors(query_expr)
    configs_in_kind = configs_for_kinds(config_pool, cls_pool)
    return [cls.inflate(config, **kwargs) for config in configs_in_kind]

  @classmethod
  def inflate_many(cls: T, kods: List[KoD], **kwargs) -> List[Model]:
    instances: List[Model] = []
    safely = kwargs.pop('safely', False)
    for kod in kods:
      try:
        instances.append(cls.inflate(kod, **kwargs))
      except Exception as e:
        if not safely:
          raise e
    return instances

  @classmethod
  def inflate(cls: T, kod: KoD, **kwargs) -> Optional[T]:
    try:
      if isinstance(kod, str):
        return cls.inflate_with_str(kod, **kwargs)
      elif isinstance(kod, Dict):
        return cls.inflate_with_config(kod, **kwargs)
      else:
        raise InflateModelError(f"inflate value {kod} neither dict or str")
    except Exception as err:
      if kwargs.pop('safely', False):
        return None
      else:
        if not kwargs.pop('mute', False):
          perr(cls, f"inflate error below for {kod}")
        raise err

  @classmethod
  def from_yaml(cls, yaml_str: str, **kwargs) -> Optional[Model]:
    as_dict = yaml.load(yaml_str)
    return cls.inflate_with_config(as_dict, **kwargs)

  @classmethod
  def inflate_with_str(cls, string: str, **kwargs) -> T:
    if string.startswith(KIND_REFERENCE_PREFIX):
      referenced_kind = string.split(KIND_REFERENCE_PREFIX)[1]
      return cls.inflate_with_kind_reference(referenced_kind, **kwargs)

    elif string.startswith(ID_REFERENCE_PREFIX):
      referenced_id = string.split(ID_REFERENCE_PREFIX)[1]
      return cls.inflate_with_id_reference(referenced_id, **kwargs)

    elif string.startswith(EXPR_REFERENCE_PREFIX):
      literal_expr = string.split(EXPR_REFERENCE_PREFIX)[1]
      return cls.inflate_with_literal(literal_expr, **kwargs)

    else:
      return cls.inflate_with_id_reference(string, **kwargs)

  @classmethod
  def inflate_with_literal(cls, expr: str, **kwargs) -> Optional[Model]:
    return None

  @classmethod
  def inflate_with_kind_reference(cls, kind_ref: str, **kwargs) -> Model:
    config = dict(kind=kind_ref)
    return cls.inflate_with_config(config, **kwargs)

  @classmethod
  def inflate_with_id_reference(cls, id_ref: str, **kwargs) -> T:
    candidate_subclasses = cls.lteq_classes(models_man.classes())
    candidate_kinds = [klass.kind() for klass in candidate_subclasses]
    query_expr = kwargs.pop(query_kw, None)
    candidate_configs = models_man.query_descriptors(query_expr)
    config = find_config_by_id(id_ref, candidate_configs, candidate_kinds)
    return cls.inflate_with_config(config, **kwargs)

  @classmethod
  def descendent_or_self(cls: T) -> T:
    subclasses = cls.lteq_classes(models_man.classes())
    not_self = lambda kls: not kls == cls
    return next(filter(not_self, subclasses), cls)({})

  @classmethod
  def inflate_with_config(cls, config: Dict, **kwargs) -> T:

    if config is None:
      raise InflateModelError("inflate_with_config given no config")

    patches: Optional[Dict] = kwargs.get('patches', {})

    host_class = cls

    inherit_id = config.get(INHERIT_KEY)
    explicit_kind = config.get(KIND_KEY)

    if explicit_kind and not explicit_kind == host_class.__name__:
      host_class = cls.kind2cls(explicit_kind)
      if not host_class:
        err = f"no kind {explicit_kind} under {cls.__name__}"
        raise RuntimeError(f"[Model] FATAL {err}")

    if inherit_id:
      other: T = cls.inflate_with_str(inherit_id, **kwargs)
      host_class = other.__class__
      config = utils.deep_merge(other.serialize(), config)

    final_config = deepcopy(utils.deep_merge(config, patches))
    model_instance = host_class(final_config)

    return model_instance

  @classmethod
  def global_provider_id(cls):
    raise NotImplemented

  @classmethod
  def from_provider(cls, provider_kod: KoD = None) -> List[Model]:
    from kama_sdk.model.supplier.base.supplier import Supplier
    provider_kod = provider_kod or cls.global_provider_id()
    provider: Supplier = Supplier.inflate(provider_kod)
    return cls.inflate_many(provider.resolve())

  @classmethod
  def singleton_id(cls):
    raise NotImplemented

  @classmethod
  def inflate_singleton(cls, **kwargs) -> T:
    return cls.inflate_with_str(cls.singleton_id(), **kwargs)

  def supplier_resolve_or_identity(self, kod: KoD, **kwargs) -> Any:
    from kama_sdk.model.supplier.base.supplier import Supplier
    prefix: str = "get::"

    if self.is_interceptor_candidate(Supplier, prefix, kod):
      final_kod = kod
      if type(kod) == str:
        trimmed_kod = kod.replace(prefix, "")
        # if trimmed_kod.startswith(LAZY_SYMBOL):
        #   trimmed_kod = trimmed_kod[len(LAZY_SYMBOL):]
        final_kod = Supplier.expr2kod(trimmed_kod)

      kwargs.pop('safely', None)
      interceptor = Supplier.inflate(
        final_kod,
        safely=True,
        **kwargs
      )

      if interceptor:
        interceptor.parent = self
        # lazy = self.is_interceptor_lazy(no_prefix_kod, interceptor.config)
        # return interceptor if lazy else interceptor.resolve()
        return interceptor.resolve()

    return kod

  @classmethod
  def id_exists(cls, _id: str) -> bool:
    return True

  @staticmethod
  def truncate_kod_prefix(kod: KoD, prefix: str) -> KoD:
    if type(kod) == str and len(kod) >= len(prefix):
      return kod[len(prefix):len(kod)]
    return kod

  @classmethod
  def is_interceptor_lazy(cls, kod: Any, config: Dict):
    if isinstance(kod, str) and kod.startswith("&"):
      return True
    else:
      return bool(config.get('lazy'))

  @classmethod
  def is_interceptor_candidate(cls, interceptor: Type[T], prefix, kod: KoD):
    if type(kod) == dict:
      interceptors = interceptor.lteq_classes(models_man.classes())
      if kod.get('kind') in [c.__name__ for c in interceptors]:
        return True
    if type(kod) == str:
      return kod.startswith(prefix)
    return False

  @classmethod
  def lteq_classes(cls, classes: List[Type]) -> List[Type[T]]:
    return [klass for klass in [*classes, cls] if issubclass(klass, cls)]

  @classmethod
  def kind2cls(cls, kind: str):
    subclasses = cls.lteq_classes(models_man.classes())
    return find_class_by_name(kind, subclasses)

  @staticmethod
  def try_read_from_asset(value):
    if value and type(value) == str:
      if value.startswith(ASSETS_PREFIX):
        return read_from_asset(value)
    return value

  def _gen_attr_helper_map(self) -> Dict[str, Callable]:
    result = {}
    for method_name, _ in inspect.getmembers(self.__class__):
      candidate_method = getattr(self.__class__, method_name)

      if hasattr(candidate_method, model_decorators.FUNCTION_ATTR_KEY):
        caching_api = self._generate_caching_api()
        setattr(candidate_method, model_decorators.CACHING_API_KEY, caching_api)
        result[candidate_method.attr_key] = candidate_method
    return result

  def _generate_caching_api(self) -> ModelCacheApi:
    model_instance = self

    class NanoCachingApi(ModelCacheApi):
      def has_entry(self, key: str) -> bool:
        return key in model_instance.cached_results.keys()

      def get_entry(self, key: str) -> Optional[Any]:
        return model_instance.cached_results.get(key)

      def set_entry(self, key: str, value: Any):
        model_instance.cached_results[key] = value

    return NanoCachingApi()


def read_from_asset(descriptor: str) -> str:
  _, path = descriptor.split("::")
  for dirpath in models_man.asset_dir_paths():
    full_path = f"{dirpath}/{path}"
    if isfile(full_path):
      with open(full_path) as file:
        return file.read()
  return ''


def key_or_dict_to_key(key_or_dict: Union[str, dict]) -> str:
  if isinstance(key_or_dict, str):
    return key_or_dict
  elif isinstance(key_or_dict, dict):
    return key_or_dict.get('id')
  raise RuntimeError(f"Can't handle {key_or_dict}")


def key_or_dict_matches(key_or_dict: KoD, target_key: str) -> bool:
  return key_or_dict_to_key(key_or_dict) == target_key


def find_class_by_name(name: str, classes) -> Type:
  matcher = lambda klass: klass.__name__ == name
  return next(filter(matcher, classes), None)

def find_any_class_by_name(name: str) -> Type:
  matcher = lambda klass: klass.__name__ == name
  return next(filter(matcher, models_man.classes()), None)

def find_any_config_by_id(_id: str) -> Dict:
  matcher = lambda c: c.get(ID_KEY) == _id
  return next(filter(matcher, models_man.descriptors()), None)

def find_config_by_id(_id: str, configs: List[Dict], kinds: List[str]) -> Dict:
  matcher = lambda c: c.get('id') == _id and c.get(KIND_KEY) in kinds
  return next(filter(matcher, configs), None)


def configs_for_kinds(configs: List[Dict], cls_pool) -> List[Dict]:
  kinds_pool = [cls.__name__ for cls in cls_pool]
  return [c for c in configs if c.get(KIND_KEY) in kinds_pool]


def default_descriptors() -> List[Dict]:
  pwd = os.path.join(os.path.dirname(__file__))
  search_space_root = f"{pwd}/../../model"
  yaml_dirs = discover_model_yaml_dirs(search_space_root)
  return utils.flatten(list(map(utils.yamls_in_dir, yaml_dirs)))


def discover_model_yaml_dirs(root: str) -> List[str]:
  pwd = root.split('/')[-1]
  is_root_yaml_dir = pwd == 'yamls'
  child_paths = [f"{root}/{name}" for name in os.listdir(root)]
  child_dirs = list(filter(os.path.isdir, child_paths))
  child_results = list(map(discover_model_yaml_dirs, child_dirs))
  self_result = [root] if is_root_yaml_dir else []
  return self_result + utils.flatten(child_results)


def default_asset_paths() -> List[str]:
  pwd = os.path.join(os.path.dirname(__file__))
  return [f"{pwd}/../../assets"]


def resolve_backup(**kwargs):
  lazy_backup = kwargs.pop('lazy_backup', None)
  if lazy_backup is not None:
    return True, lazy_backup()
  elif 'backup' in kwargs.keys():
    return True, kwargs.pop('backup', None)
  else:
    return False, None


NULLISH_ALIASES = ['__none__', '__null__', '__nil__', '__undefined__']
NEW_PROP_PREF = "new__"
OLD_PROP_PREF = "old__"
ID_REFERENCE_PREFIX = "id::"
EXPR_REFERENCE_PREFIX = "expr::"
KIND_REFERENCE_PREFIX = "kind::"
PREVENT_ALIASING_KEY = 'old'
LOOKBACK_KEY = 'lookback'
SPLATTER_STR = '...'
RESOLVE_CHILD_KOD_FLAG = 'resolve_kod'
CACHED_KEY = 'cached'
SPACE_KEY = 'space'
CONFIG_SPACE_KEY = 'config_space'
SPACE_LABEL = 'space'

ID_KEY = 'id'
TITLE_KEY = 'title'
SYNOPSIS_KEY = 'synopsis'
INHERIT_KEY = 'inherit'
KIND_KEY = 'kind'
INFO_KEY = 'info'
TAGS_KEY = 'tags'
LABELS_KEY = 'labels'
SEARCHABLE_KEY = 'searchable'
FULL_SEARCHABLE_KEY = f'{LABELS_KEY}.{SEARCHABLE_KEY}'
ASSETS_PREFIX = f'{consts.ASSETS_PREFIX}::'

LAZY_KEY = 'lazy'
LAZY_SYMBOL = "&"

query_kw = 'q'
