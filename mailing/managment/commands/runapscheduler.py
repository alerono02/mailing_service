import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from mailing.models import Schedule, User
from mailing.services import send_mail_now

logger = logging.getLogger(__name__)


def everyday_job():
    daily_schedules = Schedule.objects.filter(periodic='d', is_active=True, status='c' or 'r')
    send_mail_now(daily_schedules)


def one_time_job():
    single_schedules = Schedule.objects.filter(periodic='s', is_active=True, status='c' or 'r')
    send_mail_now(single_schedules)


def weekly_job():
    weekly_schedules = Schedule.objects.filter(periodic='w', is_active=True, status='c' or 'r')
    send_mail_now(weekly_schedules)


def monthly_job():
    monthly_schedules = Schedule.objects.filter(periodic='m', is_active=True, status='c' or 'r')
    send_mail_now(monthly_schedules)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        for schedule in Schedule.objects.filter(periodic='s', is_active=True, status='c' or 'r'):
            scheduler.add_job(
                one_time_job,
                trigger=CronTrigger(
                    year=schedule.start_date.year,
                    month=schedule.start_date.month,
                    day=schedule.start_date.day,
                    hour=schedule.time.hour,
                    minute=schedule.time.minute,
                ),
                id=f"one_time_schedule_{schedule.id}",  # Уникальный идентификатор для каждого задания
                max_instances=1,
                replace_existing=True,
            )

            for schedule in Schedule.objects.filter(periodic='d', is_active=True, status='c' or 'r'):
                scheduler.add_job(
                    everyday_job(),
                    trigger=CronTrigger(
                        hour=schedule.time.hour,
                        minute=schedule.time.minute,
                    ),
                    id=f"everyday_schedule_{schedule.id}",  # Уникальный идентификатор для каждого задания
                    max_instances=1,
                    replace_existing=True,
                )

        for schedule in Schedule.objects.filter(periodic='w', is_active=True, status='c' or 'r'):
            scheduler.add_job(
                weekly_job,
                trigger=CronTrigger(
                    day_of_week=schedule.day_of_week,
                    hour=schedule.time.hour,
                    minute=schedule.time.minute,
                ),
                id=f"weekly_schedule_{schedule.id}",  # Уникальный идентификатор для каждого задания
                max_instances=1,
                replace_existing=True,
            )

        for schedule in Schedule.objects.filter(periodic='m', is_active=True, status='c' or 'r'):
            scheduler.add_job(
                monthly_job,
                trigger=CronTrigger(
                    day=schedule.day_of_month,
                    hour=schedule.time.hour,
                    minute=schedule.time.minute,
                ),
                id=f"monthly_schedule_{schedule.id}",  # Уникальный идентификатор для каждого задания
                max_instances=1,
                replace_existing=True,
            )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
