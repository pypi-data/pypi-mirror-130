from typing import List

from kama_sdk.core.core.types import EventCapture, HealthRun, HealthRunQuery
from kama_sdk.core.telem.telem_manager import telem_manager
from kama_sdk.model.action.base.action_consts import HEALTH_CHECK_EVENT_TYPE
from kama_sdk.model.base.mc import SPACE_KEY


def get_runs(query: HealthRunQuery) -> List[HealthRun]:
  from kama_sdk.model.predicate.predicate import Predicate
  matching_predicates = runs_query2preds(query)
  matching_predicates_ids = list(map(Predicate.get_id, matching_predicates))
  occurred_at_lt = query.get('occurred_at_lt')
  occurred_at_gt = query.get('occurred_at_gt')

  events_query = dict(
    type=HEALTH_CHECK_EVENT_TYPE,
    outcome=query.get('outcome'),
    nesting_depth=query.get('nesting_depth'),
    initiator_id=matching_predicates_ids,
    occurred_at=to_range(occurred_at_lt, occurred_at_gt)
  )

  telem_manager.get_backend().query_collection()


def runs_query2preds(query: HealthRunQuery) -> List['Predicate']:
  from kama_sdk.model.predicate.predicate import Predicate
  from kama_sdk.model.predicate.predicate import SEVERITY_KEY
  severity, space = query.get('space'), query.get('severity')
  pred_query = {SPACE_KEY: space, SEVERITY_KEY: severity}
  return Predicate.inflate_all(q=pred_query)


def to_range(lt: str, gt: str) -> range:
  pass


def event_cap2checkrec(event_capture: EventCapture) -> HealthRun:
  return HealthRun(
    parent_id=event_capture.get("parent_vid")
  )
