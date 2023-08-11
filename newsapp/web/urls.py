from django.urls import path, include

from newsapp.web.views import MainPageView, AdCreateView, AdsListView, AdEditView, \
    AdDeleteView, BuyAdsListView, SellAdsListView

urlpatterns = [
    path('', MainPageView.as_view(), name='index'),
    path('ads/', include([
        path('create', AdCreateView.as_view(), name='ad create'),
        path('list', AdsListView.as_view(), name='ad list'),
        path('buy', BuyAdsListView.as_view(), name='buy list'),
        path('sell', SellAdsListView.as_view(), name='sell list'),
        path('<int:pk>/edit', AdEditView.as_view(), name='ad edit'),
        path('<int:pk>/delete', AdDeleteView.as_view(), name='ad delete'),
    ]),
         )
]
