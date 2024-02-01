from .models import Mailing, Message, Client
from sendservice.celery import app
from django.utils import timezone
from celery.schedules import crontab
import pytz


@app.task
def process_mailings():
    now = timezone.now()
    mailings = Mailing.objects.filter(
        date_time_start_mailing__lte=now,
        date_time_stop_mailing__gte=now
    )
    for mailing in mailings:
        clients_for_mailing = Client.objects.filter(
            mobile_code=mailing.mobile_code,
            tag=mailing.tag
        )
        for client in clients_for_mailing:
            if not Message.objects.filter(
                mailing=mailing, client=client
            ).exists():
                send_message_to_client.delay(client, mailing)


@app.task
def send_message_to_client(client, mailing):
    timezone = pytz.timezone(client.timezone)
    message = Message.objects.create(
        mailing=mailing,
        client=client,
        date_time_send=timezone.now()
    )
    print(f"Сообщение отправлено клиенту {client} с текстом: {message}")


app.conf.beat_schedule = {
    'process-mailings-every-minute': {
        'task': 'tasks.process_mailings',
        'schedule': crontab(minute='*/1'),
    }
}
