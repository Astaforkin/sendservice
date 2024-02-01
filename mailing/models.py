from django.db import models


class Mailing(models.Model):
    date_time_start_mailing = models.DateTimeField(
        verbose_name='дата и время запуска рассылки'
    )
    text_message = models.TextField(
        max_length=255,
        verbose_name='текст сообщения'
    )
    mobile_code = models.CharField(
        max_length=100,
        verbose_name='код мобильного оператора'
    )
    tag = models.CharField(max_length=100, verbose_name='тег')
    date_time_stop_mailing = models.DateTimeField(
        verbose_name='дата и время окончания рассылки'
    )


class Client(models.Model):
    phone_number = models.CharField(
        max_length=11,
        verbose_name='номер телефона клиента'
    )
    mobile_code = models.CharField(
        max_length=3,
        verbose_name='код мобильного оператора'
    )
    tag = models.CharField(max_length=100, verbose_name='тег')


class Message(models.Model):
    date_time_send = models.DateTimeField()
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='messages'
    )
