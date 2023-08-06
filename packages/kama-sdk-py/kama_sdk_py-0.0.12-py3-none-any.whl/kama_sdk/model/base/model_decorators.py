from typing import Dict, Callable, Optional


def model_attr(**kwargs) -> Callable:
  def inner(user_func):
    should_cache = kwargs.get('cache') or kwargs.get('cached')
    attr_key = kwargs.get('name') or kwargs.get('key')
    if not attr_key:
      attr_key = user_func.__name__

    def new_func(*func_args, **func_kwargs):
      cache: Optional[Dict] = getattr(new_func, 'cache')
      if cache is not None:
        if attr_key in cache.keys():
          return cache[attr_key]
        else:
          computed_result = user_func(*func_args, **func_kwargs)
          if should_cache:
            cache[attr_key] = computed_result
          return computed_result
      else:
        print("called without inst!")
        return user_func(*func_args, **func_kwargs)

    new_func.cache = None
    new_func.attr_key = attr_key
    return new_func
  return inner
