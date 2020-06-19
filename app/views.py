from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Funcionario,PerguntaSimples,Jogo, AuthUser
from django.shortcuts import render, redirect
from django.views.decorators.csrf  import csrf_protect, csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import date
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
        is_staff = request.POST.get("is_staff")
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        if is_staff == None:
            is_staff= bool(False)
        else:
            is_staff= bool(True)
        print('-username-'+username+'--nome-'+first_name+'--setor-'+last_name+'--pass--')
        
        try:
            user = User.objects.create_user(username=username, last_name=last_name, password='123456789', is_superuser=0, is_staff=is_staff)
            user.save()
            y = AuthUser.objects.get(id=user.id)
            if(request.user.is_superuser and request.user.is_staff):
                x = AuthUser.objects.get(id=request.user.id)
            elif(request.user.is_staff):
                print('linha76')
                a = AuthUser.objects.get(id=request.user.id)
                xy = Funcionario.objects.get(usuario = a)
                print('linha78')
                x = xy.empresa
            f = Funcionario(empresa=x,usuario=y)
            f.save()
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
            jogo = Jogo(jogador=usuario.id, pontuacao = pontuacao, nome_jogador = usuario.first_name)
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



@login_required(login_url='/login/')
def home(request):
    data = {}

    if request.user.is_superuser or request.user.is_staff:
        try:
            data['acertos']= PerguntaSimples.objects.all().order_by('-acertos')[:5]
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