from datetime import datetime

from django.conf import settings
from django.core.mail import send_mail

from mailing.models import MailingLog


def send_mail_now(schedules):
    """
    Функция для отправки почты по заданному расписанию.

    Args:
        schedules: список объектов расписания, по которым нужно отправить почту.
    """
    for schedule in schedules:
        # Получаем сообщение и пользователей для рассылки
        message = schedule.message
        users = schedule.users.filter(is_active=True)

        # Формируем текст письма
        email_body = f"""
        Тема: {message.subject}

        {message.text}
        """

        # Отправляем почту каждому пользователю
        for user in users:
            try:
                send_mail(
                    message.subject,
                    email_body,
                    "sender@example.com",
                    [user.email],
                    fail_silently=False,
                )

                # Если почта отправлена успешно, создаем лог с соответствующим статусом
                MailingLog.objects.create(
                    schedule=schedule,
                    status_of_last_attempt=True,
                    server_response="Сообщение отправлено успешно"
                )
            except Exception as e:
                # Если почта не отправлена, создаем лог с соответствующим статусом и сообщением об ошибке
                MailingLog.objects.create(
                    schedule=schedule,
                    status_of_last_attempt=False,
                    server_response=f"Ошибка при отправке сообщения: {e}"
                )

        if schedule.end_time and schedule.end_time < datetime.now():
        # Если время рассылки закончилось, обновляем статус расписания на "завершено"
            schedule.status = 'f'
        else:
            schedule.status = 'r'
        schedule.save()
