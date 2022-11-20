# -*- coding: utf-8 -*-
from tortoise.models import Model
from tortoise import fields

from core import Db, Log, dc
from core import cfg_factory as cf


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


myCoolConfig = cf.CfgFactory(
    name='CoolConfig',
    variables=[
        cf.StrVar(name='cool_str'),
        cf.TextVar(name='cool_text'),
        cf.EmojiVar(name='cool_emoji'),
        cf.OptionVar(name='cool_option', options=['one', 'two']),
        cf.BoolVar(name='cool_bool'),
        cf.IntVar(name='CoolInt'),
        cf.SliderVar(name='CoolSlider'),
        cf.RoleVar(name='CoolRole'),
        cf.TextChanVar(name='CoolTextChannel'),
        cf.DurationVar(name='CoolDuration'),
        cf.VariableTable(name='CoolTable', variables=[
            cf.StrVar(name='cool_column1'),
            cf.IntVar(name='cool_column2')
        ])
    ]
)


@dc.event
async def on_ready():
    my_guild = dc.get_guild(745999774649679923)
    cfg = await myCoolConfig.spawn(guild=my_guild, cfg_id=my_guild.id)
    Log.info(f'cool_str = {cfg.cool_str}')
    Log.info(cfg.readable())
    await cfg.update(guild=my_guild, data={'cool_str': 'ololo!'})
    Log.info(f'cool_str = {cfg.cool_str}')
