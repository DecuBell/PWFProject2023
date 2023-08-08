from django.urls import path

from newsapp.web.views import MainPageView

urlpatterns = [
    path('', MainPageView.as_view(), name='index'),
]