#for confirmation emails
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from .token import account_activation_token
from django.core.mail import EmailMessage

def send_activation_mail(request, user, form):
    #send activation mail

    current_site = get_current_site(request)
    email_subject = 'Activate Your Account'
    message = render_to_string('users/activate_account.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    to_email = form.cleaned_data.get('email')
    email = EmailMessage(email_subject, message, to=[to_email])
    email.send()
