import datetime
import random

from django.contrib.auth import authenticate, login, logout
import os
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View
from rest_framework.response import Response

from App.form import RegisterForm
from App.models import User, Userdetail, News, Car
from niupi.settings import BASE_DIR
from App.models import User, Userdetail, List
from niupi.settings import BASE_DIR, APP_PRIVATE_KEY, ALIPAY_PUBLIC_KEY
from tools.file import Fileup
from tools.verifycode import VerifyCode

from App.models import Bus


def index(request):
    if request.method == 'POST':
        start_city = request.POST.get('from')
        end_city = request.POST.get('go')
        buses = Bus.objects.filter(start_city=start_city, end_city=end_city).order_by('start_time')
        print(buses)
        if start_city and end_city:
            return render(request, 'app/ticket.html', locals())
    return render(request, 'app/index.html', locals())


def select(request):
    start_city = request.POST.get('st')
    end_city = request.POST.get('ed')
    print(start_city, end_city)
    if request.method == 'POST':
        start_city = request.POST.get('qian')
        end_city = request.POST.get('hou')
        print(start_city, end_city)
        buses = Bus.objects.filter(start_city=start_city, end_city=end_city).order_by('start_time')
        return render(request, 'app/ticket.html', locals())
    # cars = Bus.objects.filter(start_city=start_city,end_city=end_city)
    return render(request, 'app/ticket.html')


def buy(request):
    print(request.GET, '-----------------')
    bid = request.GET.get('bid')
    uid = request.GET.get('uid')
    print(uid)
    lis = User.objects.filter(uid=uid).first().friends
    sp = lis.split(',')
    print(sp)
    foos = User.objects.filter(uid__in=sp)

    print(foos)
    print(bid)
    bus = Bus.objects.filter(bid=bid).first()
    print(bus)
    return render(request, 'app/buy_before.html', locals())


def userinfo(request):
    userdetail1 = Userdetail.objects.filter(user_uid=request.user.uid)[0]
    # cars = Car.objects.all()
    # a = []
    # for i in cars:
    #     a.append(i.car_uid)
    # if int(request.user.uid) not in a:
    #     car = Car()
    #     car.car_num = request.POST.get('carnum')
    #     car.car_type = request.POST.get('cartype')
    #     car.uid = int(request.user.uid)
    #     car.seats = request.POST.get('seats')
    #     car.save()
    # else:
    car = Car.objects.filter(car_uid=request.user.uid)[0]
    uid = request.GET.get('uid')
    print(uid)
    if request.method == 'POST':
        print(request.POST.get('realname'))
        userdetail1.real_name = request.POST.get('realname')
        userdetail1.birthday = request.POST.get('birthday')
        request.user.email = request.POST.get('email')
        request.user.phone = request.POST.get('phone')
        userdetail1.address = request.POST.get('address')
        car.car_num = request.POST.get('carnum')
        car.car_type = request.POST.get('cartype')
        car.seats = request.POST.get('seats')
        userdetail1.save()
        request.user.save()
        car.save()
        print('----------------------')
        obj = Fileup(request.FILES.get('file'), is_randomname=True)
        path = os.path.join(BASE_DIR, 'static/assets/img/portrait')
        if obj.upload(path) > 0:
            # userdetail = Userdetail.objects.filter(user_uid=uid).first()
            # print(userdetail)
            # print(os.path.join('static/assets/img/portrait',obj.file_name))
            # userdetail.pic = os.path.join('/static/assets/img/portrait',obj.file_name)
            # userdetail.save()
            user = User.objects.filter(uid=uid).first()
            user.portrait = os.path.join('/static/assets/img/portrait', obj.file_name)
            user.save()
            return render(request, 'app/userinfo.html', locals())
        else:
            print(obj.upload(path))
            return HttpResponse('失败')
        # 上传头像
        if request.FILES.get('file'):
            obj = Fileup(request.FILES.get('file'), is_randomname=True)
            path = os.path.join(BASE_DIR,'static/assets/img/portrait')
            if obj.upload(path) > 0:
                # userdetail = Userdetail.objects.filter(user_uid=uid).first()
                # print(userdetail)
                # print(os.path.join('static/assets/img/portrait',obj.file_name))
                # userdetail.pic = os.path.join('/static/assets/img/portrait',obj.file_name)
                # userdetail.save()
                user = User.objects.filter(uid=uid).first()
                user.portrait = os.path.join('/static/assets/img/portrait',obj.file_name)
                user.save()
                return render(request, 'app/userinfo.html',locals())
            else:
                print(obj.upload(path))
                return HttpResponse('失败')
    return render(request, 'app/userinfo.html', locals())


