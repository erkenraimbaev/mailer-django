from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail
import pytz
from main.models import Newsletter, Logs


def send_mail_save_log(mailing, client):
    mailing.status = 'finish'
    mailing.is_active = False
    try:
        send_mail(
            subject=f'{mailing.head}',
            message=f'{mailing.body}'
                    f'С уважением, {mailing.owner}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[client]
        )
        log = Logs(newsletter=mailing, status='make', response='success')
        log.save()
    except Exception:
        log = Logs(newsletter=mailing, status='dont_make', response='error')
        log.save()
    mailing.save()


def send_mailings():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    mailings = Newsletter.objects.filter(time__lte=current_datetime).filter(status__in=['created', 'start'])
    for mailing in mailings:
        client = mailing.to_client.email
        if mailing.period == 'no':
            send_mail_save_log(mailing, client)
        elif mailing.period == 'once_a_day':
            if mailing.time.hour == current_datetime.hour and mailing.time.minute == current_datetime.minute:
                send_mail_save_log(mailing, client)
        elif mailing.period == 'once_a_week':
            if ((mailing.time - current_datetime).days % 7 == 0) and mailing.time.hour == current_datetime.hour and \
                    mailing.time.minute == current_datetime.minute:
                send_mail_save_log(mailing, client)
        elif mailing.period == 'once_a_month':
            if ((mailing.time - current_datetime).days % 31 == 0) and mailing.time.hour == current_datetime.hour and \
                    mailing.time.minute == current_datetime.minute:
                send_mail_save_log(mailing, client)


def start():
    sheduler = BackgroundScheduler()
    sheduler.add_job(send_mailings, "interval", minutes=1)
    sheduler.start()
