FROM python:3.9

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY . /app/
WORKDIR /app/

EXPOSE 8000
EXPOSE 5555