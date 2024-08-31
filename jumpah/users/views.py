from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password_repeat = request.POST['password_repeat']

        if password == password_repeat:
            print("PASSWORDS ARE MATCHED")
            if User.objects.filter(email=email).exists():
                messages.info(request, 'This email is taken.')
                print("YOU ARE IN BLOCK EMAIL MATCH")
                try:
                    return redirect('signup')
                except:
                    print("ERROR REDIRECTING IN EMAIL CHECKER")
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'This username is taken.')
                print("CHECKING USERNAME IF EXIST")
                try:
                    return redirect('signup')
                except:
                    print("ERROR IN USERNAME PART")
            else:
                print("USER SAVING")
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                try:
                    return redirect('/')
                except:
                    print("ERROR IN RIDIRECT OF SAVE")
        else:
            messages.info(request, 'Passwords are not matched.')
            return redirect('signup')
    else:
        return render(request, 'signup.html')


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect("home")
        else:
            messages.info(request, "Credentials Invalid")
            return redirect("login")
    return render(request, "login.html")

@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    return redirect("login")
