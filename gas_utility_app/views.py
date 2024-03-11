from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ServiceRequest, Account
from .forms import *

def customer_signup(request):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('login')  # Redirect to customer dashboard after signup
    else:
        form = CustomerSignUpForm()
    return render(request, 'customer/customer_signup.html', {'form': form})

def staff_member_signup(request):
    if request.method == 'POST':
        form = StaffMemberSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True  # Set is_staff to True for staff members
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('login')  # Redirect to staff dashboard after signup
    else:
        form = StaffMemberSignUpForm()
    return render(request, 'staff/staff_member_signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('admin_dashboard')  # Redirect to admin dashboard
                elif user.is_staff:
                    return redirect('support_request_list')  # Redirect to staff dashboard
                else:
                    return redirect(reverse('service_request_form'))  # Redirect to service request form
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def Customer_home(request):
    return render(request, 'customer/service_request_form.html')

def Staff_home(request):
    return render(request,'staff/support_request_list.html')


@login_required
def service_request_submit(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.customer = request.user
            service_request.save()
            return redirect('service_request_list')
    else:
        form = ServiceRequestForm()
    return render(request, 'service_request_submit.html', {'form': form})

@login_required
def service_request_list(request):
    service_requests = ServiceRequest.objects.filter(customer=request.user)
    return render(request, 'service_request_list.html', {'service_requests': service_requests})

@login_required
def account_info(request):
    account = Account.objects.get(user=request.user)
    return render(request, 'customer/account_info.html', {'account': account})

@login_required
def account_update(request):
    account = Account.objects.get(user=request.user)
    if request.method == 'POST':
        form = AccountUpdateForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('account_info')
    else:
        form = AccountUpdateForm(instance=account)
    return render(request, 'account_update.html', {'form': form})

@login_required
def support_tool(request):
    if not request.user.is_staff:
        return redirect('login')  # Redirect non-staff users
    service_requests = ServiceRequest.objects.all()
    return render(request, 'support_tool.html', {'service_requests': service_requests})

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')  # Redirect to the home page or any other desired page after logout
