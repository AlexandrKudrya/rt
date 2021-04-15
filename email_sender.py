# import necessary packages
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
import smtplib

def send_email(file_name, geter):
    msg = MIMEMultipart()

    message = "Тест от " + file_name.split("_")[0]

    # setup the parameters of the message
    password = "1qa2ws3ed1qa"
    msg['From'] = "tester.bot.no.relay@gmail.com"
    msg['To'] = geter
    msg['Subject'] = "Subscription"

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # create server
    server = smtplib.SMTP('smtp.gmail.com: 587')

    server.starttls()

    # Login Credentials for sending the mail
    server.login(msg['From'], password)

    with open(file_name, "rb", encoding='utf-8') as fil:
        part = MIMEApplication(
            fil.read(),
            Name=basename(file_name + ".txt")
        )
    # After the file is closed
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(file_name)
    msg.attach(part)

    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()

    print(f"Sucsesfuly send email to {geter}")