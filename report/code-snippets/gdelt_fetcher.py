import asyncio
import httpx
import pandas as pd
from aio_pika import connect, Message


class GdeltFetcher:
    BASE_URL = "http://data.gdeltproject.org/gdeltv2/"
    GOLDSTEIN_THRESHOLD = -5.0

    def __init__(self, rabbit_url: str, http_timeout: float = 30.0):
        self.rabbit_url = rabbit_url
        self.client = httpx.AsyncClient(timeout=http_timeout)

    async def fetch_latest_export(self, file_name: str) -> bool:
        url = f"{self.BASE_URL}{file_name}"
        response = await self.client.get(url)
        if response.status_code != 200:
            return False
        with open(f"/tmp/{file_name}", "wb") as fp:
            fp.write(response.content)
        return True

    async def process_csv(self, path: str) -> list[str]:
        df = pd.read_csv(path, sep="\t", header=None, on_bad_lines="skip")
        critical_events = df[df[30] < self.GOLDSTEIN_THRESHOLD]
        return critical_events[0].astype(str).tolist()

    async def notify_analyzer(self, event_ids: list[str]) -> None:
        connection = await connect(self.rabbit_url)
        async with connection:
            channel = await connection.channel()
            for eid in event_ids:
                await channel.default_exchange.publish(
                    Message(eid.encode()),
                    routing_key="events_queue",
                )

    async def run(self, file_name: str) -> None:
        if not await self.fetch_latest_export(file_name):
            return
        ids = await self.process_csv(f"/tmp/{file_name}")
        if ids:
            await self.notify_analyzer(ids)
