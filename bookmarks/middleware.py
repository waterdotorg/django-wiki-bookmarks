from bookmarks.models import Bookmark


class BookmarksMiddleware(object):
    """
    Set bookmarks on any page
    """
    def process_request(self, request):
        if (
                request.user.is_authenticated()
                and not request.session.get('bookmarks')
            ):
            if request.session.get('bookmark_qs'):
                del request.session['bookmark_qs']

            b = (Bookmark.objects.select_related().filter(user=request.user)
                 .order_by('article__current_revision__title'))
            request.session['bookmarks_qs'] = b
            request.session['bookmarks'] = list(b.values_list('article__pk',
                                                flat=True))
        return None
