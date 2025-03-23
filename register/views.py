from django.shortcuts import render, redirect
from django.contrib import auth, messages
from register.forms import *


# Create your views here.
def signup(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'register/Signup.html', {"form": form})
    elif request.method == 'POST':
        # Getting Data
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Checking to see if username or email exists
        if User.objects.filter(username=username).first() is not None:
            messages.error(request, 'Username already exists')
        elif User.objects.filter(email=email.lower()).first() is not None:
            messages.error(request, 'Email already exists')
        # Checking Password
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'register/Signup.html', {"form": RegisterForm(request.POST)})

        else:
            if User.objects.filter(username=username).first() is None and User.objects.filter(email=email.lower()).first() is None:
                # Saving User
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                # Login in
                auth.login(request, auth.authenticate(username=username, password=password1))
                return redirect("home")

            else:
                return render(request, 'register/Signup.html', {"form": RegisterForm(request.POST)})



def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'register/Login.html', {"form": form})

    elif request.method == "POST":
        # Getting Username & Password
        username = request.POST["username"]
        password = request.POST["password"]

        # Getting Authenticated with username or email
        user = auth.authenticate(request, username=username, password=password)
        email = auth.authenticate(request, username=User.objects.filter(email=username.lower()).first(), password=password)

        # Checking to see if this user exists
        if user is not None:
            auth.login(request, user)
            return redirect("home")

        elif email is not None:
            auth.login(request, email)
            return redirect("home")

        else:
            # Error Message
            messages.error(request, "Invalid username or password.")
            return render(request, "register/Login.html", {"form": LoginForm(request.POST)})


def logout(request):
    auth.logout(request)
    return redirect('home')