from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.forms import ModelForm
from .models import Funcionario,PerguntaSimples,Jogo
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

@csrf_protect
def login(request):
    if request.method == 'GET' :
       return render(request,'login/login.html')
    elif request.method =="POST":
        user = authenticate(username = request.POST.get('username'), password = request.POST.get('password') )
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            return redirect('')

@csrf_protect
def registro (request):
    if request.method == 'GET' :
       return render(request,'login/registro.html')
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
                return render(request,'login/registro.html')

def home(request):
    return redirect(request,'home')


def jogo(request):
    data = {}
    try:
        data['perguntas'] = PerguntaSimples.objects.all()
        random.shuffle(data['perguntas'])
        return render(request,'login/jogo.html',data)
    except:
        return render(request,'login/jogo.html',data)
    return render(request,'login/jogo.html',data)
    
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
        return render(request,'login/addPergunta.html')
    if request.method == 'POST':
        if request.POST.get('resposta') == 'on':
            boolresposta = True
        else:
            boolresposta = False
        pergunta = PerguntaSimples(descricao=request.POST.get('descricao'),resposta=boolresposta)
        pergunta.save()
        return redirect('/jogo/')

