FROM python:3

ENTRYPOINT ["python", "/opt/modem-watchdog/modem_watchdog.py"]

WORKDIR /opt/modem-watchdog/
COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pwd

COPY ./ .
