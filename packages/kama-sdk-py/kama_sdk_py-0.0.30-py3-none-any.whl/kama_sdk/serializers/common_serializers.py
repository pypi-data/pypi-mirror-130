from typing import Dict

from kama_sdk.model.base.model import Model


def ser_meta(model: Model) -> Dict:
  return {
    'id': model.get_id(),
    'title': model.get_title(),
    'info': model.get_info()
  }


def ser_meta_with_space(model: Model) -> Dict:
  return {
    'id': model.get_id(),
    'title': model.get_title(),
    'info': model.get_info(),
    'space': model.get_space_id()
  }
