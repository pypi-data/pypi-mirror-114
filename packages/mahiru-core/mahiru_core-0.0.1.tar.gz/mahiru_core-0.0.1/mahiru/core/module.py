from typing import List, Tuple, Optional

from .event import Source, Event, EventPool


class Module:
    event_pool: EventPool

    def __init__(self, event_pool: EventPool):
        self.event_pool = event_pool

    def get_routes(self) -> Tuple[Optional["jinja2.BaseLoader"], List["aiohttp.web.RouteDef"]]:
        return None, []

    async def start(self):
        pass

    async def consume(self, event: Event):
        pass

    async def trigger_event(self, event_name: str, data: dict, source_name: str, source_user: str):
        source = Source(source_name, source_user)
        event = Event(event_name, data, source)
        await self.event_pool.put(event)
