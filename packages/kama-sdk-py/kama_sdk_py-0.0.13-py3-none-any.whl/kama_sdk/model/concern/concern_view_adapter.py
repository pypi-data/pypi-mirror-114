from typing import TypeVar

from werkzeug.utils import cached_property

from kama_sdk.core.core.types import Reconstructor
from kama_sdk.core.core.utils import perr, pwar
from kama_sdk.model.base.model import Model
from kama_sdk.model.concern.concern import Concern
from kama_sdk.model.concern import concern as concern_module

T = TypeVar('T', bound='ConcernViewAdapter')


class ConcernViewAdapter(Model):

  @cached_property
  def concern_shell(self) -> Concern:
    return self.inflate_child(
      Concern,
      prop=CONCERN_SHELL_KEY,
      safely=True
    )

  @classmethod
  def reconstruct(cls, reconstructor: Reconstructor):
    adapter: T = cls.inflate(reconstructor['adapter_ref'])

    if concern_shell_ref := reconstructor.get('concern_ref'):
      concern: Concern = Concern.inflate(concern_shell_ref)
    else:
      concern = adapter.concern_shell

    if not concern:
      sig = f"{adapter.kind()}/{adapter.id()}"
      pwar(cls, f"no concern for adapter {sig} in reconstructor", False)

    if seed := reconstructor.get('seed'):
      concern.patch({concern_module.SEED_KEY: seed})

    if concern:
      adapter.patch({'concern': concern})

    return adapter


CONCERN_SHELL_KEY = 'concern_shell'
