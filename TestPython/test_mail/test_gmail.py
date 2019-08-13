import smtplib
from email import policy
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MAIL_USERNAME = ''
MAIL_PASSWORD = ''
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465


def send_email(recipient_email_addresses, subject, message):
    message = _compose_email_message(recipient_email_addresses, [], [], subject, message)

    try:
        _send_email(recipient_email_addresses, message)
    except Exception as e:
        print('***** Error: {} in trying to send message:{} to email_addresses:{}'.format(
            e, message, recipient_email_addresses
        ))
    print('***** Success: send message:{} to: {}'.format(message, recipient_email_addresses))


def _compose_email_message(to_list, cc_list, bcc_list, subject, message):
    # email_text = """\
    # From: %s
    # To: %s
    # Subject: %s
    #
    # %s
    # """ % (SENDER, recipient, subject, message)
    # return email_text

    msg = MIMEMultipart('alternative')
    msg.set_charset('utf-8')
    # msg['Subject'] = Header(subject, 'utf-8')
    # msg['From'] = Header(f'{config.EMAIL_SENDER_TITLE} <{from_}>', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = f'"Newsbx.com::نیوزباکس" <{MAIL_USERNAME}>'
    msg['To'] = ','.join([f'<{to}>' for to in to_list])
    msg['Cc'] = ','.join(cc_list)
    msg['Bcc'] = ','.join(bcc_list)

    part = MIMEText(message, 'html', _charset='utf-8')
    msg.attach(part)
    _email_policy = policy.EmailPolicy().clone(utf8=True)
    msg = msg.as_string(policy=_email_policy)
    # msg = msg.as_string()
    return msg


def _send_email(recipient_email_addresses, message):
    sent_from = MAIL_USERNAME
    mail_server = smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT)  # for gmail
    # mail_server = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)  # for jetmail
    mail_server.ehlo()
    mail_server.login(MAIL_USERNAME, MAIL_PASSWORD)
    mail_server.sendmail(sent_from, recipient_email_addresses, message.encode('utf-8'))
    mail_server.close()


subject = 'test gmail'
body = 'test body'
recipients = ['@gmail.com']

send_email(recipients, subject, body)
