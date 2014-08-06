from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin

from bookmarks.markdown_extensions import BookmarkExtension


class BookmarkPlugin(BasePlugin):
    markdown_extensions = [BookmarkExtension()]

registry.register(BookmarkPlugin)
