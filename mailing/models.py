from datetime import datetime

from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    surname = models.CharField(max_length=100, verbose_name='фамилия')
    name = models.CharField(max_length=100, verbose_name='имя')
    patronymic = models.CharField(max_length=100, verbose_name='отчество')
    email = models.EmailField(max_length=254, unique=True, verbose_name='email')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='дата изменения')
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='активность')

    def __str__(self):
        return f'{self.surname} {self.name[0]}. {self.patronymic[0]}.({self.email})'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Message(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название', **NULLABLE)
    text = models.TextField(verbose_name='текст', **NULLABLE)
    subject = models.CharField(max_length=150, **NULLABLE, verbose_name='тема')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='дата изменения')

    def __str__(self):
        return f'{self.title} {self.text}'

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Schedule(models.Model):
    PERIODIC_CHOICES = (
        ('s', 'Single'),
        ('d', 'Daily'),
        ('w', 'Weekly'),
        ('m', 'Monthly'),
    )

    STATUS_CHOICES = (
        ('c', 'Created'),
        ('r', 'Running'),
        ('p', 'Paused'),
        ('e', 'Failed'),
        ('f', 'Completed'),
    )

    DAY_OF_WEEK_CHOICES = (
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday'),
    )

    description = models.TextField(max_length=200, verbose_name='описание')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='сообщение')
    status = models.CharField(max_length=1, default='c', choices=STATUS_CHOICES, verbose_name='статус')
    day_of_week = models.IntegerField(choices=DAY_OF_WEEK_CHOICES, verbose_name='день недели', **NULLABLE)
    day_of_month = models.IntegerField(verbose_name='день месяца', **NULLABLE)
    clients = models.ManyToManyField(Client, verbose_name='Пользователи')
    periodic = models.CharField(max_length=1, choices=PERIODIC_CHOICES, verbose_name='периодичность')
    start_date = models.DateField(verbose_name='дата начала')
    end_date = models.DateField(verbose_name='дата окончания')
    time = models.TimeField(verbose_name='время начала')
    is_active = models.BooleanField(default=True, verbose_name='активна')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='дата изменения')

    def __str__(self):
        return f'{self.message.title} - {self.start_date} - {self.end_date}'

    class Meta:
        verbose_name = 'расписание'
        verbose_name_plural = 'расписания'


class MailingLog(models.Model):
    date_of_last_attempt = models.DateTimeField(auto_now=True, verbose_name='дата и время последней попытки')
    status_of_last_attempt = models.BooleanField(default=False, verbose_name='cтатус последний попытки')
    server_response = models.TextField(verbose_name='ответ сервера', **NULLABLE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, verbose_name='расписание', **NULLABLE)

    def __str__(self):
        return f'{self.schedule.description}: {self.date_of_last_attempt} - {self.status_of_last_attempt}'

    class Meta:
        verbose_name = 'Логи рассылки'
        verbose_name_plural = 'Логи рассылок'
        ordering = ('-date_of_last_attempt',)
