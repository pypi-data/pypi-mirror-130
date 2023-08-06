import json
from copy import deepcopy
from datetime import datetime
from typing import Optional, List, Dict

from kama_sdk.core.core.config_man import config_man
from kama_sdk.core.core.types import KamafileBackup
from kama_sdk.core.telem.telem_backend import TelemBackend
from kama_sdk.core.telem.telem_manager import telem_manager
from kama_sdk.utils.logging import lwar
from kama_sdk.utils.utils import safely


backups_coll_id = 'config_backups'


def serialize_for_storage(backup: KamafileBackup) -> Dict:
  serialized: Dict = deepcopy(backup)
  if isinstance(serialized.get('data'), dict):
    as_str = safely(lambda: json.dumps(serialized.get('data')), '{}')
    serialized['data'] = as_str
  return serialized


def deserialize_from_storage(backup: Dict) -> KamafileBackup:
  data_dict = safely(lambda: json.loads(backup.get('data')), {})
  return {**backup, 'data': data_dict}


def create(backup: KamafileBackup) -> Optional[KamafileBackup]:
  if backend := get_backend():
    sanitized_record = serialize_for_storage(backup)
    return backend.create_record(backups_coll_id, sanitized_record)

def create_default(trigger=None) -> Optional[KamafileBackup]:
  backup = generate_default(trigger)
  return create(backup)


def get_all() -> List[KamafileBackup]:
  if backend := get_backend():
    records = backend.query_collection(backups_coll_id, {})
    return list(map(deserialize_from_storage, records))
  else:
    return []


def find_by_id(_id: str) -> Optional[KamafileBackup]:
  if backend := get_backend():
    if raw_record := backend.find_record_by_id(backups_coll_id, _id):
      return deserialize_from_storage(raw_record)
    else:
      lwar(f"no such backup {_id}")
      return None
  else:
    return None


def generate_default(trigger=None) -> KamafileBackup:
  config = config_man.read_spaces()
  return KamafileBackup(
    trigger=trigger or TRIGGER_AUTO,
    data=config,
    timestamp=str(datetime.now())
  )


def drop_all():
  if backend := get_backend():
    backend.drop_collection(backups_coll_id)


def can_persist() -> bool:
  return False


def get_backend() -> Optional[TelemBackend]:
  return telem_manager.get_backend()


TRIGGER_AUTO = 'backup_action'
TRIGGER_USER = 'user'
