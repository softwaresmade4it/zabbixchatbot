FROM python:3.10-slim-buster

MAINTAINER Bryam Balan <bryam@made4it.com.br>

WORKDIR /opt

COPY . /opt/

RUN apt-get update && \
    apt-get -y install python-urllib3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

CMD ["python", "zabbix-chat-bot.py"]
