from django.contrib import admin

from mailing.models import User, Message, MailingLog, Schedule


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name','patronymic' , 'email', 'is_active',
                    'created_at', 'modified_date')
    list_filter = ('created_at',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'text','created_at', 'modified_date')
    list_filter = ('created_at',)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('description', 'start_date', 'end_date', 'periodic', 'time', 'day_of_week',
                    'day_of_month', 'message', 'status', 'is_active', 'created_at', 'modified_date')
    list_filter = ('start_date',)


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('date_of_last_attempt', 'status_of_last_attempt', 'server_response', 'schedule')
    list_filter = ('date_of_last_attempt',)
