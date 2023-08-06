import os
from collections.abc import Iterator
from dataclasses import dataclass

from ytrssil.constants import config_dir


@dataclass
class Configuration:
    channel_repository_type: str = 'sqlite'
    fetcher_type: str = 'aiohttp'
    feed_parser_type: str = 'feedparser'


def get_feed_urls() -> Iterator[str]:
    file_path = os.path.join(config_dir, 'feeds')
    with open(file_path, 'r') as f:
        for line in f:
            yield line.strip()
