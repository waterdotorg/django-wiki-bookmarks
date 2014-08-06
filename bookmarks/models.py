from django.conf import settings
from django.db import models

from wiki.models import Article


class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True)
    article = models.ForeignKey(Article)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'article')

    def __unicode__(self):
        return self.article.current_revision.title
