from django.conf import settings
from django.db.models import signals

from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string, get_template



def send_test_results(instance, created, **kwargs):
    print instance.request.POST
    pass