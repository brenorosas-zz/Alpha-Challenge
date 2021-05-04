from email.message import EmailMessage
from workers import task
from .models import *
import yfinance as yf
import pandas as pd
import os
import smtplib
import time
from django.utils import timezone
from datetime import datetime, timedelta

def send_email(recipient, asset, **kwargs):
    msg = EmailMessage()
    msg['Subject'] = ("ALERTA de oportunidade de negociação: " + asset.name)
    if kwargs['description'] == "superior":
        msg.set_content("O preço do ativo {} cruzou o limite superior de {} e está R${:.2f}. \n\n".format(asset.name, asset.upper_limit, kwargs['price']))
    elif kwargs['description'] == "inferior":
        msg.set_content("O ativo {} cruzou o limite inferior de {} e está R${:.2F}. \n\n".format(asset.name, asset.inferior_limit, kwargs['price']))
    msg['From'] = os.environ.get('EMAIL_ADDRESS')
    msg['To'] = recipient
    smtp = "smtp.gmail.com"
    server = smtplib.SMTP_SSL(smtp, 465)
    server.login(os.environ.get('EMAIL_ADDRESS'), os.environ.get('EMAIL_PASSWORD'))
    server.send_message(msg)
    server.quit()
    print("Sucesso ao enviar email")

def calculate_next_monitoring_date(asset):
    seconds = asset.update_time
    next_time = timezone.now() + timedelta(seconds = seconds)
    return next_time


def monitor_asset(asset):
    tckrSymb = asset.name + '.SA'
    ticker = yf.Ticker(tckrSymb)
    historical_ticker = ticker.history(period = "1d", interval = "1m")
    price = pd.DataFrame(historical_ticker)['Open'].iloc[-1]
    if price >= asset.upper_limit:
        send_email(asset.user.email, asset, description = "superior", price = price)
    elif price <= asset.inferior_limit:
        send_email(asset.user.email, asset, description = "inferior", price = price)

@task(schedule = 1)
def check_next_monitor():
    jobs = Management.objects.filter(next_time__lte= timezone.now())
    for job in jobs:
        monitor_asset(job.asset)
        Management.objects.filter(id = job.id).update(next_time = calculate_next_monitoring_date(job.asset))
