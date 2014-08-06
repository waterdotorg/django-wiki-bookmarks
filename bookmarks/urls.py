from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('bookmarks.views',
    url(r'^ajax/$', 'bookmarks_ajax', name='bookmarks_ajax'),
)
