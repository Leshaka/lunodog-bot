""" Factory for defining user configs """
from __future__ import annotations
from tortoise import Model, fields
from nextcord import Guild

from core import Db, Log


class ConfigTable(Model):
    """ Base config table class for tortoise, this is here for annotations """

    cfg_id = fields.IntField(pk=True)
    cfg_name = fields.CharField(max_length=64)
    cfg_info = fields.JSONField(default={})
    cfg_data = fields.JSONField(default={})


class CfgFactory:

    def __init__(
        self,
        name: str,
        variables: list,
        display: str = None,  # How config will be shown in the UI
        icon: str = None,  # Icon path for the UI
        table_name: str = None,  # Useful in case you need to use single table for different class objects configs
    ):

        self.name = name
        self.display = display or name
        self.icon = icon or 'default'
        self.variables = {v.name: v for v in variables}

        # Generate tortoise Model class for this CfgFactory and save it inside this class object
        @Db.model
        class _ConfigTable(ConfigTable):
            class Meta:
                __version__ = 1
                table = table_name or name

        self.table = _ConfigTable

    async def spawn(self, guild: Guild, cfg_id: int) -> Config:
        """ Load or create default config with given cfg_id """

        if (row := await self.table.get_or_none(cfg_name=self.name, cfg_id=cfg_id)) is not None:
            return await Config.new(self, guild, row)
        return await Config.new(self, guild, self.table(cfg_id=cfg_id, cfg_name=self.name))


class Config:

    @classmethod
    async def new(cls, factory: CfgFactory, guild: Guild, row: ConfigTable) -> Config:

        config = cls(factory, row)
        for var in config._factory.variables:
            try:
                obj = await var.from_json(row.cfg_data.get(var.name, var.default), guild)
            except Exception as e:
                Log.error("Failed to wrap variable '{}': {}".format(var.name, str(e)))
                obj = await var.from_json(var.default, guild)
            setattr(config, var.name, obj)

        return config

    def __init__(self, factory, row):
        self._factory = factory
        self.row = row

    async def update(self, guild: Guild, data: dict):
        # Validate data and save as useful objects in a dict
        objects = dict()
        for name, value in data.items():
            if name not in self._factory.variables.keys():
                raise KeyError(f"Variable '{name}' not found.")
            vo = self._factory.variables[name]
            data[name] = await vo.validate(value, guild)  # this may raise ValueError
            objects[name] = await vo.wrap(data[name], guild)
            vo.verify(objects[name])

        # Update self attributes
        on_change_triggers = set()
        for key, value in data.items():
            vo = self._factory.variables[key]
            setattr(self, key, objects[key])
            if vo.on_change:
                on_change_triggers.add(vo.on_change)

        # Save to DB
        self.row.cfg_data = self.jsonify()
        await self.row.save()

        # Trigger on_change events
        for f in on_change_triggers:
            f(self)  # TODO: maybe await f(self)

    def jsonify(self) -> dict:
        data = {name: var.jsonify(getattr(self, name)) for name, var in self._factory.variables.items()}
        return data

    async def delete(self):
        await self.row.delete()
