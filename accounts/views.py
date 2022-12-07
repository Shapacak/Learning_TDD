from django.urls import reverse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages, auth
from .models import Token
import sys


def send_login_email(request):
    '''отправка ключа для входа на email'''
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(reverse('login') + '?token=' + str(token.uid))
    message_body = f'Use this link to login\n\n{url}'
    send_mail('Your login link for Superlists',
              message_body,
              'noreply@superlist',
              [email])
    messages.success(request, message='Проверьте свою почту, мы отправили Вам ссылку для входа на сайт')
    return redirect('/')


def login(request):
    user = auth.authenticate(request=request)
    if user is not None:
        auth.login(request, user)
    return redirect('/')


def logout(request):
    auth.logout(request)
    messages.success(request, message='Вы вышли из системы')
    return redirect('/')

