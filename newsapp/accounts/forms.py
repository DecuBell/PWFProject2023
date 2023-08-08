from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model
from django.utils.translation import gettext_lazy as _

from newsapp.accounts.models import Profile

UserModel = get_user_model()


class RegisterUserForm(auth_forms.UserCreationForm):

    class Meta(auth_forms.UserCreationForm.Meta):
        model = UserModel
        fields = ('email', )

    password1 = forms.CharField(
        label=_('Set Password'),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text= _("Must be at least 8 characters"),
    )

    password2 = forms.CharField(
        label=_('Confirm Password'),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text= _("Repeat password, please"),
    )

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = Profile(
            email=self.cleaned_data['email'],
            user=user,
        )

        if commit:
            profile.save()
        return user


class LoginUserForm(auth_forms.AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'ala-bala'
            })
    )


class EditUserForm(auth_forms.UserCreationForm):
    pass



