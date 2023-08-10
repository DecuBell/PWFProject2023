from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from newsapp.articles.models import Article
from newsapp.web.forms import CreateAdForm, AdDeleteForm
from newsapp.web.models import Ads


class MainPageView(views.TemplateView):
    template_name = 'base/index.html'
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fetch_articles = Article.objects.all().order_by('-publish_date', '-id')
        context['can_create'] = any([
             self.request.user.groups.filter(name='Journalist').exists(),
             self.request.user.groups.filter(name='Editorial').exists(),
             self.request.user.is_staff,
             self.request.user.is_superuser
        ])
        context["last_two_articles"] = fetch_articles[:2]
        context["next_three_articles"] = fetch_articles[2:5]
        return context


class AdCreateView(LoginRequiredMixin, views.CreateView):
    template_name = 'ads/ad_create.html'
    form_class = CreateAdForm
    success_url = reverse_lazy('ad list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class AdsListView(views.ListView):
    paginate_by = 10
    model = Ads
    template_name = 'ads/ads_list.html'
    ordering = ['-publish_date', '-id']


class AdEditView(UserPassesTestMixin, LoginRequiredMixin, views.UpdateView):
    model = Ads
    fields = ('title', 'body', 'phone_number',)
    template_name = 'ads/ad_edit.html'

    def test_func(self):
        ad = self.get_object()
        return ad.user == self.request.user

    def handle_no_permission(self):
        return HttpResponseForbidden("You do not have permission to access this page.")

    def form_valid(self, form):
        item = form.save()
        self.pk = item.pk
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('ad edit', kwargs={'pk': self.pk})


class AdDeleteView(UserPassesTestMixin, LoginRequiredMixin, views.DeleteView):
    model = Ads
    template_name = 'ads/ad_delete.html'
    form_class = AdDeleteForm

    success_url = reverse_lazy('ad list')

    def test_func(self):
        ad = self.get_object()
        return any([
            self.request.user.groups.filter(name='Editorial').exists(),
            self.request.user.is_staff,
            self.request.user.is_superuser,
            ad.user == self.request.user
        ])

    def handle_no_permission(self):
        return HttpResponseForbidden("You do not have permission to access this page.")

    def get_success_url(self):
        if self.success_url:
            return self.success_url

        return super().get_success_url()

    def get_initial(self):
        ad = self.get_object()
        return {'category': ad.category,
                'title': ad.title,
                'body': ad.body,
                'phone_number': ad.phone_number,
                }
