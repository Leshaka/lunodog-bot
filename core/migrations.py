""" Versioning for Tortoise models and database migrations with aerich """

import logging
from tortoise import Model, fields
from aerich import Command as aeCommand


class Versioning(Model):

    class Meta:
        table = '__versions__'
        app = 'default_app'

    table_name = fields.CharField(max_length=256, pk=True)
    version = fields.IntField()

    @classmethod
    async def check_versions(cls, models: list[Model]) -> bool:
        """ Return True if model versions are up-to-date, else return False """

        return all([
            (ver := await cls.get_or_none(table_name=m._meta.db_table)) is None or ver.version == m.Meta.__version__
            for m in models
        ])

    @classmethod
    async def write_versions(cls, models: list[Model]):
        """ Save model versions to the db """

        for m in models:
            await cls.update_or_create(defaults=dict(version=m.Meta.__version__), table_name=m._meta.db_table)

    @classmethod
    async def create_migrations(cls, tortoise_config: dict, tortoise_app: str):
        """ Init aerich migration tool (creates ./migrations folder) """

        print('Initializing aerich migrations...')
        cmd = aeCommand(tortoise_config=tortoise_config, app=tortoise_app)
        await cmd.init()
        await cmd.init_db(safe=True)

    @classmethod
    async def update_schema(cls, tortoise_config: dict, tortoise_app: str):
        """ Run aerich to update database schema """

        if input(
            "Database schema update is needed, please backup you database. Type 'y' to proceed... "
        ).lower() != 'y':
            raise ValueError('Aborted')

        logging.basicConfig(format='%(levelname)s:%(name)s:%(message)s', level=logging.DEBUG)
        cmd = aeCommand(tortoise_config=tortoise_config, app=tortoise_app)
        await cmd.init()
        await cmd.migrate()
        await cmd.upgrade()
