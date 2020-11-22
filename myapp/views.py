from django.http import HttpResponse
from django.shortcuts import render
from .models import Send
from .models import Recieve
import imaplib
import email
import smtplib

def index(request):
    host = 'imap.gmail.com'
    username = 'Sir Here you can enter your email id'
    password = 'Sir here you can enter your Password'

    mail = imaplib.IMAP4_SSL(host)
    mail.login(username, password)
    mail.select("inbox")
    _, search_data = mail.search(None, 'UNSEEN')
    m_num = search_data[0].split()
    global get_message
    get_message = len(m_num)
    

    if get_message == 0:
        params = {"s": "You don't get new message yet now"}
    else:
        params = {"s":(f"You get {get_message} new message")}

    return render(request, 'base.html', params)


def send(request):
    to = request.POST.get('send_to', 'default')
    subject = request.POST.get('subject', 'default')
    message = request.POST.get('message', 'default')
    my_message = "Subject:{}\n\n{}".format(subject,message)
    username = 'Sir Here you can enter your email id'
    password = 'Sir Here you can enter your Password'
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(username, password)
    mail.sendmail(username, to, my_message)
    mail.close()
    send_email = Send(to=to, subject=subject, message=message)
    send_email.save()

    return HttpResponse("Hello Your message has been sent ...")


def recieve(request):
    host = 'imap.gmail.com'
    username = 'Sir Here you can enter your email id'
    password = 'Sir Here you can enter your password'

    def get_inbox():
        mail = imaplib.IMAP4_SSL(host)
        mail.login(username, password)
        mail.select("inbox")
        _, search_data = mail.search(None, 'UNSEEN')
        my_message = []
        for num in search_data[0].split():
            email_data = {}
            _, data = mail.fetch(num, '(RFC822)')
            # print(data[0])
            _, b = data[0]
            email_message = email.message_from_bytes(b)
            for header in ['subject', 'to', 'from', 'date']:
                email_data[header] = email_message[header]
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True)
                    email_data['body'] = body.decode()
                elif part.get_content_type() == "text/html":
                    html_body = part.get_payload(decode=True)
                    email_data['html_body'] = html_body.decode()
            my_message.append(email_data)
        return my_message


    
    if get_message == 0:
        return HttpResponse("You don't get new message yet.. I will inform you when you will get a new message")
    else:
        my_inbox = get_inbox()
        print(my_inbox)
        subject = my_inbox[0]['subject']
        to = my_inbox[0]['to']
        get_by = my_inbox[0]['from']
        date = my_inbox[0]['date']
        message = my_inbox[0]['body']
        recieve_email = Recieve(subject=subject, to=to, get_by = get_by, message=message)
        recieve_email.save()
        params = {'subject': subject, 'to': to, 'Get_by': get_by, 'date': date, 'message': message }
        return render(request, 'recieve.html', params)