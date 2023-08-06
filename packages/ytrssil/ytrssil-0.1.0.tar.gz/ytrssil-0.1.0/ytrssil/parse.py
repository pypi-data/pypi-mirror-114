from abc import ABCMeta, abstractmethod
from datetime import datetime

import feedparser
from inject import autoparams

from ytrssil.config import Configuration
from ytrssil.datatypes import Channel, Video
from ytrssil.exceptions import ChannelNotFound
from ytrssil.repository import ChannelRepository


class Parser(metaclass=ABCMeta):
    @autoparams('channel_repository')
    def __init__(self, channel_repository: ChannelRepository) -> None:
        self.repository = channel_repository

    @abstractmethod
    def __call__(self, feed_content: str) -> Channel:
        pass


class FeedparserParser(Parser):
    def __call__(self, feed_content: str) -> Channel:
        d = feedparser.parse(feed_content)
        channel_id: str = d['feed']['yt_channelid']
        try:
            channel = self.repository.get_channel(channel_id)
        except ChannelNotFound:
            channel = Channel(
                channel_id=channel_id,
                name=d['feed']['title'],
                url=d['feed']['link'],
            )
            self.repository.create_channel(channel)

        for entry in d['entries']:
            video = Video(
                video_id=entry['yt_videoid'],
                name=entry['title'],
                url=entry['link'],
                timestamp=datetime.fromisoformat(entry['published']),
                channel_id=channel.channel_id,
                channel_name=channel.name,
            )
            if channel.add_video(video):
                self.repository.add_new_video(channel, video)

        return channel


@autoparams()
def create_feed_parser(config: Configuration) -> Parser:
    parser_type = config.feed_parser_type
    if parser_type == 'feedparser':
        return FeedparserParser()
    else:
        raise Exception(f'Unknown feed parser type: "{parser_type}"')
