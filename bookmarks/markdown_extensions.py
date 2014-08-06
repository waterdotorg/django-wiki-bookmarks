import markdown
import re

from django.template.loader import render_to_string
from django.template import Context
from bookmarks import models


BOOKMARKS_RE = re.compile(r'.*(\[bookmarks(\s+owner\:(?P<owner>\w+))?\s*\]).*',
                          re.IGNORECASE)


class BookmarkExtension(markdown.Extension):
    """ Bookmarks plugin markdown extension for django-wiki. """

    def extendMarkdown(self, md, md_globals):
        """ Insert BookmarkPreprocessor before ReferencePreprocessor. """
        md.preprocessors.add('dw-bookmarks',
                             BookmarkPreprocessor(md), '>html_block')


class BookmarkPreprocessor(markdown.preprocessors.Preprocessor):
    """
    django-wiki bookmark preprocessor - parse text for
    [bookmarks owner:username] references.
    """

    def run(self, lines):
        new_text = []
        bookmarks = None
        owner = None
        filter_kwargs = {}
        for line in lines:
            m = BOOKMARKS_RE.match(line)
            if m:
                owner = m.group('owner')
                if owner:
                    filter_kwargs.update({'user__username': owner.strip()})
                else:
                    continue

                bookmarks = (models.Bookmark.objects.select_related()
                             .filter(**filter_kwargs).order_by('-created_date'))
                html = render_to_string(
                    "wiki/plugins/bookmarks/fragments/bookmarks.html",
                    Context({'bookmarks': bookmarks})
                )
                html_stash = self.markdown.htmlStash.store(html, safe=True)
                line = line.replace(m.group(1), html_stash)
            new_text.append(line)
        return new_text
