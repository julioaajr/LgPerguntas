from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.forms import ModelForm
from .models import Funcionario,PerguntaSimples,Jogo
from django.contrib import messages
import random

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
    #a funcao random nao funcionana ele entra no try mas nao executa o random e ele passa pro except
    try:
        data['perguntas'] = PerguntaSimples.objects.all()
        teste = data['perguntas']
        print(teste)
        random.shuffle(teste)
        
        data['perguntass'] = random.sample(data['perguntas'],len(data['perguntas']))
        print('---------------------------------linha 77')
        print(teste)
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
        for i in perguntas:
            try:
                data.append(PerguntaSimples.objects.get(id=i,resposta=i in respostas))
            except:
                None
        print(len(data))
        jogoJson = {
            'usuario': request.user,
            'pontuacao': (len(data))
        }
        jogo = SalvaPontuacao(jogoJson)
        jogo.save()
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