from dataclasses import dataclass, field
from datetime import datetime
from typing import Union


@dataclass
class Video:
    video_id: str
    name: str
    url: str
    channel_id: str
    channel_name: str
    timestamp: datetime
    watch_timestamp: Union[datetime, None] = None

    def __str__(self) -> str:
        return f'{self.channel_name} - {self.name} - {self.video_id}'


@dataclass
class Channel:
    channel_id: str
    name: str
    url: str
    new_videos: dict[str, Video] = field(default_factory=lambda: dict())
    watched_videos: dict[str, Video] = field(default_factory=lambda: dict())

    def add_video(self, video: Video) -> bool:
        if (
            video.video_id in self.watched_videos
            or video.video_id in self.new_videos
        ):
            return False

        self.new_videos[video.video_id] = video
        return True

    def remove_old_videos(self) -> None:
        vid_list: list[Video] = sorted(
            self.watched_videos.values(),
            key=lambda x: x.timestamp,
        )
        for video in vid_list[15:]:
            self.watched_videos.pop(video.video_id)

    def mark_video_as_watched(self, video: Video) -> None:
        self.new_videos.pop(video.video_id)
        self.watched_videos[video.video_id] = video
        self.remove_old_videos()

    def __str__(self) -> str:
        return f'{self.name} - {len(self.new_videos)}'
