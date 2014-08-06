from django import forms
from wiki.models import Article


class BookmarkForm(forms.Form):
    article_id = forms.IntegerField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(BookmarkForm, self).__init__(*args, **kwargs)

    def clean_article_id(self):
        data = self.cleaned_data['article_id']
        try:
            Article.objects.get(pk=data)
        except Article.DoesNotExist:
            raise forms.ValidationError('Invalid article.')
        return data

    def clean(self):
        cleaned_data = super(BookmarkForm, self).clean()

        if self.user.is_anonymous():
            raise forms.ValidationError('Invalid user.')

        a = Article.objects.get(pk=self.cleaned_data['article_id'])
        if not a.can_read(self.user):
            raise forms.ValidationError('Invalid user permissions.')

        return cleaned_data
