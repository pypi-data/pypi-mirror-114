from collections.abc import Iterator
from datetime import datetime, timezone
from operator import attrgetter
from os import execv, fork
from subprocess import PIPE, Popen
from sys import argv, stderr

from inject import autoparams

from ytrssil.bindings import setup_dependencies
from ytrssil.constants import mpv_options
from ytrssil.datatypes import Video
from ytrssil.fetch import Fetcher
from ytrssil.repository import ChannelRepository


def user_query(videos: dict[str, Video], reverse: bool = False) -> list[Video]:
    p = Popen(
        ['fzf', '-m'],
        stdout=PIPE,
        stdin=PIPE,
    )
    video_list: Iterator[Video]
    if reverse:
        video_list = reversed(videos.values())
    else:
        video_list = iter(videos.values())

    input_bytes = '\n'.join(map(str, video_list)).encode('UTF-8')
    stdout, _ = p.communicate(input=input_bytes)
    videos_str: list[str] = stdout.decode('UTF-8').strip().split('\n')
    ret: list[Video] = []
    for video_str in videos_str:
        *_, video_id = video_str.split(' - ')

        try:
            ret.append(videos[video_id])
        except KeyError:
            pass

    return ret


@autoparams()
def watch_videos(
    repository_manager: ChannelRepository,
    fetcher: Fetcher,
) -> int:
    with repository_manager as repository:
        channels, new_videos = fetcher.fetch_new_videos()
        if not new_videos:
            print('No new videos', file=stderr)
            return 1

        selected_videos = user_query(new_videos)
        if not selected_videos:
            print('No video selected', file=stderr)
            return 2

        video_urls = [video.url for video in selected_videos]
        cmd = ['/usr/bin/mpv', *mpv_options, *video_urls]
        if (fork() == 0):
            execv(cmd[0], cmd)

        for video in selected_videos:
            selected_channel = channels[video.channel_id]
            selected_channel.mark_video_as_watched(video)
            watch_timestamp = datetime.utcnow().replace(tzinfo=timezone.utc)
            repository.update_video(video, watch_timestamp)

    return 0


@autoparams()
def watch_history(
    repository_manager: ChannelRepository,
    fetcher: Fetcher,
) -> int:
    with repository_manager as repository:
        watched_videos = repository.get_watched_videos()
        selected_videos = user_query(watched_videos, reverse=True)
        if not selected_videos:
            print('No video selected', file=stderr)
            return 1

        video_urls = [video.url for video in selected_videos]
        cmd = ['/usr/bin/mpv', *mpv_options, *video_urls]
        if (fork() == 0):
            execv(cmd[0], cmd)

    return 0


@autoparams()
def mark_as_watched(
    repository_manager: ChannelRepository,
    fetcher: Fetcher,
    up_to_date: datetime
) -> int:
    with repository_manager as repository:
        channels, new_videos = fetcher.fetch_new_videos()
        for video in sorted(new_videos.values(), key=attrgetter('timestamp')):
            if video.timestamp >= up_to_date:
                continue

            selected_channel = channels[video.channel_id]
            selected_channel.mark_video_as_watched(video)
            watch_timestamp = datetime.utcnow().replace(tzinfo=timezone.utc)
            repository.update_video(video, watch_timestamp)

    return 0


def main() -> int:
    setup_dependencies()
    command: str
    try:
        command = argv[1]
    except IndexError:
        command = 'watch'

    if command == 'watch':
        return watch_videos()
    elif command == 'history':
        return watch_history()
    elif command == 'mark':
        up_to_date = datetime.fromisoformat(argv[2])
        return mark_as_watched(up_to_date=up_to_date)
    else:
        print(f'Unknown command "{command}"', file=stderr)
        return 1
