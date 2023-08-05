from flake8_plugin_utils import Plugin

from flake8_fastapi import __version__
from flake8_fastapi.visitors import CORSMiddlewareOrder, RouteDecorator, RouterPrefix


class FastAPIPlugin(Plugin):
    name = "flake8-fastapi"
    version = __version__
    visitors = [RouteDecorator, RouterPrefix, CORSMiddlewareOrder]
