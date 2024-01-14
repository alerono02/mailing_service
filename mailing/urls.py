from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import IndexView, UserListView, UserCreateView, UserUpdateView, UserDeleteView, UserDetailView, \
    MessageCreateView, MessageListView, MessageUpdateView, MessageDeleteView, MessageDetailView, ScheduleListView, \
    ScheduleCreateView, ScheduleUpdateView, ScheduleDeleteView, ScheduleDetailView, toggle_active, toggle_run_pause, \
    MailingLogListView, MailingLogDetailView

app_name = MailingConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('users/', UserListView.as_view(), name='users'),
    path('users/create/', UserCreateView.as_view(), name='user_create'),
    path('users/update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('users/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('users/detail/<int:pk>/', UserDetailView.as_view(), name='user_detail'),

    path('messages/', MessageListView.as_view(), name='messages'),
    path('messages/create', MessageCreateView.as_view(), name='message_create'),
    path('messages/update/<int:pk>', MessageUpdateView.as_view(), name='message_update'),
    path('messages/detail/<int:pk>', MessageDetailView.as_view(), name='message_detail'),
    path('messages/delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),

    path('schedules/', ScheduleListView.as_view(), name='schedules'),
    path('schedules/create', ScheduleCreateView.as_view(), name='schedule_create'),
    path('schedules/update/<int:pk>', ScheduleUpdateView.as_view(), name='schedule_update'),
    path('schedules/delete/<int:pk>', ScheduleDeleteView.as_view(), name='schedule_delete'),
    path('schedules/detail/<int:pk>', ScheduleDetailView.as_view(), name='schedule_detail'),
    path('schedules/toggle_active/<int:pk>', toggle_active, name='toggle_active'),
    path('schedules/toggle_run_pause/<int:pk>', toggle_run_pause, name='toggle_run_pause'),

    path('mailing_logs/', MailingLogListView.as_view(), name='mailing_logs'),
    path('mailing_logs/view/<int:pk>', MailingLogDetailView.as_view(), name='mailing_log_view'),
]
