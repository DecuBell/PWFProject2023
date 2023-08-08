from django.urls import path, include

from newsapp.articles.views import ArticlesView, ArticlesCreateView, SingleArticleView, EditArticleView, \
    DeleteArticleView

urlpatterns = [
    path('list', ArticlesView.as_view(), name='articles list'),
    path('create', ArticlesCreateView.as_view(), name='article create'),
    path('<int:pk>/', include([
        path('', SingleArticleView.as_view(), name='article details'),
        path('edit', EditArticleView.as_view(), name='article edit'),
        path('delete', DeleteArticleView.as_view(), name='article delete'),
    ])
         )
]
