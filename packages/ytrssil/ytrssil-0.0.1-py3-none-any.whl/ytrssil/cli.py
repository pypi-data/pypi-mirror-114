from os import execv, fork
from sys import stderr

from inject import autoparams

from ytrssil.bindings import setup_dependencies
from ytrssil.constants import mpv_options
from ytrssil.fetch import fetch_new_videos
from ytrssil.query import query
from ytrssil.repository import ChannelRepository


class NoVideoSelected(Exception):
    pass


@autoparams()
def run(repository_manager: ChannelRepository) -> None:
    with repository_manager as repository:
        channels, new_videos = fetch_new_videos()
        selected_videos = query(new_videos)
        if not selected_videos:
            raise NoVideoSelected

        video_urls = [video.url for video in selected_videos]
        cmd = ['/usr/bin/mpv', *mpv_options, *video_urls]
        if (fork() == 0):
            execv(cmd[0], cmd)

        for video in selected_videos:
            selected_channel = channels[video.channel_id]
            selected_channel.mark_video_as_watched(video)
            repository.update_video(video, True)


def main() -> int:
    setup_dependencies()
    try:
        run()
    except NoVideoSelected:
        print('No video selected', file=stderr)
        return 1

    return 0


if __name__ == '__main__':
    main()
