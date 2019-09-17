from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View

from App.form import RegisterForm
from App.models import User
from tools.verifycode import VerifyCode

from App.models import Bus


def index(request):
    if request.method == 'POST':
        start_city = request.POST.get('from')
        end_city = request.POST.get('go')
        buses = Bus.objects.filter(start_city=start_city,end_city=end_city).order_by('start_time')
        if start_city and end_city:

            return render(request, 'app/select.html',locals())
    return render(request,'app/index.html')

def select(request):
    if request.method == 'POST':
        start_city = request.POST.get('from')
        end_city = request.POST.get('go')
        print(start_city)
    # cars = Bus.objects.filter(start_city=start_city,end_city=end_city)
    return render(request,'app/select.html')

def buy(request):
    return render(request,'app/buy.html')

def userinfo(request):
    return render(request,'userinfo.html')


class UserView(View):
    def get(self,request):
        pass
    def post(self,request):
        pass





def login(request):
    if request.method == 'POST':
        if request.POST.get('loginsubmit'):
            username = request.POST.get('username')
            password = request.POST.get('password')
            # autologin = request.POST.get('cookietime')

            user = authenticate(request, username=username, password=password)
            if user:
                return redirect(reverse('app:index'))
    return render(request,'login.html')


def logout(request):
    return None


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        yzm1 = request.POST.get('code')
        yzm2 = request.session.get('code')
        res = (yzm1 == yzm2)
        if not res:
            form.errors['yzm'] = "验证码错误"
        if res and form.is_valid():
            form.cleaned_data.pop('repassword')
            form.cleaned_data.pop('yzm')
            User.objects.create(**form.cleaned_data)
            return render(request,'register.html',{'form':form})
        return render(request,'register.html',{'form':form})
    else:
        form = RegisterForm()
        return render(request,'register.html',locals())


def yzm(request):
    vc = VerifyCode()
    res = vc.output()
    request.session['code'] = vc.code
    return HttpResponse(res,'image/png')