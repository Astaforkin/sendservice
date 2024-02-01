from .models import Mailing, Message, Client
from sendservice.celery import app
from django.utils import timezone
import pytz


# @app.task
# def get_active_mailings():
#     active_mailings = Mailing.objects.filter()
#     for mailing in active_mailings:
#         get_clients_for_mailing.delay(mailing)


# @app.task
# def get_clients_for_mailing(mailing):
#     clients_for_mailing = Client.objects.filter(
#         mobile_code=mailing.mobile_code,
#         tag=mailing.tag
#     )
#     get_clients_no_message.delay(clients_for_mailing, mailing)


# @app.task
# def get_clients_no_message(clients, mailing):
#     for client in clients:
#         if not Message.objects.filter(mailing=mailing, client=client).exists():
#             send_message_to_client.delay(client, mailing)
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
        pk=mailing,
        pk=client,
        date_time_send=timezone.now()
    )
    print(f"Сообщение отправлено клиенту {client} с текстом: {message}")
