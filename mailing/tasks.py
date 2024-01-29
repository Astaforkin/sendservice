from .models import Mailing, Message, Client
from sendservice.celery import app


@app.task
def add(x, y):
    return x + y
