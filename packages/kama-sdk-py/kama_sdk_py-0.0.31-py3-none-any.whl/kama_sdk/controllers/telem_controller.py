from datetime import datetime

from flask import Blueprint, jsonify

from kama_sdk.controllers import ctrl_utils
from kama_sdk.controllers.ctrl_utils import parse_json_body
from kama_sdk.core.core.config_man import config_man
from kama_sdk.core.core.types import KamafileBackup
from kama_sdk.core.telem import backups_manager
from kama_sdk.core.telem.backups_manager import TRIGGER_USER
from kama_sdk.core.telem.telem_manager import telem_manager
from kama_sdk.model.delegate.telem_backend_delegate_meta import TelemDbDelegate
from kama_sdk.serializers.common_serializers import ser_meta, ser_meta_with_space
from kama_sdk.serializers.telem_serializers import ser_kamafile_backup, ser_kamafile_backup_full

controller = Blueprint('telem_controller', __name__)

BASE = '/api/telem'


@controller.route(f'{BASE}/backends/current')
def get_current_backend():
  if meta := telem_manager.get_crt_meta_model_from_state():
    return ser_meta_with_space(meta)
  else:
    return jsonify(data=None)


@controller.route(f'{BASE}/backends/available')
def get_available_backends():
  models = TelemDbDelegate.inflate_all()
  serialized = list(map(ser_meta, models))
  return jsonify(data=serialized)


@controller.route(f'{BASE}/backends/current', methods=['POST'])
def update_current_by_meta_id():
  body = ctrl_utils.parse_json_body()
  new_meta_id = body.get('meta_id')
  telem_manager.set_backend_by_meta_id(new_meta_id)
  return jsonify(data="ok")


@controller.route(f'{BASE}/wipe', methods=['POST'])
def wipe_data():
  models = TelemDbDelegate.inflate_all()
  serialized = list(map(ser_meta_with_space, models))
  return jsonify(data=serialized)


@controller.route(f'{BASE}/backups/index')
def config_backups_index():
  records = backups_manager.get_all() or []
  return jsonify(data=list(map(ser_kamafile_backup, records)))


@controller.route(f'{BASE}/backups/detail/<config_id>')
def get_config_backups(config_id: str):
  if record := backups_manager.find_by_id(config_id):
    return jsonify(data=ser_kamafile_backup_full(record))
  else:
    return jsonify(error='dne'), 404


@controller.route(f'{BASE}/backups/new', methods=['POST'])
def create_config_backup():
  attrs = parse_json_body()
  backup_data = config_man.read_spaces()
  config_backup = KamafileBackup(
    name=attrs.get('name'),
    trigger=TRIGGER_USER,
    data=backup_data,
    timestamp=str(datetime.now())
  )

  backups_manager.create(config_backup)
  return jsonify(data={'status': 'success', 'record': config_backup})
