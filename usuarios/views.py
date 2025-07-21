from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_django, logout as logout_django
from .models import Evento

# LOGIN
def login(request):
    if request.method == "GET":
        return render(request, 'usuarios/login.html')
    else:
        username = request.POST.get('email')
        senha = request.POST.get('senha')
        user = authenticate(username=username, password=senha)

        if user:
            login_django(request, user)
            return render(request, 'usuarios/home.html')
        else:
            return HttpResponse('E-mail ou senha inválidos!')

# LOGOUT
def logout(request):
    if request.user.is_authenticated:
        logout_django(request)
        return render(request, 'usuarios/login.html')
    return HttpResponse("Você não acessou sua conta ainda!")

# CADASTRO DE USUÁRIO
def cadastro(request):
    if request.method == "GET":
        return render(request, 'usuarios/cadastro.html')
    else:
        username = request.POST.get('email')
        email = request.POST.get('email')
        password = request.POST.get('senha')
        first_name = request.POST.get('nome')

        if User.objects.filter(username=username).exists():
            return HttpResponse("Usuário já existente!")
        else:
            User.objects.create_user(username=username, email=email, password=password, first_name=first_name)
            return render(request, 'usuarios/login.html')

# HOME
def home(request):
    if request.user.is_authenticated:
        return render(request, 'usuarios/home.html')
    return HttpResponse("Faça o login para acessar!")


def cadastrar_evento(request):
    if request.method == "GET":
        return render(request, 'usuarios/cadastro_evento.html')
    else:
        titulo = request.POST.get('titulo')
        data = request.POST.get('data')
        local = request.POST.get('local')
        descricao = request.POST.get('descricao')

        if Evento.objects.filter(titulo=titulo, data=data).exists():
            return HttpResponse("Este evento já foi cadastrado!")
        else:
            Evento.objects.create(titulo=titulo, data=data, local=local, descricao=descricao)
            return render(request, 'usuarios/home.html')


def visualizar_eventos(request):
    if request.method == "GET":
        eventos = Evento.objects.all()
    else:
        local = request.POST.get('local')
        if local == "Todos os locais":
            eventos = Evento.objects.all()
        else:
            eventos = Evento.objects.filter(local=local)
    return render(request, 'usuarios/visualizar_eventos.html', {'lista_eventos': eventos})


def alterar_evento(request):
    if request.user.is_authenticated:
        eventos = Evento.objects.all()
        return render(request, 'usuarios/alterar_evento.html', {'lista_eventos': eventos})
    return HttpResponse("Faça o login para acessar!")


def excluir_evento_confirmar(request, pk):
    if request.user.is_authenticated:
        evento = get_object_or_404(Evento, pk=pk)
        return render(request, 'usuarios/excluir_evento.html', {'evento': evento})
    return HttpResponse("Faça o login para acessar!")


def excluir_evento(request, pk):
    if request.user.is_authenticated:
        evento = get_object_or_404(Evento, pk=pk)
        evento.delete()
        return redirect('alterar_evento')
    return HttpResponse("Faça o login para acessar!")


def editar_evento_confirmar(request, pk):
    if request.user.is_authenticated:
        evento = get_object_or_404(Evento, pk=pk)
        return render(request, 'usuarios/editar_evento.html', {'evento': evento})
    return HttpResponse("Faça o login para acessar!")


def editar_evento(request, pk):
    if request.user.is_authenticated and request.method == "POST":
        titulo = request.POST.get('titulo')
        data = request.POST.get('data')
        local = request.POST.get('local')
        descricao = request.POST.get('descricao')

        Evento.objects.filter(pk=pk).update(titulo=titulo, data=data, local=local, descricao=descricao)
        return redirect('alterar_evento')
    return HttpResponse("Faça o login para acessar!")
        
