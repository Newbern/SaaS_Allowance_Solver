from django.shortcuts import render
from register.forms import *

# Create your views here.
def signup(request):
    form = RegisterForm()
    return render(request, 'register/Signup.html', {"form": form})

def login(request):
    return render(request, 'register/Signup.html', {})

def logout(request):
    return render(request, 'register/Signup.html', {})