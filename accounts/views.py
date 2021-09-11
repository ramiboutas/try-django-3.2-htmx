from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Create your views here.

def user_register(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user_obj = form.save()
        return redirect(reverse_lazy('user_login'))
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(request.GET.get('next'))
    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'accounts/login.html', context)

def user_logout(request):
    print(request)
    if request.user.is_authenticated:
        if request.method == 'POST':
            logout(request)
            return redirect(reverse_lazy('user_login'))
    context = {}
    return render(request, 'accounts/logout.html', context)
