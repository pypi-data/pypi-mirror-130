import peewee

from kama_sdk.model.base.model import Model

class TelemDbDelegate(Model):

  def connect(self) -> peewee.Database:
    raise NotImplementedError


CLASS_FQDN_KEY = "class_fqdn"
