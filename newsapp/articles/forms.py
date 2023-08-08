from django import forms

from newsapp.articles.form_mixins import BootstrapFormMixin, DisabledFieldsFormMixin
from newsapp.articles.models import Article


class CreateArticleForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        article = super().save(commit=False)
        article.user = self.user
        if commit:
            article.save()
            return article

    class Meta:
        model = Article
        fields = ('header_image', 'title', 'category', 'body',)
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'Set article name here ...',
                }
            ),
            'body': forms.Textarea(
                attrs={
                    'placeholder': 'Set article body here ...',
                }
            ),
        }


class ArticleDeleteForm(BootstrapFormMixin, DisabledFieldsFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        self._init_disabled_fields()

    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = Article
        fields = ('title', 'body')
