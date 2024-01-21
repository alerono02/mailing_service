from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from mailing.forms import ScheduleForm
from mailing.models import User, Schedule, Message, MailingLog


class IndexView(TemplateView):
    template_name = 'mailing/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Главная'
        return context_data


class UserListView(ListView):
    model = User

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = "Пользователи"
        return context_data

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset


class UserCreateView(CreateView):
    model = User
    fields = ('name', 'surname', 'patronymic', 'email')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Добавление пользователя'
        return context_data

    def get_success_url(self):
        return reverse('mailing:users')


class UserUpdateView(UpdateView):
    model = User
    fields = ('name', 'surname', 'patronymic', 'email')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Редактирование пользователя'
        return context_data

    def get_success_url(self):
        return reverse('mailing:users')


class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('mailing:users')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Удаление пользователя'
        return context_data


class UserDetailView(DetailView):
    model = User

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = self.object
        return context_data


class MessageListView(ListView):
    model = Message

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = "Сообщения"
        return context_data

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset


class MessageCreateView(CreateView):
    model = Message
    fields = ('title', 'subject', 'text')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Создание сообщения'
        return context_data

    def get_success_url(self):
        return reverse('mailing:messages')


class MessageUpdateView(UpdateView):
    model = Message
    fields = ('title', 'subject', 'text')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'Редактирование "{self.object.title}"'
        return context_data

    def get_success_url(self):
        return reverse('mailing:messages')


class MessageDetailView(DetailView):
    model = Message

    def get_context_context(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = self.object
        return context_data


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:messages')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Удаление сообщения'
        return context_data


class ScheduleListView(ListView):
    model = Schedule

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Расписания'
        return context_data


class ScheduleCreateView(CreateView):
    model = Schedule
    form_class = ScheduleForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Создание расписания'
        return context_data

    def get_success_url(self):
        return reverse('mailing:schedules')


class ScheduleUpdateView(UpdateView):
    model = Schedule
    form_class = ScheduleForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'Редактирование {self.object.description}'
        return context_data

    def get_success_url(self):
        return reverse('mailing:schedules')



class ScheduleDeleteView(DeleteView):
    model = Schedule

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Удаление'
        return context_data

    def get_success_url(self):
        return reverse('mailing:schedules')


class ScheduleDetailView(DetailView):
    model = Schedule

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = self.object.description

        schedule_item = Schedule.objects.get(pk=self.kwargs.get('pk'))
        user_item = User.objects.filter(is_active=True)
        context_data['schedule_pk'] = schedule_item.pk
        context_data['user_item'] = user_item

        return context_data


def toggle_active(request, pk):
    schedule = Schedule.objects.get(pk=pk)
    # Переключаем статус is_active, если только рассылка не завершена
    if schedule.status != 'f':
        schedule.is_active = {schedule.is_active: False,
                              not schedule.is_active: True}[True]
        schedule.save()
    else:
        messages.error(request, 'You cannot deactivate completed schedule')
    return redirect(reverse('mailing:schedules'))


def toggle_run_pause(request, pk):
    schedule = Schedule.objects.get(pk=pk)
    # Переключаем статус running/pause, если только рассылка не завершена
    if schedule.status != 'f':
        schedule.status = {schedule.status == 'p': 'c',
                           schedule.status == 'c' or schedule.status == 'r': 'p'}[True]
        schedule.save()
    else:
        messages.error(request, 'You cannot run/pause completed schedule')
    return redirect(reverse('mailing:schedules'))


class MailingLogListView(ListView):
    model = MailingLog


class MailingLogDetailView(DetailView):
    model = MailingLog
