from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def signup(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'accounts/signup.html', {
                'form' : form
                })
    else:
        return render(request, 'accounts/signup.html', {
                'form' : UserRegisterForm()
                })