from .models import Mailing, Message, Client
from sendservice.celery import app
from django.utils import timezone
from celery.schedules import crontab
import pytz
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


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
                send_message_to_client.delay(client_id=client.id, mailing_id=mailing.id)


@app.task
def send_message_to_client(client_id=None, mailing_id=None):
    try:
        client = Client.objects.get(id=client_id)
        mailing = Mailing.objects.get(id=mailing_id)
        timezone = pytz.timezone(client.timezone)
        message = Message.objects.create(
            mailing=mailing,
            client=client,
            date_time_send=timezone.now()
        )
        logger.info(f"Сообщение отправлено клиенту {message.client.tag} с текстом:{message.mailing.text_message}")

    except Client.DoesNotExist:
        logger.error(f"Клиент с id {client_id} не найден")
    except Mailing.DoesNotExist:
        logger.error(f"Рассылка с id {mailing_id} не найдена")
