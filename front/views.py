# Create your views here.

# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from front.forms import RegistrationForm, LoginForm
from django.contrib.auth.models import User


def front_index(request, template="front/index.html"):
    values = {
        'index': True,
    }
    c = RequestContext(request, values)
    return render_to_response(template, c)

def front_about(request, template="front/about.html"):
    values = {
        'about': True,
    }
    c = RequestContext(request, values)
    return render_to_response(template, c)

def front_register(request, template="front/register.html"):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = User.objects.create_user(username, email, password)
            new_user = authenticate(username=username, password=password)
            login(request, new_user)
            #send a confirmation message
            messages.success(request, "Account Created!")
            return HttpResponseRedirect(reverse("dashboard"))
    else:
        form = RegistrationForm()

    values = {
        'form': form,
        'register': True,
    }
    c = RequestContext(request, values)
    return render_to_response(template, c)

def front_login(request, template="front/login.html"):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('dashboard'))
    else:
        form = LoginForm()

    values = {
        'form':form,
        'login': True,
    }
    c = RequestContext(request, values)
    return render_to_response(template, c)




