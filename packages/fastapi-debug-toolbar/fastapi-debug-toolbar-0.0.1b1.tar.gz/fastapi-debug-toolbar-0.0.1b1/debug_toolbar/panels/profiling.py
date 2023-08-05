import asyncio
import typing as t

from fastapi import Request, Response
from pyinstrument import Profiler
from starlette.concurrency import run_in_threadpool
from starlette.routing import Match

from debug_toolbar.panels import Panel


def matched_endpoint(request: Request) -> t.Optional[t.Callable]:
    for route in request.app.routes:
        match, _ = route.matches(request.scope)
        if match == Match.FULL:
            return getattr(route, "endpoint", None)
    return None


class ProfilingPanel(Panel):
    title = "Profiling"
    template = "panels/profiling.html"

    async def process_request(self, request: Request) -> Response:
        self.profiler = Profiler(**self.toolbar.settings.PROFILER_OPTIONS)
        endpoint = matched_endpoint(request)

        if endpoint is None:
            return await super().process_request(request)

        is_async = asyncio.iscoroutinefunction(endpoint)

        async def call(func: t.Callable) -> None:
            await run_in_threadpool(func) if not is_async else func()

        await call(self.profiler.start)
        response = await super().process_request(request)
        await call(self.profiler.stop)
        return response

    async def generate_stats(
        self,
        request: Request,
        response: Response,
    ) -> t.Optional[t.Dict[str, t.Any]]:
        return {"content": self.profiler.output_html()}
