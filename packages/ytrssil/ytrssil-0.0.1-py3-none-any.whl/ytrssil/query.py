from subprocess import PIPE, Popen

from ytrssil.datatypes import Video


def query(videos: dict[str, Video]) -> list[Video]:
    p = Popen(
        ['fzf', '-m'],
        stdout=PIPE,
        stdin=PIPE,
    )
    input_bytes = '\n'.join(map(str, videos.values())).encode('UTF-8')
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
