from django.shortcuts import render
from first_app import forms


from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(request,'first_app/index.html')

@login_required
def special(request):
    # Remember to also set login url in settings.py!
    return HttpResponse("You are logged in. Nice!")

@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('index'))

@login_required
def optionchain(request):
    return render(request,'first_app/optionchain.html',{})

def userLogin(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('index'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'first_app/user_login.html', {})

def newUser(request):
    loginform = forms.createNewUser()

    if request.method == 'POST':
        loginform = forms.createNewUser(request.POST)

        if loginform.is_valid():
            loginform.save(commit=True)
            return index(request)

    return render(request,"first_app/register.html",context={'loginform': loginform})
