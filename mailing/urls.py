from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import IndexView, UserListView, UserCreateView, UserUpdateView, UserDeleteView, UserDetailView

app_name = MailingConfig.name


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('users/', UserListView.as_view(), name='users'),
    path('users/create/', UserCreateView.as_view(), name='user_create'),
    path('users/update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('users/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('users/detail/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
]