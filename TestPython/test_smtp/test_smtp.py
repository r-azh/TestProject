from email.mime.text import MIMEText
from smtplib import SMTP


class SmtpMail:
    host = None
    port = None
    user_name = None
    password = None

    def __init__(self, host, port, user_name=None, password=None):
        self.host = host
        self.port = port
        self.user_name = user_name
        self.password = password

    def send(self, sender, receivers, subject, content, message_type="plain"):
        """message_type could be plain, html, xml"""
        try:
            message = MIMEText(content, message_type)
            message['Subject'] = subject
            message['From'] = sender
            message['To'] = str(receivers)
            smtp = SMTP(self.host, self.port)
            if self.user_name and self.password:
                smtp.login(self.user_name, self.password)
            smtp.sendmail(sender, receivers, message.as_string())
        except Exception as ex:
            raise ex


def send_email(mail_smtp_port, mail_smtp_host, mail_smtp_username, mail_smtp_password, recipient_email_address,subject, message, message_type):
    if mail_smtp_host and mail_smtp_port:
        smtp_client = SmtpMail(mail_smtp_host,
                               mail_smtp_port,
                               mail_smtp_username,
                               mail_smtp_password)
        smtp_client.send(mail_smtp_username,
                         recipient_email_address,
                         subject,
                         message, message_type=message_type)


# mail_smtp_host = '185.55.226.157'
# mail_smtp_port = 25
# mail_smtp_username = 'amir.prof.net@parsadp.com'
# mail_smtp_password = 'p5yd5DU#'
mail_smtp_host = '185.4.30.74'
mail_smtp_port = 587
mail_smtp_username = 'ipn@rahyabtelecom.com'
mail_smtp_password = 'kbFQ5NXLm'
receiver = ["r_azh_777@yahoo.com", "r.azh.777@gmail.com", "rezazadeh.ali1@gmail.com", "AliRezazadeh@live.com"]
subject = "hello from Rezvan :)"
# message = "hello world, this is a message from python"
# message_type = "plain"
message = "<div dir='rtl'><b>به شبکه حرفه ای امیر خوش آمدید,<br>از پیوست شما به شبکه حرفه امیر سپاسگذاریم ." \
          "<br>با کلیک بر روی لینک زیر می توانید حساب کاربر خود در شبکه امیر را فعال کنید :" \
          "<br>http://amir.parsadp.com/#/user_activate?person_id=571f420b3ae7282dff9c02b9" \
          "<br>اطلاعات حساب کاربری شما در سایت امیر به صورت زیر می باشد :" \
          "<br>User-Name: 571f420a3ae7283ea2bd3d76@hotmail.com<br>Password: bahartest2@chmail.ir<br>" \
          "<br>شما می توانید برنامه اندروید امیر را از آدرس زیر دانلود کنید : " \
          "<br>http://amir.parsadp.com/Amir_App.apk<br></b></div>"
message_type = "html"

send_email(mail_smtp_port, mail_smtp_host, mail_smtp_username, mail_smtp_password, receiver, subject, message, message_type)



