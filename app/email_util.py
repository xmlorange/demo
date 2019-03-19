# -*- coding: utf-8 -*-
"""
    author: Q.Y.
"""

import smtplib
import mimetypes
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate

from app.config import config


class SendEMail(object):
    username = config.EMAIL_USERNAME
    password = config.EMAIL_PASSWORD

    def __init__(self):
        self.send_server = smtplib.SMTP_SSL(host=config.EMAIL_HOST, port=config.EMAIL_PORT, timeout=300)
        self.send_server.login(self.username, self.password)

    @staticmethod
    def create_email(to_email, body=None, subject=None, files=None):
        msg = MIMEMultipart()
        if not to_email:
            to_email = [config.EMAIL_USERNAME]
        msg['From'] = config.EMAIL_USERNAME
        msg['Subject'] = subject
        msg['To'] = ','.join(to_email)
        msg['Date'] = formatdate(localtime=True)
        if body:
            msg.attach(MIMEText(body))

        if files:
            for filename, file_stream in files.items():
                _types = mimetypes.types_map.get("." + filename.split(".")[-1], "application/vnd.ms-excel")
                main_type, sec_type = _types.split("/")

                part = MIMEBase(main_type, sec_type)  # 'octet-stream': binary data
                part.set_payload(file_stream)

                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment',
                                filename=("utf8", "", filename))
                # filename='=?utf-8?b?' + str(base64.b64encode(filename.encode('UTF-8'))) + '?=')
                msg.attach(part)
        return msg

    def run(self, to_email=None, body=None, subject=None, files=None):
        if not subject:
            subject = '无主题'
        message = self.create_email(to_email=to_email, body=body, subject=subject, files=files)
        self.send_server.sendmail(from_addr=self.username, to_addrs=to_email, msg=message.as_string())

    def close(self):
        self.send_server.quit()


def sender_email(to_email=None, body=None, subject=None, files=None):
    sender = SendEMail()
    sender.run(to_email=to_email or config.TO_EMAIL,
               body=body,
               subject=subject,
               files=files)
    sender.close()
