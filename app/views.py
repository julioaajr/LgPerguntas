from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.forms import ModelForm
from .models import Funcionario,PerguntaSimples,Jogo
from django.contrib import messages
import random
from datetime import datetime

# Create your views here.

class SalvaPontuacao(ModelForm):
    class Meta:
        model = Jogo
        fields = ['jogador','pontuacao']

class PerguntaSimplesForm(ModelForm):

    class Meta:
        model: PerguntaSimples
        fields = ['descricao','resposta']

def login_user(request):
    return render(request, 'login.html')


@csrf_protect
def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "usuário e senha invalido favor tentar novamente.")
    return redirect('/login/')

def logout_user(request):
    logout(request)
    return redirect('/login/')

@csrf_protect
def registro (request):
    if request.method =='POST':
        username = request.POST.get('username')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        rpassword = request.POST.get('rpassword')
        is_superuser = False
        is_staff = True
        is_active = True
        date_joined = datetime.now()
        if (password == rpassword):
            try:
                user = user.objects.create_user(username=username, password=password, is_superuser=False, is_staff=True, is_active=True)
                user.save()
                return redirect('/')
            except:
                return render(request,'registro.html')
    return render(request,'registro.html')


def jogo(request):
    data = {}
    try:
        data['perguntas'] = PerguntaSimples.objects.all().order_by('?')
        return render(request,'jogo.html',data)
    except:
        return render(request,'jogo.html',data)
    return render(request,'jogo.html',data)
    
@csrf_protect
def valida_reposta(request):
    if request.method =='POST':
        perguntas = request.POST.getlist('pergunta')
        #respostas = request.POST.getlist('resposta')
        data = []
        point = 0
        print(request.POST)

        print(perguntas)
        for i in perguntas:
            try:
                # data.append(PerguntaSimples.objects.get(id=i,resposta=i in respostas))
                print(respostas[i])
                vp = PerguntaSimples.objects.get(id= int(i))
                print(vp.resposta)
                if (vp.resposta == respostas[i]):
                   point = point + 1
                   print (point) 
            except:   
                None
                
        try:
            usuario = AuthUser.objects.get(pk=request.user.id)
            jogo = Jogo(jogador=usuario,pontuacao=points)
            jogo.save()
        except:
            None
        return redirect('/jogo/')

def Cadastra_Pergunta(request):
    if request.method == 'GET':
        return render(request,'addPergunta.html')
    if request.method == 'POST':
        if request.POST.get('resposta') == 'on':
            boolresposta = True
        else:
            boolresposta = False
        pergunta = PerguntaSimples(descricao=request.POST.get('descricao'),resposta=boolresposta)
        pergunta.save()
        return redirect('/jogo/')

def registraComplexa(request):
    if request.method == 'GET':
        return render(request,'login/addComplexa.html')
    if request.method == 'POST':
        if request.POST.get('resposta') == 'on':
            boolresposta = True

        else:
            boolresposta = False
        alternativas = Alternativas(descricao=request.POST.get('descricao'),resposta=boolresposta)
        alternativas.save()
        return redirect('/jogo/')


@login_required(login_url='/login/')
def home(request):
    return render(request, 'home.html')