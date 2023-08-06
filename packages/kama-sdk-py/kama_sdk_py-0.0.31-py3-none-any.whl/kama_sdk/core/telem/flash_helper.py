import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List


flash_path = '/tmp/nmachine-telem-flash.json'


def fname(**kwargs) -> str:
  return kwargs.get('fname') or flash_path


def prep_open_flash(**kwargs):
  file_ptr = Path(fname(**kwargs))
  if not file_ptr.exists():
    file_ptr.touch(exist_ok=True)

def clear(**kwargs):
  file_ptr = Path(fname(**kwargs))
  if file_ptr.exists():
    os.remove(fname(**kwargs))


def write_collection(coll_id: str, records: List[Dict], **kwargs):
  prep_open_flash(**kwargs)
  with open(fname(**kwargs), 'w+') as file:
    contents: Dict = json.loads(file.read() or '{}')
    contents[coll_id] = records
    file.write(json.dumps(contents))


def read_collection(coll_id: str, **kwargs) -> List[Dict]:
  prep_open_flash(**kwargs)
  with open(fname(**kwargs), 'r') as file:
    contents: Dict = json.loads(file.read() or '{}')
    return contents.get(coll_id, [])


def push_record(coll_id: str, record: Dict, **kwargs):
  collection = read_collection(coll_id, **kwargs)
  new_collection = [*collection, sanitize_item(record)]
  write_collection(coll_id, new_collection, **kwargs)


def sanitize_item(record: Dict) -> Dict:
  new_record = {}
  for key, value in record.items():
    if isinstance(value, Dict):
      new_record[key] = json.dumps(value)
    elif isinstance(value, datetime):
      new_record[key] = str(value)
    else:
      new_record[key] = value
  return new_record
