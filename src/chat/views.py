from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormMixin
from django.contrib.auth.models import User
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView
from .forms import ComposeForm, GenerateRandomUserForm
from .models import Thread, ChatMessage
from .tasks import create_random_user_accounts

from bs4 import BeautifulSoup 
import requests 
import re 
import sys 
import pprint
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

@cache_page(CACHE_TTL)
class InboxView(LoginRequiredMixin, ListView):
    template_name = 'chat/inbox.html'
    def get_queryset(self):
        SMS = " "
        for e in ChatMessage.objects.all():
            SMS += e.message
            f = open("output.txt", 'wb')
            dd = SMS.encode('utf-8')
            f.write(dd)
            f.close()
        return Thread.objects.by_user(self.request.user)

@cache_page(CACHE_TTL)
class ThreadView(LoginRequiredMixin, FormMixin, DetailView):
    template_name = 'chat/thread.html'
    form_class = ComposeForm
    success_url = './'

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        other_username  = self.kwargs.get("username")
        obj, created    = Thread.objects.get_or_new(self.request.user, other_username)
        if obj == None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        thread = self.get_object()
        user = self.request.user
        message = form.cleaned_data.get("message")
        ChatMessage.objects.create(user=user, thread=thread, message=message)
        return super().form_valid(form)

@cache_page(CACHE_TTL)
class TestView(FormView):
    template_name = 'chat/test.html'
    form_class = GenerateRandomUserForm
    success_url = './'
    def form_valid(self, form):
        create_random_user_accounts.delay(total)
        print ('We are generating your random users! Wait a moment and refresh this page.')
        return super().form_valid(form)

