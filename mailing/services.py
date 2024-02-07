import datetime

from django.conf import settings
from django.core.mail import send_mail

from mailing.models import MailingLog, Client, Schedule


def send_mail_now(schedule):
    """
    Функция для отправки почты по заданному расписанию.

    Args:
        schedules: список объектов расписания, по которым нужно отправить почту.
        :param schedule:
    """
    # Получаем сообщение и пользователей для рассылки
    message = schedule.message
    users = Schedule.objects.get(id=schedule.id).clients.all()
    print(users)
    # Отправляем почту каждому пользователю

    try:
        schedule.status = 'r'
        result = send_mail(
            subject=message.subject,
            message=message.text,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email for user in users],
            fail_silently=False,
        )
        print('sent')
        print([user.email for user in users])
        print(result)
        # Если почта отправлена успешно, создаем лог с соответствующим статусом
        MailingLog.objects.create(
            schedule=schedule,
            status_of_last_attempt=True,
            server_response="Сообщение отправлено успешно"
        )

        print("Log created")
        if schedule.end_date and schedule.end_date <= datetime.date.today():
            # Если время рассылки закончилось, обновляем статус расписания на "завершено"
            schedule.status = 'f'
        schedule.save()

    except Exception as e:
        # Если почта не отправлена, создаем лог с соответствующим статусом и сообщением об ошибке
        MailingLog.objects.create(
            schedule=schedule,
            status_of_last_attempt=False,
            server_response=f"Ошибка при отправке сообщения: {e}"
        )
        print('Schedule failed, check logs')
        schedule.status = 'e'
        schedule.save()

