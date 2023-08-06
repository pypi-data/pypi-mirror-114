from __future__ import annotations

import os
from abc import ABCMeta, abstractmethod
from datetime import datetime
from sqlite3 import connect
from typing import Any, Union

from inject import autoparams

from ytrssil.config import Configuration
from ytrssil.constants import config_dir
from ytrssil.datatypes import Channel, Video


class ChannelNotFound(Exception):
    pass


class ChannelRepository(metaclass=ABCMeta):
    @abstractmethod
    def __enter__(self) -> ChannelRepository:
        pass

    @abstractmethod
    def __exit__(
        self,
        exc_type: Any,
        exc_value: Any,
        exc_traceback: Any,
    ) -> None:
        pass

    @abstractmethod
    def get_channel(self, channel_id: str) -> Channel:
        pass

    @abstractmethod
    def create_channel(self, channel: Channel) -> None:
        pass

    @abstractmethod
    def add_new_video(self, channel: Channel, video: Video) -> None:
        pass

    @abstractmethod
    def update_video(self, video: Video, watched: bool) -> None:
        pass


class SqliteChannelRepository(ChannelRepository):
    def __init__(self) -> None:
        os.makedirs(config_dir, exist_ok=True)
        self.file_path: str = os.path.join(config_dir, 'channels.db')
        self.setup_database()

    def setup_database(self) -> None:
        connection = connect(self.file_path)
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = ON')
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS channels ('
            'channel_id VARCHAR PRIMARY KEY, name VARCHAR, url VARCHAR UNIQUE)'
        )
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS videos ('
            'video_id VARCHAR PRIMARY KEY, name VARCHAR, url VARCHAR UNIQUE, '
            'timestamp VARCHAR, watched BOOLEAN, channel_id VARCHAR, '
            'FOREIGN KEY(channel_id) REFERENCES channels(channel_id))'
        )
        connection.commit()
        connection.close()

    def __enter__(self) -> ChannelRepository:
        self.connection = connect(self.file_path)
        return self

    def __exit__(
        self,
        exc_type: Any,
        exc_value: Any,
        exc_traceback: Any,
    ) -> None:
        self.connection.close()

    def get_channel_as_dict(self, channel: Channel) -> dict[str, str]:
        return {
            'channel_id': channel.channel_id,
            'name': channel.name,
            'url': channel.url,
        }

    def get_video_as_dict(self, video: Video, watched: bool) -> dict[str, Any]:
        return {
            'video_id': video.video_id,
            'name': video.name,
            'url': video.url,
            'timestamp': video.timestamp.isoformat(),
            'watched': watched,
            'channel_id': video.channel_id,
        }

    def get_videos(self, channel: Channel) -> list[tuple[Video, bool]]:
        cursor = self.connection.cursor()
        cursor.execute(
            'SELECT video_id, name, url, timestamp, watched '
            'FROM videos WHERE channel_id=:channel_id',
            {'channel_id': channel.channel_id},
        )
        ret: list[tuple[Video, bool]] = []
        video_data: tuple[str, str, str, str, bool]
        for video_data in cursor.fetchall():
            ret.append((
                Video(
                    video_id=video_data[0],
                    name=video_data[1],
                    url=video_data[2],
                    timestamp=datetime.fromisoformat(video_data[3]),
                    channel_id=channel.channel_id,
                    channel_name=channel.name,
                ),
                video_data[4]
            ))

        return ret

    def get_channel(self, channel_id: str) -> Channel:
        cursor = self.connection.cursor()
        cursor.execute(
            'SELECT * FROM channels WHERE channel_id=:channel_id',
            {'channel_id': channel_id},
        )
        channel_data: Union[tuple[str, str, str], None] = cursor.fetchone()
        if channel_data is None:
            raise ChannelNotFound

        channel = Channel(
            channel_id=channel_data[0],
            name=channel_data[1],
            url=channel_data[2],
        )
        for video, watched in self.get_videos(channel):
            if watched:
                channel.watched_videos[video.video_id] = video
            else:
                channel.new_videos[video.video_id] = video

        return channel

    def create_channel(self, channel: Channel) -> None:
        cursor = self.connection.cursor()
        cursor.execute(
            'INSERT INTO channels VALUES (:channel_id, :name, :url)',
            self.get_channel_as_dict(channel),
        )
        self.connection.commit()

    def update_channel(self, channel: Channel) -> None:
        cursor = self.connection.cursor()
        cursor.execute(
            'UPDATE channels SET channel_id = :channel_id, name = :name, '
            'url = :url WHERE channel_id=:channel_id',
            self.get_channel_as_dict(channel),
        )
        self.connection.commit()

    def add_new_video(self, channel: Channel, video: Video) -> None:
        cursor = self.connection.cursor()
        cursor.execute(
            'INSERT INTO videos VALUES '
            '(:video_id, :name, :url, :timestamp, :watched, :channel_id)',
            self.get_video_as_dict(video, False),
        )
        self.connection.commit()

    def update_video(self, video: Video, watched: bool) -> None:
        cursor = self.connection.cursor()
        cursor.execute(
            'UPDATE videos SET watched = :watched WHERE video_id=:video_id',
            {'watched': watched, 'video_id': video.video_id},
        )
        self.connection.commit()


@autoparams()
def create_channel_repository(config: Configuration) -> ChannelRepository:
    repo_type = config.channel_repository_type
    if repo_type == 'sqlite':
        return SqliteChannelRepository()
    else:
        raise Exception(f'Unknown channel repository type: "{repo_type}"')
