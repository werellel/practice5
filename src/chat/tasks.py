# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

import string

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

@shared_task
def create_random_user_accounts(total):
    for i in range(total):
        username = 'user_{}'.format(i)
        email = '{}@example.com'.format(username)
        password = 'password'
        # try:
        #     u = User.objects.get(username = username)
        #     u.delete()
        #     messages.sucess(request, "The user is deleted")
        # except:
        #     messages.error(request, "The user not found")
        User.objects.create_superuser(username=username, email=email, password=password)
    return (User.objects.get(username=user_))


@shared_task
def add(x, y):
    return x + y

@shared_task
def mul(x, y):
    return x * y

@shared_task
def xsum(numbers):
    return sum(numbers)


