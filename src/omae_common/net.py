import smtplib
from email.mime.text import MIMEText


# smtp (sending) wrapper

def send_email(smtp_param: dict, subject: str, message: str):
    """Send email to the receiver using smtp library

    Keyword arguments:
    smtp_param -- smtp paramters (dict) containing sender, receiver, host,
            port, id, and password
            ex) {
                'host': 'smpt.host.com',
                'port': 587,
                'id': 'id_of_smtp_host',
                'passwd': 'password_of_smtp_host',
                'to': 'email address(receiver)',
                'from': 'email address(sender)',
            }
    subject -- subject of message
    message -- message (plain text)
    """
    host = smtp_param['host']
    smtpid = smtp_param['id']
    smtppw = smtp_param['passwd']

    smtp = smtplib.SMTP(host, smtp_param['port'])
    smtp.ehlo()
    smtp.starttls()
    #smtp.ehlo()
    smtp.login(smtpid, smtppw)

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['To'] = smtp_param['to']

    smtp.sendmail(smtp_param['from'], smtp_param['to'], msg.as_string())