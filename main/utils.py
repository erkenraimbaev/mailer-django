from datetime import datetime
from time import sleep

from django.conf import settings
from django.core.mail import send_mail
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ProcessPoolExecutor


jobstores = {
    'mongo': {'type': 'mongodb'},
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}
executors = {
    'default': {'type': 'threadpool', 'max_workers': 20},
    'processpool': ProcessPoolExecutor(max_workers=5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

# СОЗДАЕМ ФОНОВЫЙ ПЛАНИРОВЩИК
# ЗАДАНИЙ ПО УМОЛЧАНИЮ
scheduler = BackgroundScheduler()

# настраиваем фоновый планировщик заданий
scheduler.configure(jobstores=jobstores, executors=executors,
                    job_defaults=job_defaults, timezone=utc)

# добавляем задание
# scheduler.add_job(..., trigger='interval', id='job_1', hour=1,
#                   jobstore='default', executor='default')


def send(newsletter):
    send_mail(
        subject=f'{newsletter.head}',
        message=f'{newsletter.body}'
                f'С уважением, {newsletter.owner}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[newsletter.to_client]
    )


def send_mail_to_client(newsletter_list):
    for newsletter in newsletter_list:
        if newsletter.is_active:
            if newsletter.period == 'no':
                if newsletter.time >= datetime.now:
                    send(newsletter)
                    newsletter.status = 'start'
                    newsletter.save()

            if newsletter.period == 'once_a_day':
                scheduler.add_job(send(newsletter), trigger='interval', id='job_1', day=1,
                                  jobstore='default', executor='default')
                newsletter.status = 'start'
                newsletter.save()
            if newsletter.period == 'once_a_week':
                scheduler.add_job(send(newsletter), trigger='interval', id='job_2', week=1,
                                  jobstore='default', executor='default')
                newsletter.status = 'start'
                newsletter.save()
            if newsletter.period == 'once_a_month':
                scheduler.add_job(send(newsletter), trigger='interval', id='job_3', month=1,
                                  jobstore='default', executor='default')
                newsletter.status = 'start'
                newsletter.save()


# Запуск запланированных заданий
scheduler.start()

# Запускает бесконечный цикл
while True:
    sleep(1)
