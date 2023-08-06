import asyncio
from dataclasses import dataclass


@dataclass
class Source:
    name: str
    user: str


@dataclass
class Event:
    name: str
    data: dict
    source: Source


class EventPool:
    queue: asyncio.Queue
    closed: asyncio.Event

    def __init__(self):
        self.queue = asyncio.Queue()
        self.closed = asyncio.Event()

    async def put(self, event: Event):
        if not self.closed.is_set():
            await self.queue.put(event)

    async def get(self) -> Event:
        if not self.closed.is_set():
            # FIXME this probably locks when an empty queue is closed see #1
            event = await self.queue.get()
            self.queue.task_done()
            return event
        raise NotImplementedError()

    async def has_events(self) -> bool:
        return not (self.closed.is_set() and self.queue.empty())

    def close(self):
        self.closed.set()

    async def join(self):
        await self.closed.wait()
        await self.queue.join()
