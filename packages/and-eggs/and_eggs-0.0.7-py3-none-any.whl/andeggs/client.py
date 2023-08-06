import time
import imaplib
import email
import smtplib
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import asyncio


class Sender:
    def __init__(self, name, email):
        self.name = name
        self.email = email


class MailContext:
    def __init__(self, sender, subject, body):
        self.sender = sender
        self.subject = subject
        self.body = body
        self._binding = None
    
    def _bind(self, binding):
        self._binding = binding
        return self
    
    async def send(self, body):
        await self._binding.send(
            to=[self.sender.email], 
            subject=self.subject, 
            body=body, 
            is_html=False,
            name=self.sender.name
        )
    
    async def sendf(self, body, *args):
        await self._binding.send(
            to=[self.sender.email], 
            subject=self.subject, 
            body=body.format(*args), 
            is_html=True,
            name=self.sender.name
        )


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
        self._tasks = []
        self._events = {
            'on_ready': lambda: None,
            'on_message': lambda _: None,
            'on_stop': lambda: None,
            'on_command': lambda _: None,
            'on_send': lambda _: None,
        }
        self._running = False
        self._server = None

    def command(self, name):
        def inner(func):
            def cmd(ctx):
                if self._running:
                    threading.Thread(target=lambda: asyncio.run(func(ctx._bind(self)))).start()
            self._commands[name.lower()] = cmd
            return cmd
        return inner

    async def help_default(self, ctx):
        out = "<code><b>DEFAULT HELP COMMAND</b><br>Commands:"
        for command in self._commands:
            out += "<br>&emsp;- " + command
        out += "</code>"
        await ctx.sendf(out)

    async def send(self, *, to, subject, body, is_html, name=None):
        self._events['on_send'](MailContext(
            Sender(name, to),
            subject,
            body,
        ))
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['To'] = ", ".join(to)
        msg['From'] = self.email

        msg.attach(MIMEText(body, 'html' if is_html else 'plain'))


        server = self._get_server()
        while self._running:
            try:
                server.sendmail(self.email, to, msg.as_string())
                break
            except (smtplib.SMTPSenderRefused, \
                    smtplib.SMTPDataError, \
                    smtplib.SMTPServerDisconnected):
                time.sleep(150)
                server = self._get_server()
        if self._running: server.close()
    
    def _get_server(self):
        if not self._running:
            return None
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(self.email, self.password)
        return server

    def task(self, interval):
        def decor(func):
            
            def inner():
                if not self._running:
                    return
                threading.Timer(interval, inner).start()
                func()
                
            def middle():
                if not self._running:
                    return
                threading.Thread(target=inner).start()
                
            self.tasks.append(middle)
            return middle
        return decor

    def event(self, name):
        if name not in self._events:
            raise Exception("Invalid event name")
        def decor(func):
            def event(*args):
                if self._running:
                    threading.Thread(target=lambda: asyncio.run(func(*args))).start()
            self._events[name] = event
            return func
        return decor
    
    def _idle(self):
        last_len = None
        connection = self._server
        connection.select('inbox')        
        while self._running:
            connection.select('inbox')
            _, data = connection.search(None, 'ALL')
            
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

    def run(self, email, password):
        threading.Thread(target=self._run, args=(email, password)).start()

    def _run(self, email, password):
        self.email = email
        self.password = password

        server = imaplib.IMAP4_SSL('imap.gmail.com')
        server.login(email, password)
        self._server = server
        self._running = True
        
        self._events['on_ready']()
        
        for task in self._tasks:
            task()

        for mail_id in self._idle():
            _, data = server.fetch(mail_id, '(RFC822)')
            message = get_email(data)
            
            is_command = message.subject.startswith(self.prefix)
            if is_command:
                message.subject = ("=>" if self.prefix == "->" else "->") + message.subject[len(self.prefix):]
            
            self._events['on_message'](message)
            
            if is_command:
                self._events['on_command'](message)
                
                command = message.subject[len(self.prefix):].lower()

                if command not in self._commands:
                    continue

                func = self._commands[command]
                func(message)
                server.store(mail_id, '+FLAGS', '\\Deleted')

    def stop(self):
        if not self._running:
            raise Exception("Client is not running")
        
        self._events['on_stop']()
        
        self._running = False
        self._server = None
        
        self.email = None
        self.password = None
