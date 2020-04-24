from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from string import Template

import config.config as config

#Start the SMTP server
secrets = config.get_secrets()
smtp_server = smtplib.SMTP(host=secrets['email-sender-host'], port=secrets['email-sender-port'])
smtp_server.starttls()
smtp_server.login(secrets['email-sender-address'], secrets['email-sender-password'])


def get_message_template() -> Template:
    """Returns email Template object from file"""
    with open('message_template.txt', 'r', encoding='utf-8') as template_file:
        content = template_file.read()
    return Template(content)

def send_moisture_alert_email(moisture_reading: int) -> None:
    """Sends email to list of recipients with anomalous soil moisture reading"""
    recipients = secrets['email-recipients']
    for recipient in recipients:
        
        msg = MIMEMultipart()
        msg_template = get_message_template()
        msg_text = msg_template.substitute(SOIL_MOISTURE=moisture_reading)

        msg['From'] = secrets['email-sender-address']
        msg['To'] = recipient
        msg['Subject'] = "DirtBag Pi: Soil Moisture Alert"
        msg.attach(MIMEText(msg_text, 'plain'))
        
        smtp_server.send_message(msg)
        del msg

send_moisture_alert_email(17)
