from django.db import models


class Mailing(models.Model):
    date_time_start_mailing = models.DateTimeField()
    text_message = models.TextField()
    mobile_code = models.CharField()
    tag = models.CharField()
    date_time_stop_mailing = models.DateTimeField()


class Client(models.Model):
    phone_number = models.CharField()
    mobile_code = models.CharField()
    tag = models.CharField()


class Message(models.Model):
    date_time_send = models.DateTimeField()
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
