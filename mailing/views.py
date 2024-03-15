from random import sample

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from blog.models import Blog
from mailing.forms import ScheduleForm
from mailing.models import Client, Schedule, Message, MailingLog


class IndexView(TemplateView):
    template_name = 'mailing/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Главная'
        context_data['count_mailing'] = len(Schedule.objects.all())
        active_mailings_count = Schedule.objects.filter(is_active=True).count()
        context_data['active_mailings_count'] = active_mailings_count
        unique_clients_count = Client.objects.filter(is_active=True).distinct().count()
        context_data['unique_clients_count'] = unique_clients_count
        all_posts = list(Blog.objects.filter(is_published=True))
        context_data['random_blog_posts'] = sample(all_posts, min(3, len(all_posts)))
        return context_data


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = "Пользователи"
        return context_data

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.groups.filter(name='manager'):
            queryset = super().get_queryset()
        else:
            queryset = super().get_queryset().filter(owner=self.request.user)
        return queryset


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ('name', 'surname', 'patronymic', 'email', 'is_active', 'comment')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Добавление пользователя'
        return context_data

    def get_success_url(self):
        return reverse('mailing:clients')

    def form_valid(self, form):
        new_client = form.save()
        new_client.owner = self.request.user
        new_client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    fields = ('name', 'surname', 'patronymic', 'email', 'is_active', 'comment')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Редактирование пользователя'
        return context_data

    def get_success_url(self):
        return reverse('mailing:clients')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:clients')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Удаление пользователя'
        return context_data

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = self.object
        return context_data

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = "Сообщения"
        return context_data

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.groups.filter(name='manager'):
            queryset = super().get_queryset()
        else:
            queryset = super().get_queryset().filter(owner=self.request.user)
        return queryset


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ('title', 'subject', 'text')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Создание сообщения'
        return context_data

    def get_success_url(self):
        return reverse('mailing:messages')

    def form_valid(self, form):
        new_message = form.save()
        new_message.owner = self.request.user
        new_message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ('title', 'subject', 'text')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'Редактирование "{self.object.title}"'
        return context_data

    def get_success_url(self):
        return reverse('mailing:messages')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = self.object
        return context_data

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:messages')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Удаление сообщения'
        return context_data

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


class ScheduleListView(LoginRequiredMixin, ListView):
    model = Schedule

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Расписания'
        return context_data

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.groups.filter(name='manager'):
            queryset = super().get_queryset()
        else:
            queryset = super().get_queryset().filter(owner=self.request.user)
        return queryset


class ScheduleCreateView(LoginRequiredMixin, CreateView):
    model = Schedule
    form_class = ScheduleForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Создание расписания'
        return context_data

    def get_success_url(self):
        return reverse('mailing:schedules')

    def form_valid(self, form):
        new_schedule = form.save()
        new_schedule.owner = self.request.user
        new_schedule.save()
        return super().form_valid(form)


class ScheduleUpdateView(LoginRequiredMixin, UpdateView):
    model = Schedule
    form_class = ScheduleForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'Редактирование {self.object.description}'
        return context_data

    def get_success_url(self):
        return reverse('mailing:schedules')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


class ScheduleDeleteView(LoginRequiredMixin, DeleteView):
    model = Schedule

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Удаление'
        return context_data

    def get_success_url(self):
        return reverse('mailing:schedules')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


class ScheduleDetailView(LoginRequiredMixin, DetailView):
    model = Schedule

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = self.object.description

        schedule_item = Schedule.objects.get(pk=self.kwargs.get('pk'))
        user_item = Client.objects.filter(is_active=True)
        context_data['schedule_pk'] = schedule_item.pk
        context_data['user_item'] = user_item

        return context_data

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


@login_required
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


@login_required
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


class MailingLogListView(LoginRequiredMixin, ListView):
    model = MailingLog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.schedule.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_superuser:
            queryset = super().get_queryset()
        else:
            queryset = super().get_queryset().filter(schedule__owner=self.request.user)
        return queryset


class MailingLogDetailView(LoginRequiredMixin, DetailView):
    model = MailingLog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.schedule.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object
