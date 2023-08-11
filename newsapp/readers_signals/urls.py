from django.urls import path, include
from newsapp.readers_signals.views import SubmitSignalView

urlpatterns = [
    path('send', SubmitSignalView.as_view(), name='signals'),
]
