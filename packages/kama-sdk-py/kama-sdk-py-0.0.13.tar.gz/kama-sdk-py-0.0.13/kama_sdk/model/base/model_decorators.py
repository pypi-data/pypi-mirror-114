import functools
from abc import ABC, abstractmethod
from typing import Optional, Any


def model_attr(user_func=None, key: str = None, cached: bool = True):

  if not user_func:
    return functools.partial(model_attr, key=key, cached=cached)

  final_key = key or f"resolved_{user_func.__name__}"
  should_cache = cached

  @functools.wraps(user_func)
  def new_func(*func_args, **func_kwargs):
    compute_original = lambda: user_func(*func_args, **func_kwargs)

    if should_cache:
      caching_api: ModelCacheApi = getattr(new_func, CACHING_API_KEY)

      if caching_api.has_entry(final_key):
        return caching_api.get_entry(final_key)
      else:
        computed_result = compute_original()
        if should_cache:
          caching_api.set_entry(final_key, computed_result)
        return computed_result
    else:
      return user_func(*func_args, **func_kwargs)

  setattr(new_func, FUNCTION_ATTR_KEY, final_key)
  return new_func


def model_attr_old(key: str = None, cached: bool = True):
  def inner(user_func):
    print(f"CALLED ON {user_func}")
    final_key = key or f"resolved_{user_func.__name__}"
    should_cache = cached

    def new_func(*func_args, **func_kwargs):
      compute_original = lambda: user_func(*func_args, **func_kwargs)

      if should_cache:
        caching_api: ModelCacheApi = getattr(user_func, CACHING_API_KEY)

        if caching_api.has_entry(key):
          return caching_api.get_entry(key)
        else:
          computed_result = compute_original()
          if should_cache:
            caching_api.set_entry(key, computed_result)
          return computed_result
      else:
        print("called without inst!")
        return user_func(*func_args, **func_kwargs)

    new_func.should_cache = should_cache
    setattr(new_func, FUNCTION_ATTR_KEY, final_key)
    return new_func

  return inner


class ModelCacheApi(ABC):

  @abstractmethod
  def has_entry(self, key: str) -> bool:
    pass

  @abstractmethod
  def get_entry(self, key: str) -> Optional[Any]:
    pass

  @abstractmethod
  def set_entry(self, key: str, value: Any):
    pass


ATTR_KEY_KEY = 'key'
FUNCTION_ATTR_KEY = 'attr_key'
CACHING_API_KEY = 'cached'
