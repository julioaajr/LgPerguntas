from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from .models import Funcionario,PerguntaSimples,Jogo
import random
# Create your views here.

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
        print('erro')
        return render(request,'login/jogo.html',data)
    return render(request,'login/jogo.html',data)
    
    