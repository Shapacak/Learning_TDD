import uuid
import sys
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from accounts.models import Token


def send_login_email(request):
    '''отправить логин на email'''
    email = request.POST.get('email')
    uid = str(uuid.uuid4())
    Token.objects.create(email=email, uid=uid)
    print(f'email {email}, uuid {uid}', file=sys.stderr)
    url = request.build_absolute_uri(f'/accounts/login?uid={uid}')
    send_mail('Your login link for Superlist',
              f'Use this link to login in:\n\n{url}',
              'noreply@superlist',
              [email],)
    return render(request, 'login_email_sent.html')


def login(request):
    '''регистрация в системе'''
    print('login view', file=sys.stderr)
    uid = request.GET.get('uid')
    user = authenticate(uid=uid)
    if user is not None:
        print('auth user')
        auth_login(request, user, backend='accounts.authentication.PasswordlessAuthenticationBackend')
    print(user)
    return redirect('/')

def logout(request):
    '''выход из системы'''
    auth_logout(request)
    return redirect('/')
