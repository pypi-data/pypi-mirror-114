from typing import Awaitable, Optional
from pluginbase import PluginBase
import asyncio
import threading


def unasync_call(f, *args, **kvargs) -> None:
    def entry(f, args, kvargs):
        eventloop = asyncio.new_event_loop()
        return eventloop.run_until_complete(f(*args, **kvargs))
    th = threading.Thread(target=entry, args=(f, args, kvargs))
    th.start()
    th.join()


class PlugBox(object):
    def __init__(self):
        self.pbase = PluginBase(
            package="makru.plugins",
        )
        self.searchpaths = []
        self._source = None

    def source(self):
        if self._source:
            return self._source
        self._source = self.pbase.make_plugin_source(
            searchpath=self.searchpaths,
            persist=True,
        )
        return self._source

    def plugin_names(self):
        return self.source().list_plugins()

    def exists(self, name: str):
        return name in self.plugin_names()

    def load(self, name: str):
        return self.source().load_plugin(name)

    async def runhook_async(self, name: str, *args, **kvargs) -> None:
        """Run hook functions called `name` in all loaded plugins."""
        awaitables = []
        for n in self.plugin_names():
            p = self.load(n)
            if hasattr(p, name):
                val = getattr(p, name)(*args, **kvargs)
                if isinstance(val, Awaitable):
                    awaitables.append(val)
        if len(awaitables) > 0:
            await asyncio.gather(*awaitables)

    def runhook(self, name: str, *args, **kvargs):
        """Run hook functions called `name` in all loaded plugins.
        This is synchronous version of `.runhook_async` by running the async function in new event loop using `.run_until_complete`.

        Note on `ContextVar`: this function will run hooks in new eventloop, values in `ContextVar` could not be consistent there.

        Please use `.runhook_async` directly in async environment.
        """
        unasync_call(self.runhook_async, name, *args, **kvargs)
