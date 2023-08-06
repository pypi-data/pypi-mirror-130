from typing import List

from flask import Blueprint, jsonify
from typing_extensions import TypedDict

from kama_sdk.controllers import ctrl_utils
from kama_sdk.core.telem.telem_manager import telem_manager
from kama_sdk.model.predicate.predicate import Predicate
from kama_sdk.serializers.common_serializers import ser_meta

controller = Blueprint('health', __name__)

BASE_PATH = '/api/health'


@controller.route(f"{BASE_PATH}/predicates")
def list_predicates():
  query = ctrl_utils.space_selector(False)
  all_models = Predicate.inflate_all(q=query)
  models = [p for p in all_models if p.get_title()]
  serialized = list(map(ser_meta, models))
  return jsonify(data=serialized)


@controller.route(f"{BASE_PATH}/history")
def list_checkups():
  checkups = telem_manager
  pass


class ResourceAssocQuery(TypedDict):
  resource_kinds: List[str]
