from django.contrib.auth import authenticate, login, logout
import os
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View

from App.form import RegisterForm
from App.models import User, Userdetail
from niupi.settings import BASE_DIR
from tools.file import Fileup
from tools.verifycode import VerifyCode

from App.models import Bus


def index(request):
    if request.method == 'POST':
        start_city = request.POST.get('from')
        end_city = request.POST.get('go')
        buses = Bus.objects.filter(start_city=start_city,end_city=end_city).order_by('start_time')
        print(buses)
        if start_city and end_city:

            return render(request, 'app/picket.html', locals())
    return render(request,'app/index.html',locals())

def select(request):
    if request.method == 'POST':
        start_city = request.POST.get('from')
        end_city = request.POST.get('go')
        print(start_city)
    # cars = Bus.objects.filter(start_city=start_city,end_city=end_city)
    return render(request, 'app/picket.html')

def buy(request):
    bid = request.GET.get('bid')
    print(bid)
    bus = Bus.objects.filter(bid=bid).first()
    print(bus)
    return render(request, 'app/buy_before.html',locals())

def userinfo(request):
    # 上传头像
    uid = request.GET.get('uid')
    print(uid)
    if request.method == 'POST':
        print('----------------------')
        obj = Fileup(request.FILES.get('file'), is_randomname=True)
        path = os.path.join(BASE_DIR,'static/assets/img/portrait')
        if obj.upload(path) > 0:
            userdetail = Userdetail.objects.filter(user_uid=uid).first()
            print()
            print(os.path.join('static/assets/img/portrait',obj.file_name))
            userdetail.pic = os.path.join('static/assets/img/portrait',obj.file_name)
            userdetail.save()
            user = User.objects.filter(uid=uid).first()
            return render(request, 'app/userinfo.html',locals())
        else:
            return HttpResponse('失败')
    return render(request, 'app/userinfo.html', locals())


class UserView(View):
    def get(self,request):
        pass
    def post(self,request):
        pass





def user_login(request):
    if request.method == 'POST':
        if request.POST.get('loginsubmit'):
            username = request.POST.get('username')
            password = request.POST.get('password')
            # autologin = request.POST.get('cookietime')

            user = authenticate(request, username=username, password=password)
            print(user)
            if user:
                login(request,user)
                return redirect(reverse('app:index'))
    return render(request,'login.html')


def user_logout(request):
    logout(request)
    return redirect(reverse('app:index'))


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        yzm1 = request.POST.get('yzm')
        yzm2 = request.session.get('code')
        res = (yzm1 == yzm2)
        if not res:
            form.errors['yzm'] = "验证码错误"
        if res and form.is_valid():
            # form.cleaned_data.pop('repassword')
            # form.cleaned_data.pop('yzm')
            # User.objects.create(**form.cleaned_data)
            # user = User()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            phone = form.cleaned_data.get('phone')
            user = User.objects.create_user(username=username,password=password,phone=phone)
            login(request,user)
            return redirect(reverse('app:index'))
        return render(request,'register.html',{'form':form})
    else:
        form = RegisterForm()
        return render(request,'register.html',locals())

def yzm(request):
    vc = VerifyCode()
    res = vc.output()
    request.session['code'] = vc.code
    return HttpResponse(res,'image/png')


def findpassword(request):
    return render(request,'findpassword.html',locals())


def pay(request):
    return render(request,'app/buy.html')


def relation(request):
    return render(request,'app/add_user.html')


def payment(request):
    return render(request, 'app/payment.html')


def news(request):
    return render(request, 'app/news.html')
