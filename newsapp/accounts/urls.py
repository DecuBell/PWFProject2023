from django.urls import path, include

from newsapp.accounts.views import UserLoginView, UserLogoutView, UserRegistrationView, UserDetailsView, UserEditView, \
    UserDeleteView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login user'),
    path('logout/', UserLogoutView.as_view(), name='logout user'),
    path('register/', UserRegistrationView.as_view(), name='register user'),
    path('details/<int:pk>/', include([
        path('', UserDetailsView.as_view(), name='profile details'),
        path('edit/', UserEditView.as_view(), name='profile edit'),
        path('delete/', UserDeleteView.as_view(), name='profile delete'),
    ])
         )
]
