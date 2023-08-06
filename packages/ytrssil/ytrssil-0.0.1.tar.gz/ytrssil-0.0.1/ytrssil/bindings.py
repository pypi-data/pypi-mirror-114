from inject import Binder, configure

from ytrssil.config import Configuration
from ytrssil.parser import Parser, create_feed_parser
from ytrssil.repository import ChannelRepository, create_channel_repository


def dependency_configuration(binder: Binder) -> None:
    config = Configuration()
    binder.bind(Configuration, config)
    binder.bind_to_provider
    binder.bind_to_constructor(ChannelRepository, create_channel_repository)
    binder.bind_to_constructor(Parser, create_feed_parser)


def setup_dependencies() -> None:
    configure(dependency_configuration)