class UserView(View):
    def get(self, request):
        pass

    def post(self, request):
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
                login(request, user)
                print(user.uid)
                userdetail = Userdetail.objects.filter(user_uid=user.uid).first()
                print(userdetail, '--------------------------')
                u = 6
                return redirect(reverse('app:index'), locals())
    return render(request, 'login.html')


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
            user = User.objects.create_user(username=username, password=password, phone=phone)

            user = User.objects.create_user(username=username,password=password,phone=phone)
            user.portrait = '/static/assets/img/basic/cirrus.png'
            user.save()
            userdetail = Userdetail()
            userdetail.user_uid_id = user.uid

            userdetail.save()
            login(request, user)
            userdetail = Userdetail.objects.filter(user_uid=user.uid).first()
            return redirect(reverse('app:index'), locals())
        return render(request, 'register.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'register.html', locals())


def yzm(request):
    vc = VerifyCode()
    res = vc.output()
    request.session['code'] = vc.code
    return HttpResponse(res, 'image/png')


def findpassword(request):
    return render(request, 'findpassword.html', locals())


def pay(request):
    return render(request, 'app/buy.html')


def relation(request):
    # print(request.user.uid)
    str = request.user.friends
    x = str.split(',')
    a = []
    userdetail = Userdetail.objects.all()
    for i in x:
        i = int(i)
        a.append(i)
    if request.GET.get('search'):
        search = request.GET.get('search')
        users = Userdetail.objects.filter(id_num__exact=search)[0]
    if request.GET.get('userid'):
        x = request.GET.get('userid')
        if int(x) not in a:
            str = str+','+x
            userself = User.objects.filter(uid=request.user.uid)[0]
            userself.friends = str
            userself.save()

    return render(request,'app/add_user.html',locals())


# 生产订单的函数
def set(sb):
    oo = []
    PO = []
    for n in range(len(sb)):
        op = []
        for i in range(4):
            i = random.randint(0, 9)
            op.append(i)
        op = ''.join(str(i) for i in op)
        date = datetime.datetime.now()
        detester = date.strftime('%Y-%m-%d %H:%M:%S')
        kko = ''.join(detester.split(' ')[0].split('-')) + op
        oo.append(kko)
    # 乘客编号
    for i in range(4):
        i = random.choice('VASJNAKCDSNOIDAAKNLASDMCACNJ')
        PO.append(i)
    # 订单号
    payment_num = oo[0] + ''.join(PO)
    user_num = oo
    return payment_num, user_num

# 直接购买
def payment(request):
    if request.GET.get('bid'):
        price = request.GET['price']
        uid = request.GET['user']
        bid = request.GET['bid']
        print('订单购买')

        if request.GET.get('hoo'):
            hoo = request.GET.get('hoo').replace('(', '').replace(')', '').replace("'", '').strip('[]').replace(' ','').split(',')
            su = set(hoo)
            print(hoo)
            sb = []
            sun = []
            for i in range(len(hoo)):
                if i % 2 == 0:
                    sb.append(str(hoo[i]))
                elif i % 2 == 1:
                    sun.append(int(hoo[i]))
            print(sb,sun)
            users = User.objects.filter(uid__in=sb)
            kll = {k: v for k, v in zip(users, sun)}
            time = datetime.datetime.now()
            bun = Bus.objects.filter(bid=bid).first()
            PO = su[0]
            # 总票价，保险费，总价
            cash = float(price)
            bcore = float(cash * 0.1)
            num_core = cash + bcore
            return render(request, 'app/payment.html', locals())
        print('直接购买')
        uuo = request.GET.get('uu')
        if uuo:
            sb = uuo.split(',')
            # 用户列表
            suo_list = list(int(i) for i in sb)
            su = set(suo_list)
            s = list(zip(suo_list, su[1]))
            list_pay = List()
            list_pay.num_list = su[0]
            list_pay.price_list = price
            list_pay.list_uid_id = uid
            list_pay.list = s
            list_pay.traffic_id = bid
            list_pay.save()
            PO = su[0]
            buu = Bus.objects.filter(bid=bid).first()
            buu.standby_ticket = int(buu.standby_ticket) - len(suo_list)
            buu.save()
            users = User.objects.filter(uid__in=sb)
            kll = {k: v for k, v in zip(users, su[1])}
            time = datetime.datetime.now()
            bun = Bus.objects.filter(bid=bid).first()
            # 总票价，保险费，总价
            cash = float(price)
            bcore = float(cash * 0.1)
            num_core = cash + bcore
            return render(request, 'app/payment.html', locals())
    return render(request, 'app/payment.html', locals())


# 添加订单
def add_payment(request):
    print('---添加订单---')
    print('000000000000000000')
    suo = request.GET['id']
    print(suo)
    price = request.GET['price']
    uid = request.GET['user']
    bid = request.GET['bid']
    print(bid)
    if suo:
        suo_list = suo.split(',')
        suo_list = list(int(i) for i in suo_list[1:])
        su = set(suo_list)
        s = list(zip(suo_list, su[1]))
        list_pay = List()
        list_pay.num_list = su[0]
        list_pay.price_list = price
        list_pay.list_uid_id = uid
        list_pay.list = s
        list_pay.traffic_id = bid
        buu = Bus.objects.filter(bid=bid).first()
        buu.standby_ticket = int(buu.standby_ticket)-len(suo_list)
        buu.save()
        list_pay.save()
    print('---添加订单结束---')
    return HttpResponse('')

# 订单列表
def pay_list(request):
    print('---订单列表---')
    lists = List.objects.all()
    lists_w = List.objects.filter(status=0)
    lists_a = List.objects.filter(status=2)
    li = lists.first()
    print('---订单结束---')
    return render(request,'app/payment_all.html',locals())



def news(request):
    print(request.user.uid)
    new = News.objects.all()
    userdetail = Userdetail.objects.all()
    newsol = {k:v for k,v in zip(new,userdetail)}
    print(newsol)
    if request.GET.get('read'):
        print('拿到更改按钮了')
        a = request.GET.get('read')
        print(a)
    return render(request, 'app/news.html',locals())


# 支付宝

def ali_buy(request,pay_id,pay_price):
    alipay = AliPay(
        appid='2016101400681426',
        app_notify_url=None,
        # 默认回调url
        app_private_key_string=APP_PRIVATE_KEY,
        # 支付宝的公钥,验证支支付宝回传消息使用用,不是你自自己己的公钥,
        alipay_public_key_string=ALIPAY_PUBLIC_KEY,
        sign_type="RSA2",
        debug=False  # RSA 或者 RSA2  默认False
    )
    # 订单
    order_string = alipay.api_alipay_trade_page_pay(
        # 订单号
        out_trade_no=pay_id,
        #　订单金额
        total_amount=pay_price,
        # 订单名称
        subject='NP'+pay_id,
        # 回调地址
        return_url='http://127.0.0.1:8000',
        # 异步通知商家服务器器地址,postnotify_url="http://localhost:8000/mine/index"使用用默认notify url
    )
    print(order_string,'000000000000000000000000000000000000000000000')
    # 支支付宝网网关
    net = "https://openapi.alipaydev.com/gateway.do?"
    data = {
        "msg": "ok",
        "status": 200,
        "data": {
            "pay_url": net + order_string
        }
    }
    return  HttpResponseRedirect(net + order_string)
    # return net + order_string
    # return Response(data)


def pay_ali(request):
    pay_num = request.GET.get('pay_num')
    pay_price = request.GET.get('pay_price')
    return ali_buy(id,pay_num,pay_price)


def all(request):
    return render(request,'app/payment_all.html')





