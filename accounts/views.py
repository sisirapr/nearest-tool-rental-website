# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from accounts.forms import UserAdminCreationForm
from users.forms import Profileform


def register(req):
    form = UserAdminCreationForm()
    if req.method == 'POST':
    	form = UserAdminCreationForm(req.POST)
    	if form.is_valid():
    		form.save()
    		return redirect('login')
    return render(req, 'register.html', {'form': form})