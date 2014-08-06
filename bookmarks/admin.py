from django.contrib import admin
from bookmarks.models import Bookmark


class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ('user__first_name', 'user__last_name')
    ordering = ['-created_date']

admin.site.register(Bookmark, BookmarkAdmin)
