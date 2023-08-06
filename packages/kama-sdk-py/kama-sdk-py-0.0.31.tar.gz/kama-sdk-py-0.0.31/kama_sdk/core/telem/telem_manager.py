from __future__ import annotations

from copy import deepcopy
from typing import Optional, List

import peewee

from kama_sdk.core.core import hub_api_client
from kama_sdk.core.core.config_man import config_man
from kama_sdk.core.core.types import ErrorCapture
from kama_sdk.core.telem import flash_helper
from kama_sdk.model.base.mc import APP_SPACE
from kama_sdk.model.delegate.telem_db_delegate import TelemDbDelegate
from kama_sdk.utils.logging import lerr

synced_key = 'synced'
primary_key = '_id'

EVENTS_COLLECTION_ID = 'events'
BACKUPS_COLLECTION_ID = 'config_backups'
errors_coll_id = 'errors'


class TelemManager:
  """
  Class responsible for handling requests to register, persist, and/or
  upload telemetry data. Telemetry data may either be
  events (EventCapture schema) or errors (ErrorCapture).

  When a caller (e.g an Action) creates telemetry, it starts by calling
  `register_event/error`, which writes a serialized version of the event
  to a temporary JSON file called the "flash". The flash must be persisted
  because callers may run in different processes. A better implementation
  may be
  """

  _peewee_db: Optional[peewee.Database]

  def __init__(self):
    self._peewee_db = None

  def connect(self, force=False):
    if force or not self.is_online():
      try:
        meta_model = self.get_current_db_delegate()
        self._peewee_db = meta_model.connect()
      except Exception as e:
        lerr(f"failed to reload telem backend", exc=e)

  def disconnect(self):
    if database := self.get_database():
      try:
        database.close()
      except Exception as e:
        lerr(f"err closing db: {str(e)}, setting to None anyways")
      finally:
        self._peewee_db = None

  def get_database(self) -> peewee.Database:
    return self._peewee_db

  def set_backend_by_meta_id(self, new_meta_id: str):
    assignment = {SAVED_DELEGATE_META_KEY: new_meta_id}
    config_man.patch_prefs(assignment, space=APP_SPACE)
    self.disconnect()
    self.connect()

  def is_enabled(self) -> bool:
    return self.get_current_db_delegate() is not None

  def is_online(self) -> bool:
    if self.is_enabled():
      if self._peewee_db:
        return self._peewee_db.is_connection_usable()
    return False

  def flush_flash(self):
    backend = self.get_backend()
    for collection_id in [EVENTS_COLLECTION_ID, errors_coll_id]:
      for record in flash_helper.read_collection(collection_id):
        is_synced = upload_item(collection_id, record)
        record[synced_key] = is_synced
        if backend:
          backend.create_record(collection_id, record)
      flash_helper.write_collection(collection_id, [])

  def get_checkups(self) -> List:
    pass

  @staticmethod
  def get_current_db_delegate() -> Optional:
    prefs = config_man.read_prefs()
    if meta_model_id := prefs.get(SAVED_DELEGATE_META_KEY):
      return TelemDbDelegate.inflate(meta_model_id)

  @staticmethod
  def register_error(error: ErrorCapture):
    flash_helper.push_record(errors_coll_id, error)

  def flush_persistent_store(self):
    if backend := self.get_backend():
      for coll_id in [EVENTS_COLLECTION_ID, errors_coll_id]:
        records = backend.query_collection(coll_id, {synced_key: False})
        for record in records:
          if upload_item(coll_id, record):
            record[synced_key] = True
            backend.update_record(coll_id, record)


def upload_item(collection_name: str, item) -> bool:
  hub_key = f'kama_{collection_name}'[0:-1]
  clean_item = deepcopy(item)
  clean_item.pop(primary_key, None)
  clean_item.pop(synced_key, None)
  resp = hub_api_client.post(f'/{hub_key}s', {hub_key: clean_item})
  return resp.status_code == 400


telem_manager = TelemManager()
SAVED_DELEGATE_META_KEY = "telem-delegate-meta-key"
