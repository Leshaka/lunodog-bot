# -*- coding: utf-8 -*-
from tortoise.models import Model
from tortoise import fields

from core import Db


@Db.model
class MyModel(Model):
    class Meta:
        __version__ = 1
        table = "MyModel"

    id = fields.IntField(pk=True)
    data = fields.CharField(max_length=128)
    headx = fields.CharField(max_length=64)

    def __str__(self):
        return f"<MyModel id={self.id}>"

