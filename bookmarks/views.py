import simplejson

from django import http
from django.contrib.auth.decorators import login_required

from wiki.models import Article, URLPath
from bookmarks.forms import BookmarkForm
from bookmarks.models import Bookmark


@login_required
def bookmarks_ajax(request):
    response_data = {}
    response_data['success'] = False
    response_data['errors'] = ''

    if not request.method == 'POST'or not request.is_ajax():
        return http.HttpResponseForbidden('Forbidden.')

    data = request.POST
    files = request.FILES
    form = BookmarkForm(data, files, user=request.user)

    if form.is_valid():
        try:
            b = Bookmark.objects.get(article_id=form.cleaned_data.get('article_id'),
                                     user=request.user)
            b.delete()
        except Bookmark.DoesNotExist:
            b = Bookmark(article_id=form.cleaned_data.get('article_id'),
                         user=request.user)
            b.save()

        # Delete bookmarks session key so they get rebuilt on next request
        # via middleware
        if request.session.get('bookmarks'):
            del request.session['bookmarks']

        # Delete article instance cache
        a = Article.objects.get(pk=form.cleaned_data.get('article_id'))
        a.clear_cache()

        # Delete user dashboard cache if possible
        try:
            urlpath = URLPath.objects.get(slug=request.user.username)
            urlpath.article.clear_cache()
        except:
            pass

        response_data['success'] = True
    else:
        response_data['errors'] = dict((k, map(unicode, v))
                                       for (k, v) in form.errors.iteritems())

    return http.HttpResponse(simplejson.dumps(response_data),
                             mimetype='application/json; charset=UTF-8')
