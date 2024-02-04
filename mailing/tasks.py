from .models import Mailing, Message, Client
from sendservice.celery import app
from django.utils import timezone
from celery.schedules import crontab
import pytz
from celery.utils.log import get_task_logger
from django.shortcuts import get_object_or_404


logger = get_task_logger(__name__)


@app.task
def process_mailings():
    logger.info("Начало задачи process_mailings")
    try:
        now = timezone.now()
        mailings = Mailing.objects.filter(
            date_time_start_mailing__lte=now,
            date_time_stop_mailing__gte=now
        )
        logger.info(f"Найдено {len(mailings)} активных рассылок")
        for mailing in mailings:
            clients_for_mailing = Client.objects.filter(
                mobile_code=mailing.mobile_code,
                tag=mailing.tag
            )
            logger.info(f"Найдено {len(clients_for_mailing)} клиентов для рассылки {mailing.id}")
            for client in clients_for_mailing:
                if not Message.objects.filter(
                    mailing=mailing, client=client
                ).exists():
                    send_message_to_client.delay(client_id=client.pk, mailing_id=mailing.pk)
                    logger.info(f"Отправка сообщения клиенту {client.pk} для рассылки {mailing.pk}")
    except Exception as e:
        logger.error(f"Произошла ошибка в задаче process_mailings: {e}")


@app.task
def send_message_to_client(client_id, mailing_id):
    logger.info(f"Начало задачи send_message_to_client для клиента {client_id} и рассылки {mailing_id}")
    try:
        client = Client.objects.get(pk=client_id)
        mailing = Mailing.objects.get(pk=mailing_id)
        message = Message.objects.create(
            mailing=mailing,
            client=client,
            date_time_send=timezone.now()
        )
        logger.info(f"Сообщение отправлено клиенту {message.client.id} с текстом:{message.mailing.text_message}")

    except Client.DoesNotExist:
        logger.error(f"Клиент с id {client_id} не найден")
    except Mailing.DoesNotExist:
        logger.error(f"Рассылка с id {mailing_id} не найдена")
