from .models import Mailing, Message, Client
from sendservice.celery import app
import datetime
import pytz


@app.task
def get_active_mailings():
    active_mailings = Mailing.objects.filter(is_sent=False)
    for mailing in active_mailings:
        get_clients_for_mailing.delay(mailing)


@app.task
def get_clients_for_mailing(mailing):
    clients_for_mailing = Client.objects.filter(
        mobile_code=mailing.mobile_code,
        tag=mailing.tag
    )
    get_clients_no_message.delay(clients_for_mailing, mailing)


@app.task
def get_clients_no_message(clients, mailing):
    for client in clients:
        if not Message.objects.filter(mailing=mailing, client=client, s_delivered=False).exists():
            send_message_to_client.delay(client, mailing)


@app.task
def send_message_to_client(client_id, mailing_id):
    client = Client.objects.get(pk=client_id)
    mailing = Mailing.objects.get(pk=mailing_id)
    timezone = pytz.timezone(client.timezone)
    now = datetime.now(timezone)

    if mailing.date_time_start_mailing <= now.time() <= mailing.date_time_stop_mailing:
        