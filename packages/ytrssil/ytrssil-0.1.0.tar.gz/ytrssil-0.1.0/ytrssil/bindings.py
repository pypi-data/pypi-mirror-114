from inject import Binder, Injector, configure, get_injector_or_die

from ytrssil.config import Configuration
from ytrssil.fetch import Fetcher, create_fetcher
from ytrssil.parse import Parser, create_feed_parser
from ytrssil.repository import ChannelRepository, create_channel_repository


def dependency_configuration(binder: Binder) -> None:
    config = Configuration()
    binder.bind(Configuration, config)
    binder.bind_to_provider
    binder.bind_to_constructor(ChannelRepository, create_channel_repository)
    binder.bind_to_constructor(Fetcher, create_fetcher)
    binder.bind_to_constructor(Parser, create_feed_parser)


def setup_dependencies() -> Injector:
    configure(dependency_configuration)

    return get_injector_or_die()
