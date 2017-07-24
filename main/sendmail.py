# -*- coding: UTF-8 -*-
from email.mime.text import MIMEText
from subprocess import Popen, PIPE


def send_mail(_from, _to, _subject, _content):
    msg = MIMEText(_content.encode('utf-8'), 'html', 'utf-8')
    msg["From"] = _from
    msg["To"] = _to
    msg["Subject"] = _subject
    p = Popen(["/usr/sbin/sendmail", "-t"], stdin=PIPE)
    # print msg.as_string()
    p.communicate(msg.as_string())
