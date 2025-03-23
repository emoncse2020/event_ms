from django.shortcuts import render, redirect, HttpResponse
from .forms import CustomRegistrationForm, SignInForm, EditRoleForm, CreateGroupForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch

# Create your views here.

def is_admin(user):
    return user.groups.filter(name="Admin").exists()

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
    print("form error", form.errors)
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

@login_required
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
    
@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    users = User.objects.prefetch_related(Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')).all()

    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = 'No group Assigned'
    return render(request, 'admin/dashboard.html', {"users":users})

@user_passes_test(is_admin, login_url='no-permission')
def edit_group(request, id):
    user = User.objects.get(id=id)
    form = EditRoleForm()

    if request.method == "POST":
        form = EditRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request, f'User {user.username} has been assigned to the {role.name} group')
            return redirect('admin-dashboard')
        
    return render(request, 'admin/edit_group.html', {"form": form})
@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()

    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            role = form.save()
            messages.success(request, f'Group {role.name} has been created successfully')
            return redirect('create-group')
        
    return render(request, 'admin/create_group.html', {"form": form})

@user_passes_test(is_admin, login_url='no-permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()

    return render(request,'admin/group_list.html', {"groups": groups} )
