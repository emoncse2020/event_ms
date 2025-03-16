from django.shortcuts import render, redirect, HttpResponse
from .forms import CustomRegistrationForm, SignInForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator

# Create your views here.

def sign_up(request):
    form = CustomRegistrationForm()

    if request.method == "POST":
        form = CustomRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()
            messages.success(request, "A activation url sent to your mail.Sign up By clicking url. Please check you email")
            return redirect('sign-in')
    
    return render(request, 'users/sign-up.html', {"form": form})

def sign_in(request):
    form = SignInForm()
    if request.method == "POST":
        form = SignInForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        
    return render (request, 'users/sign-in.html', {"form": form})


def sign_out(request):
    if request.method =="POST":
        logout(request)
        return redirect('sign-in')     
    
def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active=True
            user.save()
            return redirect('sign-in')
        
        else:
            return HttpResponse("Invalid id or token")
    
    except User.DoesNotExist:
        return HttpResponse("User not found")