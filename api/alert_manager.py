from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from string import Template

import config.config as config


SECRETS  = config.get_secrets()

def make_smtp_server() -> smtplib.SMTP:
    """Start SMTP server"""
    smtp_server = smtplib.SMTP(host=SECRETS['email-sender-host'], port=SECRETS['email-sender-port'])
    smtp_server.starttls()
    smtp_server.login(SECRETS['email-sender-address'], SECRETS['email-sender-password'])
    return smtp_server

def get_message_template() -> Template:
    """Returns email Template object from file"""
    with open('message_template.txt', 'r', encoding='utf-8') as template_file:
        content = template_file.read()
    return Template(content)


def send_moisture_alert_email(moisture_reading: int) -> None:
    """Sends email to list of recipients with anomalous soil moisture reading"""
    recipients = SECRETS['email-recipients']
    smtp_server = make_smtp_server()

    for recipient in recipients:
        
        msg = MIMEMultipart()
        msg_template = get_message_template()
        msg_text = msg_template.substitute(SOIL_MOISTURE=moisture_reading)

        msg['From'] = SECRETS['email-sender-address']
        msg['To'] = recipient
        msg['Subject'] = "DirtBag Pi: Soil Moisture Alert"
        msg.attach(MIMEText(msg_text, 'plain'))
        
        smtp_server.send_message(msg)
        del msg
    
    smtp_server.quit()
