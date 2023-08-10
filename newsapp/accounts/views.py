from django.conf.urls.static import static
from django.contrib.auth import views as auth_views, get_user_model, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views

from newsapp.accounts.forms import RegisterUserForm
from newsapp.accounts.models import Profile

UserModel = get_user_model()


class UserRegistrationView(views.CreateView):
    form_class = RegisterUserForm
    template_name = 'accounts/user_registration.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)

        login(self.request, self.object)

        return result

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['next'] = self.request.GET.get('next', '')

        return context

    def get_success_url(self):

        return self.request.POST.get('next', self.success_url)

    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['password1'].help_text = _('Enter your password')

    # def save(self, commit=True):
    #     user = super().save(commit=commit)
    #
    #     profile = Profile(
    #         first_name=self.cleaned_data['first_name'],
    #         user=user,
    #     )
    #
    #     if commit:
    #         profile.save()


class UserLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('index')

    def get_success_url(self):
        if self.success_url:
            return self.success_url

        return super().get_success_url()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')

        return super().dispatch(request, *args, **kwargs)


class UserLogoutView(LoginRequiredMixin, auth_views.LogoutView):
    pass


class UserDetailsView(LoginRequiredMixin, views.DetailView):
    template_name = 'accounts/profile_details.html'
    model = Profile

    profile_image = static('images/default_profile_picture.png')

    def get_profile_image(self):
        if self.object.profile_picture is not None:
            return self.object.profile_picture
        return self.profile_image

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['profile_image'] = self.get_profile_image()
        # context['articles'] = self.request.user.article_set.all()
        return context


class UserEditView(UserPassesTestMixin, LoginRequiredMixin, views.UpdateView):
    model = Profile
    fields = ('profile_picture', 'first_name', 'last_name', 'email', 'profile_description')
    template_name = 'accounts/profile_edit.html'

    def test_func(self):
        user = self.get_object()
        return any([
            self.request.user.is_staff,
            self.request.user.is_superuser,
            user.user == self.request.user
        ])

    def handle_no_permission(self):
        return HttpResponseForbidden("You do not have permission to access this page.")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['email'].widget.attrs['readonly'] = 'readonly'
        form.fields['profile_picture'].widget.attrs['placeholder'] = 'Insert picture URL'
        return form

    def form_valid(self, form):
        item = form.save()
        self.pk = item.pk
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile details', kwargs={'pk': self.pk})


class UserDeleteView(UserPassesTestMixin, LoginRequiredMixin, views.DeleteView):
    model = UserModel
    template_name = 'accounts/profile_delete.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        user = self.get_object()
        return any([
            self.request.user.is_staff,
            self.request.user.is_superuser,
            user.profile.user == self.request.user
        ])

    def handle_no_permission(self):
        return HttpResponseForbidden("You do not have permission to access this page.")
