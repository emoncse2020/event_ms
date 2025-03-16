from django.shortcuts import render, redirect
from .forms import CustomRegistrationForm
from django.contrib import messages

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



            