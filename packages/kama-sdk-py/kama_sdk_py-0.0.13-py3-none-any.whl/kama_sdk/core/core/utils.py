import collections
import functools
import json
import os
import random
import string
import subprocess
import sys
import traceback
import uuid
from datetime import datetime
from functools import reduce
from os import listdir
from os.path import isfile, join, isdir
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Callable

import yaml
from inflection import underscore
from k8kat.auth.kube_broker import broker
from k8kat.res.base.kat_res import KatRes
from k8kat.utils.main.api_defs_man import api_defs_man
from termcolor import cprint
from yaml import scanner

from kama_sdk.core.core.types import KAO, K8sResDict, K8sResSig

legal_envs = ['production', 'development', 'test']


def exec_mode() -> str:
  from_argv = sys.argv[1] if len(sys.argv) >= 2 else None
  return from_argv or 'server'


def exception2trace(exception: Exception) -> List[str]:
  as_list = traceback.format_exception(
    etype=type(exception),
    value=exception,
    tb=exception.__traceback__
  )
  return list(map(str.strip, as_list)) if as_list else []


def is_in_cluster() -> bool:
  return broker.is_in_cluster_auth()


def is_out_of_cluster() -> bool:
  return not is_in_cluster()


def is_shell() -> bool:
  return exec_mode() == 'shell'


def listlike(value: Any) -> bool:
  return isinstance(value, list)


def dictlike(value: Any) -> bool:
  return isinstance(value, dict)


def worker_uuid() -> Optional[str]:
  return os.environ.get('WIZ_WORKER_UUID')


def keyed2dict(keyed_assigns: List[Tuple[str, any]]) -> Dict:
  root = {}
  for keyed_assign in keyed_assigns:
    deep_key_as_list = keyed_assign[0].split('.')  # fully qualified hash key
    deep_set(root, deep_key_as_list, keyed_assign[1])
  return root


def deep_merge(*dicts):
  from k8kat.utils.main.utils import deep_merge as k8kat_deep_merge
  merged = {}
  for _dict in dicts:
    merged = k8kat_deep_merge(merged, _dict)
  return merged


def deep_unset(deep_dict: Dict, victim_keys) -> Dict:
  flat_source = deep2flat(deep_dict)
  for victim_key in victim_keys:
    flat_source.pop(victim_key, None)
  return flat2deep(flat_source)


def flat2deep(flat_dict: Dict) -> Dict:
  return keyed2dict(list(flat_dict.items()))


def dict2keyed(assigns: Dict) -> List[Tuple[str, any]]:
  list_keyed_dict = _dict2keyed([], assigns)
  cleaner = lambda t: (".".join(t[0]), t[1])
  return list(map(cleaner, list_keyed_dict))


def deep2flat(assigns) -> Dict:
  tuples = dict2keyed(assigns)
  return {t[0]: t[1] for t in tuples}


def _dict2keyed(parents, assigns: Dict) -> List[Tuple[List[str], any]]:
  result: List[Tuple[List[str], any]] = []

  for assign in assigns.items():
    key, value = assign
    if type(value) == dict:
      result = result + _dict2keyed(parents + [key], value)
    else:
      result.append((parents + [key], value))
  return result


def deep_set(dict_root: Dict, names: List[str], value: any):
  """
  Iterates over items in names list, using them as keys to go deeper into the
  dictionary at each iteration. Eventually sets the passed value with the final key.
  with the passed value.
  :param dict_root: dict to be modified with the desired value.
  :param names: list of names to be iterated over, to find the right depth.
  :param value: value to be eventually set at the right depth.
  """
  if len(names) == 1:
    dict_root[names[0]] = value
  else:
    if not dict_root.get(names[0]):
      dict_root[names[0]] = dict()
    deep_set(dict_root[names[0]], names[1:], value)


def deep_get2(dict_root: Dict, deep_key) -> Any:
  return deep_get(dict_root, deep_key.split('.'))


