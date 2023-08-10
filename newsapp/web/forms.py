from django import forms

from newsapp.articles.form_mixins import DisabledFieldsFormMixin, BootstrapFormMixin
from newsapp.web.models import Ads


class CreateAdForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        ad = super().save(commit=False)
        ad.author_id = self.user.pk
        if commit:
            ad.save()
            return ad

    class Meta:
        model = Ads
        fields = ['title', 'body', 'phone_number', 'category']


class AdDeleteForm(BootstrapFormMixin, DisabledFieldsFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        self._init_disabled_fields()

    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = Ads
        fields = '__all__'
