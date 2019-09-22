import datetime
import random
import re

from alipay import AliPay
from django.contrib.auth import authenticate, login, logout
import os
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View
from rest_framework.response import Response

from App.form import RegisterForm, ChangeForm
from App.models import User, Userdetail, News, Car
from niupi.settings import BASE_DIR
from App.models import User, Userdetail, List
from niupi.settings import BASE_DIR, APP_PRIVATE_KEY, ALIPAY_PUBLIC_KEY
from tools.file import Fileup
from tools.verifycode import VerifyCode
from tools.sms import send_sms

from App.models import Bus


def index(request):
    if request.method == 'POST':
        start_city = request.POST.get('from')
        end_city = request.POST.get('go')
        buses = Bus.objects.filter(start_city=start_city, end_city=end_city).order_by('start_time')
        print(buses)
        if start_city and end_city:
            return render(request, 'app/select.html', locals())
    return render(request, 'app/index.html', locals())


def select(request):
    if request.GET:
        page = request.GET.get('page')
        start_city = request.GET.get('st')
        end_city = request.GET.get('ed')
        buses = Bus.objects.filter(start_city=start_city, end_city=end_city).order_by('start_time')
        paginator = Paginator(buses,1)
        page = paginator.page(int(page))
        buses = page.object_list
        if request.method == 'POST':
            page = request.GET.get('page')
            start_city = request.POST.get('qian')
            end_city = request.POST.get('hou')
            buses = Bus.objects.filter(start_city=start_city, end_city=end_city).order_by('start_time')
            paginator = Paginator(buses, 1)
            page = paginator.page(int(page))
            buses = page.object_list
        return render(request, 'app/select.html', locals())
    return render(request, 'app/select.html', locals())
    # cars = Bus.objects.filter(start_city=start_city,end_city=end_city)




def buy(request):
    if request.GET:
        print('购买详情')
        bid = request.GET.get('bid')
        uid = request.GET.get('uid')
        lis = User.objects.filter(uid=uid).first().friends
        sp = lis.split(',')
        foos = User.objects.filter(uid__in=sp)
        bus = Bus.objects.filter(bid=bid).first()
        suu = int(bus.standby_ticket)
        print('购买结束')
        return render(request, 'app/buy_before.html', locals())
    return render(request, 'app/buy_before.html', locals())



def userinfo(request):
    userdetail1 = Userdetail.objects.filter(user_uid=request.user.uid)[0]

    # 得到汽车车主列表
    cids = Car.objects.all()
    ci = []
    for i in cids:
        ci.append(i.car_uid)

    if request.method == 'POST':
        if request.user.uid not in ci:
            userdetail1.real_name = request.POST.get('realname')
            print(request.POST.get('birthday'),type(request.POST.get('birthday')))
            userdetail1.birthday = request.POST.get('birthday')
            userdetail1.address = request.POST.get('address')
            request.user.email = request.POST.get('email')
            request.user.phone = request.POST.get('phone')
            userdetail1.age = request.POST.get('age')

            userdetail1.save()
            request.user.save()
            print('没车的')
        else:
            car = Car.objects.filter(car_uid=request.user.uid)[0]
            userdetail1.real_name = request.POST.get('realname')
            userdetail1.birthday = request.POST.get('birthday')
            request.user.email = request.POST.get('email')
            request.user.phone = request.POST.get('phone')
            userdetail1.address = request.POST.get('address')
            car.car_num = request.POST.get('carnum')
            car.car_type = request.POST.get('cartype')
            car.seats = request.POST.get('seats')
            userdetail1.age = request.POST.get('age')
            userdetail1.save()
            request.user.save()
            car.save()
            print('有车的')
        print('----------------------')
        obj = Fileup(request.FILES.get('file'), is_randomname=True)
        path = os.path.join(BASE_DIR, 'static/assets/img/portrait')
        # 上传头像
        if request.FILES.get('file'):
            obj = Fileup(request.FILES.get('file'), is_randomname=True)
            path = os.path.join(BASE_DIR,'static/assets/img/portrait')
            if obj.upload(path) > 0:
                user = User.objects.filter(uid=request.user.uid).first()
                user.portrait = os.path.join('/static/assets/img/portrait',obj.file_name)
                user.save()
                userdetail = Userdetail.objects.filter(user_uid=request.user.uid)[0]
                # 生日
                birth = str(userdetail.birthday)
                print(birth, '生日')
                return render(request, 'app/userinfo.html',locals())
            else:
                print(obj.upload(path))
                return HttpResponse('失败')
    userdetail = Userdetail.objects.filter(user_uid=request.user.uid)[0]
    # 生日
    birth = str(userdetail.birthday)
    print(birth, '生日')
    return render(request, 'app/userinfo.html', locals())


