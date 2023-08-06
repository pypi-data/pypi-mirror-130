import time
import imaplib
import email
import smtplib
import asyncio
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def idle(connection):
    last_len = None
    connection.select('inbox')
    while True:
        connection.select('inbox')
        status, data = connection.search(None, 'ALL')
        
        mail_ids = []
        for block in data:
            mail_ids += block.split()
        
        if last_len is None or \
            len(mail_ids) <= last_len:
            last_len = len(mail_ids)
            continue
        
        if len(mail_ids) > last_len:
            yield mail_ids[last_len]
            last_len = len(mail_ids)


class Sender:
    def __init__(self, name, email):
        self.name = name
        self.email = email


class MailContext:
    def __init__(self, sender, subject, body):
        self.sender = sender
        self.subject = subject
        self.body = body
        self.binding = None
    
    def bind(self, binding):
        self.binding = binding
        return self
    
    async def send(self, body):
        await self.binding.send([self.sender.email], self.subject, body, False)
    
    async def sendf(self, body):
        await self.binding.send([self.sender.email], self.subject, body, True)


def get_email(data):
    for response_part in data:
        if isinstance(response_part, tuple):
            message = email.message_from_bytes(response_part[1])

            mail_from = message['from']
            mail_subject = message['subject']
            if message.is_multipart():
                mail_content = ''
                for part in message.get_payload():
                    if part.get_content_type() == 'text/plain':
                        mail_content += part.get_payload()
            else:
                mail_content = message.get_payload()
            
            email_from = mail_from[mail_from.rfind('<') + 1 : -1]
            user_from = mail_from[:mail_from.rfind('<') - 1]
            return MailContext(
                Sender(user_from, email_from), 
                mail_subject, 
                mail_content
            )


class Client:
    def __init__(self, prefix):
        self.prefix = prefix
        self.email = None
        self.password = None
        self._commands = {
            'help': self.help_default
        }

    def command(self, name):
        def inner(cmd):
            self._commands[name.lower()] = cmd
            return cmd
        return inner

    async def help_default(self, ctx):
        out = "<code><b>DEFAULT HELP COMMAND</b><br>Commands:"
        for command in self._commands:
            out += "<br>&emsp;- " + command
        out += "</code>"
        await ctx.sendf(out)

    async def send(self, to, subject, body, is_html):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['To'] = ", ".join(to)
        msg['From'] = self.email

        msg.attach(MIMEText(body, 'html' if is_html else 'plain'))


        server = self._get_server()
        while True:
            try:
                server.sendmail(self.email, to, msg.as_string())
                break
            except (smtplib.SMTPSenderRefused, \
                    smtplib.SMTPDataError, \
                    smtplib.SMTPServerDisconnected):
                time.sleep(150)
                server = self._get_server()
        server.close()
    
    def _get_server(self):
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(self.email, self.password)
        return server

    def run(self, email, password):
        self.email = email
        self.password = password

        server = imaplib.IMAP4_SSL('imap.gmail.com')
        server.login(email, password)

        for mail_id in idle(server):
            status, data = server.fetch(mail_id, '(RFC822)')
            message = get_email(data)
            if message.subject.startswith(self.prefix):
                command = message.subject[len(self.prefix):].lower()
                message.subject = ("=>" if self.prefix == "->" else "->") + message.subject[len(self.prefix):]

                if command not in self._commands:
                    continue

                func = self._commands[command]
                threading.Thread(target=lambda: asyncio.run(func(message.bind(self)))).start()
                server.store(mail_id, '+FLAGS', '\\Deleted')
