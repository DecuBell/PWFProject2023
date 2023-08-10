from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from newsapp.accounts.models import Profile
from newsapp.articles.models import Article
from newsapp.comments.forms import CommentForm


# Create your views here.
# @login_required
# def add_comment(request):
#     form = CommentForm(request.POST, request=request)
#     # # article = Article.objects.get(pk=object.art)
#     if request.method == 'POST':
#         form = CommentForm(request.POST, request=request)
#
#         if form.is_valid():
#             print('neshtod')
#             comment = form.save(commit=False)
#             comment.author = Profile.objects.get(user=request.user)
#             print(comment.author)
#             article_pk = form.cleaned_data['article_pk']
#             profile_pk = form.cleaned_data['profile_pk']
#             print(article_pk)
#
#             article = Article.objects.get(pk=article_pk)
#             profile = Profile.objects.get(pk=profile_pk)
#
#             comment.article = article
#             comment.profile = profile
#             comment.save()
#             return JsonResponse({'success': True})
#         else:
#             return JsonResponse({'success': False, 'errors': form.errors})
#     # else:
#     #     form = CommentForm(request=request)
#
#     return render(request, 'articles/single_article.html', {'form': form})
