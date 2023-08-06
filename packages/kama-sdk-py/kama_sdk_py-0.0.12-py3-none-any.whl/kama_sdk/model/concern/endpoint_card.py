from werkzeug.utils import cached_property

from kama_sdk.core.core.types import EndpointDict
from kama_sdk.model.base.model import Model


class SiteConcern(Concern):

  def endpoint_bundle(self) -> EndpointDict:
    pass

  def is_working(self) -> bool:
    pass

  def status(self) -> str:
    return "positive" if self.is_working() else "negative"

  def logo_url(self) -> str:
    return self.get_prop('logo_url')


class SiteCard(Model):

  @cached_property
  def concern(self) -> SiteConcern:
    return self.inflate_child(
      SiteConcern,
      prop='concern'
    )

  def header_desc(self):
    site_name = self.concern.title
    site_info = self.concern.info
    status = self.concern.status()
    col = "pleasant" if self.concern.is_working() else "ruby"
    logo_url = self.concern.logo_url()
    return _header_desc(site_name, status, col, logo_url, site_info)


def _header_desc(name, status, col, img, info):
  return {
    'type': 'ThreePartHeader',
    'graphic': {
      'type': 'Image',
      'uri': img
    },
    'title': {
      'type': 'Line',
      'elements': [
        {
          'type': 'Text',
          'text': name
        },
        {
          'type': 'Tag',
          'text': status,
          'style': {'bkgCol': col}
        }
      ]
    },
    'subtitle': {
      'type': 'Text',
      'text': info
    }
  }