def deep_set2(dict_root: Dict, deep_key: str, value: Any):
  deep_set(dict_root, deep_key.split("."), value)


def deep_get(dict_root: Dict, keys: List[str]) -> Any:
  """
  Iterates over items in keys list, using them as keys to go deeper into the
  dictionary at each iteration. Eventually retrieves the value of the final key.
  :param dict_root: dict containing the desired value.
  :param keys: list of keys to be iterated over, to find the right depth.
  :return: value of the final key.
  """
  keys = [k for k in keys if not k.strip() == '']

  if len(keys) > 0:
    return reduce(
      lambda d, key: d.get(key, None)
      if isinstance(d, dict)
      else None, keys, dict_root
    )
  else:
    return dict_root


def exclusive_deep_merge(**kwargs) -> Dict:
  old_dict = kwargs['old_dict']
  new_dict = kwargs['new_dict']
  weak_var_keys = kwargs['weak_var_keys']

  merged = deep_merge(old_dict, new_dict)
  old_dict_deep_keys = list(deep2flat(old_dict).keys())
  for deep_key in old_dict_deep_keys:
    if deep_key not in weak_var_keys:
      original_value = deep_get2(old_dict, deep_key)
      deep_set2(merged, deep_key, original_value)

  return merged


def dupes(a: List):
  items = collections.Counter(a).items()
  return [item for item, count in items if count > 1]


def pluck_or_getattr_deep(obj, attr):
  """
  Deep attribute supplier.
  :param obj: Object from which to get the attribute.
  :param attr: attribute to get.
  :return: value of the attribute if found, else None.
  """

  def _getattr(_obj, _attr):
    if type(_obj) == dict:
      return _obj[_attr]
    else:
      if hasattr(_obj, _attr):
        func_or_lit = getattr(_obj, _attr)
        return func_or_lit() if callable(func_or_lit) else func_or_lit
      elif hasattr(_obj, "get_prop"):
        func = getattr(_obj, "get_prop")
        return func(_attr)
  try:
    return functools.reduce(_getattr, [obj] + attr.split('.'))
  except AttributeError:
    return None


def shell_exec(unsplit_cmd: str) -> str:
  formatted_cmd = unsplit_cmd.split(' ')
  output = subprocess.run(
    formatted_cmd,
    stdout=subprocess.PIPE
  )
  return output.stdout.decode('utf-8')


def perr(inst, message, trace=False):
  if trace:
    message = f"{message}\n{traceback.format_exc()}"
  print_colored(inst, message, 'magenta')


def pwar(inst, message, trace=False):
  if trace:
    message = f"{message}\n{traceback.format_exc()}"
  print_colored(inst, message, 'yellow')


def print_colored(inst, message, color):
  if isinstance(inst, type):
    class_sig = underscore(inst.__name__)
  elif hasattr(inst, '__class__'):
    class_sig = underscore(inst.__class__.__name__)
  elif isinstance(inst, str):
    class_sig = inst.split('.')[:-1] if "." in inst else inst
  else:
    class_sig = 'unknown_origin'
  cprint(f"[kama_sdk:{class_sig}] {message}", color=color, attrs=['bold'])


def yamls_in_dir(dir_path, recursive=None) -> List[Dict]:
  is_yaml = lambda path: isfile(path) and path.endswith(".yaml")
  fnames = [f for f in listdir(dir_path) if is_yaml(join(dir_path, f))]
  yaml_arrays = [yamls_in_file(f"{dir_path}/{fname}") for fname in fnames]
  if recursive:
    sub_dirs = [f for f in listdir(dir_path) if isdir(join(dir_path, f))]
    for sub_dir in sub_dirs:
      yaml_arrays.append(yamls_in_dir(join(dir_path, sub_dir), True))
  return flatten(yaml_arrays)


