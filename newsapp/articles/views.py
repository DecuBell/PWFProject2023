from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from newsapp.articles.forms import CreateArticleForm, ArticleDeleteForm
from newsapp.articles.models import Article
from newsapp.comments.forms import CommentForm
from newsapp.comments.models import Comment

UserModel = get_user_model()


class ArticlesCreateView(UserPassesTestMixin, LoginRequiredMixin, views.CreateView):
    template_name = 'articles/article_create.html'
    form_class = CreateArticleForm
    success_url = reverse_lazy('articles list')

    def test_func(self):
        return any([
            self.request.user.groups.filter(name='Editorial').exists(),
            self.request.user.groups.filter(name='Journalist').exists(),
            self.request.user.is_staff,
            self.request.user.is_superuser,
        ])

    def handle_no_permission(self):
        return HttpResponseForbidden("You do not have permission to access this page.")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ArticlesView(views.ListView):
    paginate_by = 4
    model = Article
    template_name = 'articles/articles_list.html'
    ordering = ['-publish_date', '-id']
    is_editor = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_editor'] = any([self.request.user.groups.filter(name='Editorial').exists(), self.request.user.is_staff, self.request.user.is_superuser])
        # context['is_journalist'] = self.request.user.groups.filter(name='Journalist').exists()
        context['general_crime'] = len(Article.objects.filter(category="General crime"))
        context['local_news'] = len(Article.objects.filter(category="Local news"))
        context['good_news'] = len(Article.objects.filter(category="Good news"))
        context['politics'] = len(Article.objects.filter(category="Politics"))
        context['street_reporters'] = len(Article.objects.filter(category="Street reporters"))

        return context


class SingleArticleView(views.DetailView):
    model = Article
    template_name = 'articles/single_article.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.object.user == self.request.user
        context['article_author'] = self.object.user.profile.full_name
        article = self.object
        comments = Comment.objects.filter(article=article)
        comment_form = CommentForm()

        context['comments'] = comments
        context['comment_form'] = comment_form
        context['form'] = CommentForm(request=self.request)
        return context

    def post(self, request, *args, **kwargs):
        article = self.get_object()  # Get the article object
        comment_form = CommentForm(request.POST, request=request)

        if comment_form.is_valid():
            comment = comment_form
            # comment.profile = comment_form.request.user.pk  # Assuming your user profile is linked to the user
            comment.instance.article_id = article.pk
            comment.instance.author_id = comment_form.request.user.pk
            comment.save()
            return HttpResponseRedirect(reverse('article details', kwargs={'pk': article.pk}))

        # If the form is not valid, re-render the detail view with errors
        context = self.get_context_data()
        context['comment_form'] = comment_form
        return self.render_to_response(context)

    # def form_valid(self, form):
    #     item = form.save()
    #     self.pk = item.pk
    #     return super().form_valid(form)

    def get_success_url(self):
        return reverse('article details', kwargs={'pk': self.pk})


class EditArticleView(UserPassesTestMixin, LoginRequiredMixin, views.UpdateView):
    model = Article
    fields = ('header_image', 'title', 'category', 'body')
    template_name = 'articles/article_edit.html'

    def test_func(self):
        article = self.get_object()
        return any([
            self.request.user.groups.filter(name='Editorial').exists(),
            self.request.user.is_staff,
            self.request.user.is_superuser,
            article.user == self.request.user
        ])

    def handle_no_permission(self):
        return HttpResponseForbidden("You do not have permission to access this page.")

    def form_valid(self, form):
        item = form.save()
        self.pk = item.pk
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('article details', kwargs={'pk': self.pk})


class DeleteArticleView(UserPassesTestMixin, LoginRequiredMixin, views.DeleteView):
    model = Article
    template_name = 'articles/article_delete.html'
    form_class = ArticleDeleteForm

    success_url = reverse_lazy('index')

    def test_func(self):
        article = self.get_object()
        return any([
            self.request.user.groups.filter(name='Editorial').exists(),
            self.request.user.is_staff,
            self.request.user.is_superuser,
            article.user == self.request.user
        ])

    def handle_no_permission(self):
        return HttpResponseForbidden("You do not have permission to access this page.")

    def get_success_url(self):
        if self.success_url:
            return self.success_url

        return super().get_success_url()

    def get_initial(self):
        article = self.get_object()
        return {'title': article.title,
                'body': article.body}
