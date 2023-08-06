from peewee import SqliteDatabase

from kama_sdk.model.delegate.telem_db_delegate import TelemDbDelegate

DATABASE_FNAME = '/tmp/nmachine-telem-file-db'

class FileTelemDbDelegate(TelemDbDelegate):

  def connect(self) -> SqliteDatabase:
    return SqliteDatabase(DATABASE_FNAME, pragmas={})
    # return SqliteDatabase(DATABASE_FNAME, pragmas={
    #   'journal_mode': 'wal',
    #   'cache_size': -1024 * 64
    # })


ID_COL = "_id"