def yamls_in_file(fname) -> List[Dict]:
  """
  Converts a YAML file into a list of dicts.
  :param fname: YAML file.
  :return: list of dicts.
  """
  with open(fname, 'r') as stream:
    file_contents = stream.read()
    try:
      raw_list = list(yaml.full_load_all(file_contents))
      reject_nullish = lambda y: len((y or {}).items()) > 0
      return list(filter(reject_nullish, raw_list))
    except scanner.ScannerError as e:
      print(f"[kama_sdk::utils] YAML parse error @ {fname}")
      raise e


def jk_exec(cmd, **kwargs) -> Dict[str, any]:
  cmd = f"{kmd(cmd, **kwargs)} -o json"
  result = shell_exec(cmd)
  return json.loads(result)


def k_exec(cmd, **kwargs) -> str:
  cmd = kmd(cmd, **kwargs)
  return shell_exec(cmd)


def kmd(cmd: str, **kwargs) -> str:
  kubectl = kwargs.get('k', 'kubectl')
  ns = kwargs.get('ns', None)
  context = kwargs.get('ctx', None)

  cmd = f"{cmd} -n {ns}" if ns else cmd
  cmd = f"{cmd} --context={context}" if context else cmd
  cmd = f"{kubectl} {cmd}"

  return cmd


def root_path() -> str:
  return str(Path(__file__).parent.parent.parent)


def set_run_env(_run_env):
  if _run_env in legal_envs:
    os.environ['FLASK_ENV'] = _run_env
    os.environ['KAT_ENV'] = _run_env
  else:
    raise Exception(f"Bad environment '{_run_env}'")


def run_env() -> str:
  return os.environ.get('FLASK_ENV', 'production')


def is_prod() -> bool:
  return run_env() == 'production'


def is_dev() -> bool:
  return run_env() == 'development'


def is_in_cluster_dev():
  return is_dev() and broker.is_in_cluster_auth()


def is_local_dev_server():
  return not broker.is_in_cluster_auth()


def is_test() -> bool:
  return run_env() == 'test'


def is_ci() -> bool:
  return is_test() and os.environ.get('CI')


def is_ci_keep():
  return os.environ.get("CI") == 'keep'


def any2bool(anything: Any) -> bool:
  if type(anything) == bool:
    return anything
  elif type(anything) == str:
    if anything in ['true', 'True', 'yes', 'positive']:
      return True
    elif anything in ['false', 'False', 'None', 'no', 'negative']:
      return False
    else:
      return bool(anything)
  else:
    return bool(anything)


def is_non_trivial(dict_array):
  if not dict_array:
    return False
  return [e for e in dict_array if e]


def is_either_hash_in_hash(big_hash, little_hashes):
  little_tuples = [list(h.items())[0] for h in little_hashes]
  for _tuple in (big_hash or {}).items():
    if _tuple in little_tuples:
      return True
  return False


def selects_labels(selector: Dict, actual_labels: Dict):
  for key, value in selector.items():
    value_as_list = value if listlike(value) else [value]
    if key not in actual_labels.keys():
      return False
    if actual_labels[key] not in value_as_list:
      return False
  return True


# noinspection PyBroadException
def try_or(lam, fallback=None):
  try:
    return lam()
  except:
    return fallback


def dict_to_eq_str(_dict):
  return ",".join(
    ["=".join([k, str(v)]) for k, v in _dict.items()]
  )


def parse_dict_array(_string):
  parts = _string.split(',')
  return [parse_dict(part) for part in parts]


def parse_dict(encoded_dict):
  result_dict = {}
  for encoded_kv in encoded_dict.split(','):
    key, value = encoded_kv.split(':')
    result_dict[key] = value
  return result_dict


def rand_str(string_len=10):
  letters = string.ascii_lowercase
  return ''.join(random.choice(letters) for _ in range(string_len))


def gen_uuid() -> str:
  return str(uuid.uuid4())


def fqcn(o):
  module = o.__class__.__module__
  if module is None or module == str.__class__.__module__:
    return o.__class__.__name__
  else:
    return module + '.' + o.__class__.__name__


