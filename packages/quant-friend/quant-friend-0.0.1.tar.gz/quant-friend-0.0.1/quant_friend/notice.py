import mimetypes
import os
import smtplib
import typing
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from typing import List


def format_address(s):
    name, address = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), address))


class EmailSender:
    sender: str
    host: str
    port: int
    ssl: bool
    user: str
    password: str

    def __init__(self, sender: str,
                 host: str,
                 port: int,
                 ssl: bool,
                 user: str,
                 password: str):
        super().__init__()
        if not sender:
            raise ValueError("未配置邮件服务: sender")
        self.sender = sender
        if not host:
            raise ValueError("未配置邮件服务: host")
        self.host = host
        if not port:
            raise ValueError("未配置邮件服务: port")
        self.port = port
        self.ssl = ssl
        self.user = user
        self.password = password

    def create_smtp(self):
        if self.ssl:
            obj = smtplib.SMTP_SSL(self.host, self.port)
        else:
            obj = smtplib.SMTP(self.host, self.port)
        if self.user and self.password:
            obj.login(self.user, self.password)
        return obj


emailConfig: typing.Optional[EmailSender] = None


def config_email_sender(sender: str,
                        host: str,
                        port: int,
                        ssl: bool,
                        user: str,
                        password: str):
    global emailConfig
    emailConfig = EmailSender(sender, host, port, ssl, user, password)


def send_result(receivers: List[str], title: str, body: str, attachments: List[str]):
    global emailConfig
    if not emailConfig:
        config = {}
        for name in filter(lambda it: it.startswith("smtp_"), iter(os.environ)):
            key = name[5:]
            if key == 'port':
                config[key] = int(os.environ[name])
            elif key == 'ssl':
                config[key] = bool(os.environ[name])
            else:
                config[key] = os.environ[name]
        emailConfig = EmailSender(config['sender'], config['host'], config['port'], config['ssl'], config['user'],
                                  config['password'])
    sender = emailConfig.sender

    try:
        smtp_obj = emailConfig.create_smtp()

        msg = MIMEMultipart()
        # Header对中文进行转码
        msg['From'] = format_address('Quant Friend <%s>' % sender)
        msg['To'] = ','.join(receivers)
        msg['Subject'] = Header(title, 'utf-8').encode()
        # plain代表纯文本
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        # msg.set_payload(body, 'utf-8')
        for file in attachments:
            file_type = mimetypes.guess_type(file)
            if not file_type:
                raise ValueError("{0} 不是支持的附件类型".format(file))
            file_type_str = file_type[0]
            with open(file, 'rb') as f:
                mime = MIMEBase(file_type_str[0:file_type_str.index('/')], file_type_str[file_type_str.index('/') + 1:],
                                filename=file)
                mime.add_header('Content-Disposition', 'attachment', filename=file)
                mime.set_payload(f.read())
                encoders.encode_base64(mime)
                msg.attach(mime)

        smtp_obj.send_message(msg)
        print("Successfully sent email")
        smtp_obj.quit()
        smtp_obj.close()
    except smtplib.SMTPException as v1:
        print("Error: unable to send email:", v1)
