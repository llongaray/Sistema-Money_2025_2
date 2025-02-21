from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")  # Redireciona para a home ou dashboard
        else:
            messages.error(request, "Usuário ou senha inválidos.")

    return render(request, "usuarios/login.html")  # Renderiza o template de login

def logout_view(request):
    logout(request)
    return redirect("usuarios:login")  # Redireciona para a página de login