def coerce_cmd_format(cmd):
  if isinstance(cmd, str):
    return cmd.split(" ")
  else:
    return cmd


def clean_log_lines(chunk) -> List[str]:
  if type(chunk) == str:
    log_lines = chunk.split("\n")
    weeder = lambda line: not line.strip() == ''
    return list(filter(weeder, log_lines))
  elif type(chunk) == list:
    return chunk
  else:
    return []


def log2kao(log: str) -> Optional[KAO]:
  try:
    api = ''
    kind_and_name, verb = log.split(" ")
    kind, name = kind_and_name.split("/")
    if "." in kind:
      parts = kind.split(".")
      kind = parts[0]
      api = '.'.join(parts[1:])
    return KAO(
      api_group=api,
      kind=kind,
      name=name,
      verb=verb,
      error=None
    )
  except:
    return None


def kao2log(kao: KAO) -> str:
  group_and_kind = ''
  if kao.get('api_group'):
    group_and_kind = f"{kao.get('api_group')}."
  group_and_kind = f"{group_and_kind}{kao.get('kind')}"
  identity = f"{group_and_kind}/{kao.get('name')}"

  if not kao.get('error'):
    return f"{identity} {kao.get('verb')}"
  else:
    return f"{identity} {kao.get('error')}"


def same_res(r1: K8sResSig, r2: K8sResSig):
  kinds_eq = api_defs_man.kind2plurname(r1['kind']) and \
             api_defs_man.kind2plurname(r2['kind'])
  names_eq = r1['name'] == r2['name']
  return kinds_eq and names_eq


def full_res2sig(res_dict: K8sResDict) -> K8sResSig:
  meta = res_dict.get('metadata') or {}
  return K8sResSig(
    kind=res_dict.get('kind'),
    name=meta.get('name')
  )


def logs2outkomes(logs: List[str]) -> List[KAO]:
  outcomes = list(map(log2kao, logs))
  return [o for o in outcomes if o is not None]


def flatten(nested_list):
  return [item for sublist in nested_list for item in sublist]


def compact(nullish_list: List[Optional[Any]]) -> List[Any]:
  return [item for item in nullish_list if item is not None]


def unmuck_primitives(root: Any) -> Any:
  if type(root) == dict:
    return {k: unmuck_primitives(v) for k, v in root.items()}
  elif type(root) == list:
    return list(map(unmuck_primitives, root))
  else:
    return unmuck_primitive(root)


def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False


def unmuck_primitive(original: Any) -> Any:
  if type(original) == str:
    if original.isdigit():
      return int(original)
    elif isfloat(original):
      return float(original)
    elif original.lower() == 'true':
      return True
    elif original.lower() == 'false':
      return False
    else:
      return original
  else:
    return original


def kres2dict(kat_res: KatRes) -> Optional[Dict]:
  if kat_res:
    if raw_res := kat_res.raw:
      as_dict = raw_res.to_dict()
      as_dict['kind'] = kat_res.kind
      return sanitize_kres_values(as_dict)
    else:
      print("[kama_sdk:res_sup] danger kat_res has no .raw")
      print(kat_res)
      return sanitize_kres_values(kat_res.__dict__)
  else:
    return None


def safely(func: Callable, bkp=None) -> Any:
  try:
    return func()
  except:
    return bkp


def sanitize_kres_values(root: Any) -> Any:
  if dictlike(root):
    new_root = {}
    for key, value in root.items():
      if listlike(value):
        new_root[key] = list(map(sanitize_kres_values, value))
      elif dictlike(value):
        new_root[key] = sanitize_kres_values(value)
      elif isinstance(value, datetime):
        new_root[key] = str(value)
      else:
        new_root[key] = value
    return new_root
  else:
    return root


def unique(seq, key=None):
  seen = set()
  seen_add = seen.add
  if key is None:
    for item in seq:
      if item not in seen:
        seen_add(item)
        yield item
  else:
    for item in seq:
      val = key(item)
      if val not in seen:
        seen_add(val)
        yield item