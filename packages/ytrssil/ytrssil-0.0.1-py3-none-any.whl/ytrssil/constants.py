import os

config_prefix: str
try:
    config_prefix = os.environ['XDG_CONFIG_HOME']
except KeyError:
    config_prefix = os.path.expanduser('~/.config')

config_dir: str = os.path.join(config_prefix, 'ytrssil')
mpv_options: list[str] = [
    '--no-terminal',
    '--ytdl-format=bestvideo[height<=?1080]+bestaudio/best',
]
