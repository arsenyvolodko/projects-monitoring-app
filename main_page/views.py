from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect


def home(request):
    if request.user.is_authenticated:
        return redirect('project:all_projects')
    return redirect('loginuser')


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'main_page/loginuser.html', {'form': AuthenticationForm()})  # формочка для регистрации
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'main_page/loginuser.html',
                          {'form': AuthenticationForm(), 'error': "username and password didn't match"})
        else:
            login(request, user)
            return redirect('project:all_projects')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('loginuser')
