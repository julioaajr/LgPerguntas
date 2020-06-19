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
    data['perguntas']=[]
    try:
        data['pergunta'] = PerguntaSimples.objects.all().order_by('?')
        x=0
        while x < 5:
            data['perguntas'].append(data['pergunta'][x])
            x+=1
        return render(request,'jogo.html',data)
    except:
        return render(request,'jogo.html',data)
    return render(request,'jogo.html',data)
    
@csrf_protect
def valida_reposta(request):
    if request.method =='POST':
        perguntas = request.POST.getlist('pergunta')
        respostas = request.POST.getlist('resposta')

        data = []
        pontuacao=0
        for i in perguntas:
            try:
                y = i in respostas
                vp = PerguntaSimples.objects.get(id=i,resposta=y)
                vp.acertos+=1
                vp.save()
                pontuacao+=1
            except:
                try:
                    pe = PerguntaSimples.objects.get(id=i)
                    pe.erros +=1
                    pe.save()
                except:
                    None
        print(pontuacao)
        try:
            usuario = request.user
            jogo = Jogo(jogador=usuario.id, pontuacao = pontuacao, nome_jogador = usuario.username)
            jogo.save()
            print (jogo.data_jogo)
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
    data = {}

    if request.user.is_superuser or request.user.is_staff:
        try:
            data['acertos']= PerguntaSimples.objects.all().order_by('-acertos')
            print(data['acertos'])
            data['erros']=PerguntaSimples.objects.all().order_by('-erros')
            data['melhores']=Jogo.objects.all().order_by('-pontuacao')[:5]

            if request.user.is_staff:
                data['score']=Jogo.objects.filter(jogador=request.user.id).order_by('-pontuacao')
        except:
            None
    else:
        try:
            data['score']=Jogo.objects.filter(jogador=request.user.id).order_by('-pontuacao')
        except:
            None
    return render(request, 'home.html',data)