class UserView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass





def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # autologin = request.POST.get('cookietime')
        user = authenticate(request, username=username, password=password)
        print('1111111111231231231')
        user2 = User.objects.filter(username=username).first()
        if user2.is_locked == 1:
            errorss = '你的账户已被锁定'
        else:
            if user:
                user.count = 0
                user.save()
                login(request, user)
                print(user.uid)
                userdetail = Userdetail.objects.filter(user_uid=user.uid).first()
                print(userdetail, '--------------------------')
                return redirect(reverse('app:index'), locals())

            else:
                user3 = User.objects.filter(username=request.POST.get('username')).first()
                print(user3.count)
                user3.count += 1
                user3.save()
                if user3.count == 3:
                    user3.is_locked = 1
                    user3.save()
                return render(request, 'login.html', locals())
    return render(request, 'login.html',locals())


def user_logout(request):
    logout(request)
    return redirect(reverse('app:index'))


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        yzm1 = request.POST.get('yzm')
        yzm2 = request.session.get('code')
        print('yzm1:',yzm1)
        print('yzm2:',yzm2)
        sms1 = request.POST.get('sms')
        sms2 = request.session.get('num')
        print('sms1:',sms1)
        print('sms2:',sms2)
        ress = (sms1 == sms2)
        res = (yzm1 == yzm2)
        print(form.is_valid())
        if not res:
            form.errors['yzm'] = "验证码错误"
        if not ress:
            form.errors['sms'] = "手机验证码错误"
        if res and ress and form.is_valid():
            # form.cleaned_data.pop('repassword')
            # form.cleaned_data.pop('yzm')
            # User.objects.create(**form.cleaned_data)
            # user = User()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            phone = form.cleaned_data.get('phone')
            user = User.objects.create_user(username=username, password=password, phone=phone)

            # user = User.objects.create_user(username=username,password=password,phone=phone)
            user.portrait = '/static/assets/img/basic/cirrus.png'
            user.save()
            userdetail = Userdetail()
            userdetail.user_uid_id = user.uid

            userdetail.save()
            login(request, user)
            userdetail = Userdetail.objects.filter(user_uid=user.uid).first()

            # car = Car()
            # car.uid = user.uid
            # car.car_type = ''
            #
            # car.save()
            return redirect(reverse('app:index'), locals())
        return render(request, 'register.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'register.html', locals())

def sms(request):
    if User.objects.filter(username=request.GET.get('nameuser')).first():

        if request.GET.get('phone') == User.objects.filter(username=request.GET.get('nameuser')).first().phone:
            num = str(random.randint(10000, 1000000))
            phone = request.GET.get('phone')
            res = send_sms(phone, {'number': num})
            print(num)
            request.session['num'] = num
            return HttpResponse('发送成功,请接收')
        else:
            return HttpResponse('手机号错误')
    else:
        return HttpResponse('用户不存在')

def sms1(request):
    print(request.GET.get('phone'))
    phone = request.GET.get('phone')
    print(len(phone))
    if len(phone) == 11:
        num = str(random.randint(10000, 1000000))
        res = send_sms(phone, {'number': num})
        print(num)
        request.session['num'] = num
        return HttpResponse('发送成功,请接收')
    else:
        return HttpResponse('请输入正确的手机号')

def yzm(request):
    vc = VerifyCode()
    res = vc.output()
    request.session['code'] = vc.code
    return HttpResponse(res, 'image/png')

# def checkpassword(password):
#     if re.search(r'\d+',password) and \
#        re.search(r'[a-z]',password) and  \
#        re.search(r'[A-Z]',password) and len(password)>=6:
#         return password
#     else:
#         return '密码强度不够'

def findpassword(request):
    # if request.method == 'POST':
    #     users = User.objects.filter(username=request.POST.get('username'))
    #     if users: # 如果有这个用户名：
    #         print(users.first().phone,request.POST.get('mobile'))
    #         if users.first().phone == request.POST.get('mobile'): # 如果表单提交的手机号与上述用户名的手机号一致
    #             sms1 = request.POST.get('sms')
    #             sms2 = request.session.get('num')
    #             ress = (sms1 == sms2)
    #             print('sms1:', sms1)
    #             print('sms2:', sms2)
    #             if ress: #　如果手机验证码通过了
    #                 passwords = request.POST.get('newpassword')
    #                 if checkpassword(passwords) == '密码强度不够': # 如果新密码强度不够checkpassword的要求
    #                     error4 = checkpassword(passwords)
    #                 elif request.POST.get('newpassword') == request.POST.get('renewpassword'):# 如果够要求并且两次输入一致
    #                     # 那么就终于可以将新密码写入到数据库了
    #                     new_password = request.POST.get('newpassword')
    #                     user = auth.authenticate(username=username)
    #                     user.set_password(new_password)
    #                     user.save()
    #                 else:
    #                     error5 = '两次密码不一致'
    #             else:
    #                 error3 = '验证码错误'
    #         else:
    #             error2 = '手机号错误'
    #     else:
    #         error1 = '用户不存在'
    if request.method == 'POST':
        form = ChangeForm(request.POST)
        sms1 = request.POST.get('sms')
        sms2 = request.session.get('num')
        print('sms1:',sms1)
        print('sms2:',sms2)
        ress = (sms1 == sms2)
        print(form.is_valid())
        if not ress:
            form.errors['sms'] = "手机验证码错误"
        if User.objects.filter(username=request.POST.get('username')).first():
            print('在这里')
            print(request.POST.get('username'))
            if request.POST.get('phone') != User.objects.filter(username=request.POST.get('username')).first().phone:
                form.errors['phone'] = "手机号不匹配"
            if ress and form.is_valid():
                # form.cleaned_data.pop('repassword')
                # form.cleaned_data.pop('yzm')
                # User.objects.create(**form.cleaned_data)
                user = User.objects.get(username=request.POST.get('username'))
                user.password = make_password(request.POST.get('newpassword'))
                user.save()
                # user = User.objects.create_user(username=username,password=password,phone=phone)
                return redirect(reverse('app:index'), locals())
        else:
            form.errors['username'] = '用户不存在'


        return render(request, 'findpassword.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'findpassword.html', locals())


def pay(request):
    return render(request, 'app/buy.html')


def relation(request):
    # 删除好友
    if request.GET.get('uid'):
        uid = request.GET['uid']
        user1 = User.objects.filter(uid=request.user.uid).first()
        lists = user1.friends.split(',')
        lists.remove(uid)
        friendss = ','.join(lists)
        user1.friends = friendss
        user1.save()
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
    #         userself = User.objects.filter(uid=request.user.uid)[0]
    # userdetail = Userdetail.objects.all()
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
            kel = List.objects.filter(lid=request.GET.get('hoo')).first()
            print(kel)
            hoo = kel.list.replace('(', '').replace(')', '').replace("'", '').strip('[]').replace(' ','').split(',')
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
            PO = kel.num_list
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
        print(suo_list)
        su = set(suo_list)
        s = list(zip(suo_list, su[1]))
        print(s)
        list_pay = List()
        list_pay.num_list = su[0]
        list_pay.price_list = price
        list_pay.list_uid_id = uid
        list_pay.list = s
        list_pay.traffic_id = bid
        buu = Bus.objects.filter(bid=bid).first()
        if int(buu.standby_ticket) >= len(suo_list):
            print(len(suo_list),int(buu.standby_ticket))
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
    lists_d = List.objects.filter(status=1)
    lists_a = List.objects.filter(status=2)
    li = lists.first()
    print('---订单结束---')
    return render(request, 'app/pay_list.html', locals())



def news(request):
    if request.GET.get('nid'):
        print('拿到ajax了')
        print('----=====')
        print(request.GET.get('nid'))
        new1 = News.objects.filter(nid=request.GET.get('nid')).first()
        print(new1.is_read)
        if new1.is_read == 0:
            new1.is_read = 1
            new1.save()
            print(new1.is_read)

    print(request.user.uid)
    new = News.objects.filter(belong_user=request.user.uid)
    newss = new.filter(is_read=0)
    userdetail = Userdetail.objects.all()
    newsol = {k:v for k,v in zip(new,userdetail)}

    print(newsol)
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
        return_url='http://127.0.0.1:8000/send_new?payment_num='+pay_id+'&code=0',
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
    print('---')
    return render(request, 'app/pay_list.html')


def send_new(request):
    print('取消订单')
    if request.GET['code']== '1':
        pay_de = request.GET['id']
        print(pay_de)
        payment0 = List.objects.filter(num_list=pay_de).first()
        print(payment0)
        payment0.status = 1
        payment0.save()
        new0 = News()
        new0.set_time = datetime.datetime.now()
        new0.content = '你的订单'+pay_de+'已经取消,您可以在订单页面查看！'
        new0.belong_user_id = request.user.uid
        new0.save()
    print('已完成订单')
    print(request.GET['code'])
    if request.GET['code']== '0':
        print(request.GET['code'])
        pay_id = request.GET.get('payment_num')
        print(pay_id)
        payment1 = List.objects.filter(num_list=pay_id).first()
        print(payment1)
        payment1.status = 2
        payment1.save()
        new1 = News()
        new1.set_time = datetime.datetime.now()
        new1.content = '你的订单' + pay_id + '已经支付,感谢您使用牛皮网！'
        new1.belong_user_id = request.user.uid
        new1.save()
    return render(request,'app/success.html')

