from abc import ABCMeta, abstractmethod
from asyncio import gather, run
from collections.abc import Iterable

from aiohttp import ClientResponse, ClientSession
from inject import autoparams

from ytrssil.config import Configuration, get_feed_urls
from ytrssil.datatypes import Channel, Video
from ytrssil.parse import Parser
from ytrssil.repository import ChannelRepository


class Fetcher(metaclass=ABCMeta):
    @abstractmethod
    def fetch_feeds(self, urls: Iterable[str]) -> Iterable[str]:
        pass

    @autoparams('parser', 'repository')
    def fetch_new_videos(
        self,
        parser: Parser,
        repository: ChannelRepository,
    ) -> tuple[dict[str, Channel], dict[str, Video]]:
        feed_urls = get_feed_urls()
        channels: dict[str, Channel] = {}
        new_videos: dict[str, Video] = {}
        for feed in self.fetch_feeds(feed_urls):
            channel = parser(feed)
            channels[channel.channel_id] = channel
            new_videos.update(channel.new_videos)

        return channels, new_videos


class AioHttpFetcher(Fetcher):
    async def request(self, session: ClientSession, url: str) -> ClientResponse:
        return await session.request(method='GET', url=url)

    async def async_fetch_feeds(self, urls: Iterable[str]) -> Iterable[str]:
        async with ClientSession() as session:
            responses: list[ClientResponse] = await gather(*[
                self.request(session, url) for url in urls
            ])
            return [
                await response.text(encoding='UTF-8')
                for response in responses
            ]

    def fetch_feeds(self, urls: Iterable[str]) -> Iterable[str]:
        return run(self.async_fetch_feeds(urls))


@autoparams()
def create_fetcher(config: Configuration) -> Fetcher:
    fetcher_type = config.fetcher_type
    if fetcher_type == 'aiohttp':
        return AioHttpFetcher()
    else:
        raise Exception(f'Unknown feed fetcher type: "{fetcher_type}"')
