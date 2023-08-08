from django.views import generic as views
from newsapp.articles.models import Article


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
