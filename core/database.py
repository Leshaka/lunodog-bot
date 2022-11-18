import traceback
from sys import exit
from os.path import isdir
from tortoise import Tortoise

from . import cfg
from .migrations import Versioning


class Database:

    __models__ = []

    TORTOISE_CONFIG = {
        'connections': {
            'default_conn': cfg.TORTOISE_DATABASE
        },
        'apps': {
            'default_app': {
                'default_connection': 'default_conn',
                'models': ['core.database', 'core.migrations', 'aerich.models']
            },
        }
    }

    @classmethod
    def model(cls, model_class: callable) -> callable:
        """ Decorator for adding a Tortoise model """
        if type(model_class.__dict__.get('Meta').__dict__.get('__version__')) is not int:
            raise ValueError("Model must have Meta class with integer __version__ attribute")
        cls.__models__.append(model_class)
        return model_class

    @classmethod
    async def init(cls):
        """ Prepare cls and init database connection """

        # Init tortoise config
        await Tortoise.init(cls.TORTOISE_CONFIG)

        # Init aerich migrations on first launch
        if not isdir('migrations'):
            await Versioning.create_migrations(cls.TORTOISE_CONFIG, 'default_app')

        # Compare current Models versions with last saved
        if await Versioning.check_versions(cls.__models__) is False:
            try:
                await Versioning.update_schema(cls.TORTOISE_CONFIG, 'default_app')
            except:
                traceback.print_exc()
            else:
                await Versioning.write_versions(cls.__models__)
                print('Database schema updated. Please restart the application.')
            finally:
                await cls.close()
                exit(0)

        # Create database tables if necessary
        await Tortoise.generate_schemas()

        # After everything is done save models versions info
        await Versioning.write_versions(cls.__models__)

    @staticmethod
    async def close():
        await Tortoise.close_connections()


__models__ = Database.__models__  # Necessary for Tortoise to detect the models
