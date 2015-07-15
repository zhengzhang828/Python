import smtplib
import mimetypes
from email.mime.text import MIMEText
import re


class Mailer(object):

    def __init__(self,host, port):
        self.host = host
        self.port = port
        self.user = None
        self.pwd = None

    def login(self, user, pwd):
        self.user = user
        self.pwd = pwd

    def send(self, msg):
        sender = msg.From
        receiver = msg.To
        server=smtplib.SMTP(self.host, self.port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        if self.user and self.pwd:
            server.login(self.user, self.pwd)
        try:
            server.sendmail(sender, receiver, msg.text())
        except TypeError:
            server.sendmail(sender, receiver, msg.text())
        server.close()
    
class Message(object):
    
    def __init__(self):
        self.From=None
        self.To=None
        self.Subject = None
        self.Body = None

    def emailAdrCorrect(self,email):
        pattern = '[\.\w]{1,}[@]\w+[.]\w+'
        if re.match(pattern, email):
            return True
        else:
            return False
    
    def text(self):
        msg = MIMEText(self.Body)
        self.setInfo(msg)
        return msg.as_string()

    def setInfo(self, msg):
        msg['Subject']=self.Subject
        if self.emailAdrCorrect(self.From) and self.emailAdrCorrect(self.To):
            msg['From']=self.From
            msg['To'] = self.To
        else:
            raise ValueError("Wrong email addresses")

if __name__=='__main__':
    localHost = "smtp.emailsrvr.com"
    localPort = 587

    mailer = Mailer(localHost,localPort)
    mailer.user = "username"
    mailer.pwd = "password"

    message = Message()
    message.From = "sender@email.com"
    message.To = "receiver@email.com"
    message.Subject = "Testing Email"
    message.Body = "This is an email for testing"

    mailer.send(message)
