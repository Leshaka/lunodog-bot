# -*- coding: utf-8 -*-
import ssl
from aiohttp_middlewares import cors_middleware
from aiohttp import web

from core import cfg, Log


class ApiServer:

    app = web.Application(
        middlewares=[cors_middleware(allow_all=True, allow_credentials=True)]
    )
    runner = web.AppRunner(app)

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(
        certfile=cfg.API_SSL_CERT_FILE,
        keyfile=cfg.API_SSL_KEY_FILE
    )

    @classmethod
    async def start(cls):
        await cls.runner.setup()
        site = web.TCPSite(cls.runner, cfg.API_HOST, cfg.API_PORT, ssl_context=cls.context)
        await site.start()
        Log.info(f'API| Serving at https://{cfg.API_HOST}:{cfg.API_PORT}')
