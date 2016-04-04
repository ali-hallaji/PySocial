# -*- coding: utf-8 -*-
# Django Import
from django.core.mail import EmailMultiAlternatives
from django.core.mail import get_connection
from django.template.loader import render_to_string
from email.mime.image import MIMEImage

# PySocial import
from pysocial.settings import BASE_DIR


def welcome_mail(_to):
    connection = get_connection()
    connection.open()
    msg = EmailMultiAlternatives(
        'به گردهمایی پایتونی ها خوش آمدید.',
        '<p> import <strong>python</strong></p>',
        'PySocial پای سوشیال <Info@pysocial.com>',
        _to
    )

    html_content = render_to_string('welcome.html')
    msg.attach_alternative(html_content, "text/html")
    msg.mixed_subtype = 'related'

    image_path = BASE_DIR + '/static/main/img/Welcome.jpg'
    fp = open(image_path, 'rb')
    msg_img = MIMEImage(fp.read())
    fp.close()

    msg_img.add_header('Content-ID', '<{0}>'.format('Welcome.jpg'))
    msg.attach(msg_img)

    msg.send()
    connection.close()
