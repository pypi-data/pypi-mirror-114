import asyncio
import importlib
from typing import List

import aiohttp_jinja2
import jinja2
from aiohttp import web
from mahiru.core.event import Event, EventPool
from mahiru.core.module import Module


class Heart:
    modules: List[Module]
    event_pool: EventPool
    web_app: web.Application
    web_runner: web.AppRunner
    web_site: web.TCPSite
    __consumer: asyncio.Task

    def __init__(self):
        self.modules = []
        self.event_pool = EventPool()
        self.web_app = web.Application()
        self.__consumer = asyncio.create_task(self.route_events())

    async def initialize(self, config: dict):
        module = ControlModule(self.event_pool, self)
        await module.start()
        self.modules.append(module)

        for i, name in enumerate(config):
            print(f'initializing {name} ({i + 1}/{len(config)})')
            py_module = importlib.import_module(f'.{name}', 'mahiru')
            module = py_module.initialize(self.event_pool, **config[name])
            await module.start()
            self.modules.append(module)

    async def run(self):
        loaders = []
        all_routes = []
        for module in self.modules:
            loader, routes = module.get_routes()
            if loader:
                loaders.append(loader)
            all_routes += routes
        aiohttp_jinja2.setup(self.web_app, loader=jinja2.ChoiceLoader(loaders))
        self.web_app.add_routes(all_routes)
        self.web_runner = web.AppRunner(self.web_app)
        await self.web_runner.setup()
        self.web_site = web.TCPSite(self.web_runner, '0.0.0.0', 8080)
        await self.web_site.start()
        print('all running')

    async def route_events(self):
        while self.event_pool.has_events():
            event = await self.event_pool.get()
            if event:
                for module in self.modules:
                    await module.consume(event)

    async def shutdown(self):
        # TODO send shutdown command to modules
        self.event_pool.close()

    async def join(self):
        await self.event_pool.join()
        await self.web_runner.cleanup()


class ControlModule(Module):
    heart: Heart

    def __init__(self, event_pool: EventPool, heart: Heart):
        super().__init__(event_pool)
        self.heart = heart

    async def consume(self, event: Event):
        if event.name == 'shutdown':
            await self.heart.shutdown()
