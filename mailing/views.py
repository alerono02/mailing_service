from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse, reverse_lazy

from mailing.models import User


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
        return reverse('mailing:user_list')


class UserUpdateView(UpdateView):
    model = User
    fields = ('name', 'surname', 'patronymic', 'email')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Редактирование пользователя'
        return context_data

    def get_success_url(self):
        return reverse('mailing:user_list')


class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('mailing:user_list')

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
