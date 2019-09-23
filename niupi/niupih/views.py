import datetime

from django.contrib.auth import authenticate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse

from App import form
from App.form import RegisterForm
from App.models import User, Userdetail, Car, Bus
from niupih.forms import AdminForm, BusForm, BusForm2


def index(request):
    id = request.session.get('uid')
    if id:
        admin = Userdetail.objects.filter(user_uid=id).first()
        return render(request, 'niupih/index.html', locals())
    return redirect(reverse('myadmin:login'), locals())


def login(request):
    if request.method == 'POST':
        admin_name = request.POST.get('admin')
        password = request.POST.get('password')
        admin = authenticate(request, username=admin_name, password=password, type=1)
        if admin:
            request.session['uid'] = admin.uid
            return redirect(reverse('myadmin:index'), locals())
    return render(request, 'niupih/login-2.html', locals())


def logout(request):
    request.session.delete()
    return redirect(reverse('myadmin:login'), locals())
    # return render(request, 'niupih/login-2.html', locals())


def order_list(request):
    return render(request, 'niupih/order_list.html', locals())


def user_list(request):
    id = request.session.get('uid')
    if id:
        admin = Userdetail.objects.filter(user_uid=id).first()
        userdetail = Userdetail.objects.all()
        return render(request, 'niupih/user_list.html', locals())
    return redirect(reverse('myadmin:login'), locals())
    # admin = Userdetail.objects.filter(user_uid=id).first()


def user_detail(request, uid=0):
    id = request.session.get('uid')
    if id:
        admin = Userdetail.objects.filter(user_uid=id).first()
        userdetail = Userdetail.objects.filter(user_uid=uid).first()
        print(userdetail)
        return render(request, 'niupih/user_detail.html', locals())
    return redirect(reverse('myadmin:login'), locals())


# 不需要, 不修改用户信息
def user_update(request, uid=0):
    id = request.session.get('uid')
    if id:
        admin = Userdetail.objects.filter(user_uid=id).first()
        return render(request, 'niupih/user_detail.html', locals())
    return redirect(reverse('myadmin:login'), locals())


def admin_add(request):
    id = request.session.get('uid')
    if id:
        admin = Userdetail.objects.filter(user_uid=id).first()
        if request.method == 'POST':
            # print(request.POST)
            form = AdminForm(request.POST)
            if form.is_valid():
                print(form.cleaned_data)
                admin_name = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                phone = form.cleaned_data.get('phone')
                print(admin_name, password, 11111)
                pic = 'admin.jpeg'
                admin = User.objects.create_user(username=admin_name, password=password, phone=phone, type=1,)
                # login(request, admin)
                admin_detail = Userdetail.objects.get_or_create(user_uid=admin, pic=pic)
                # admin = User.objects.filter(username=request.POST.get('username')).first()
                # admin.pic = 'admin.jpeg'
                # print(admin.pic)
                # admin.save()
                return redirect(reverse('myadmin:admin_list'), locals())
                # return render(request, 'niupih/admin_add.html', locals())
            # return render(request, 'niupih/admin_add.html', locals())
        else:
            form = RegisterForm()
            return render(request, 'niupih/admin_add.html', locals())
        # if request.method == 'POST':
        #     admin_name = request.POST.get('username')
        #     password = request.POST.get('password')
        #     re_password = request.POST.get('confirm_password')
        #     admin = User.objects.create_user(a)
        #     email = request.POST.get('email')
        #     if User.objects.filter(username=admin_name).first():
        #         res = '该管理员已经存在'
        #         return redirect(reverse('myadmin:admin_add'), locals())
        #     if password != re_password:
        #         return HttpResponse('密码不一致')
        #     print(request.POST, 111111)
        #     admin = User()
        #     admin.username = admin_name
        #     admin.password = password
        #     admin.type = 1
        #     admin.is_active = 1
        #     admin.phone = None
            # print(admin.username, admin.password)
            # user.save()
            # admin = User(username=admin_name, password=password)
        return render(request, 'niupih/admin_add.html', locals())
    return redirect(reverse('myadmin:login'), locals())


def admin_list(request):
    id = request.session.get('uid')
    if id:
        admin = Userdetail.objects.filter(user_uid=id).first()
        # admin = User.objects.filter(type=1)
        userdetail = Userdetail.objects.filter(user_uid__type=1)
        user = User.objects.filter(type=1)
        for user in user:
            return render(request, 'niupih/user_list.html', locals())
    return redirect(reverse('myadmin:login'), locals())


def admin_detail(request, uid=0):
    id = request.session.get('uid')
    if id:
        admin = Userdetail.objects.filter(user_uid=uid).first()
        return render(request, 'niupih/admin_detail.html', locals())
    return redirect(reverse('myadmin:login'), locals())


def admin_update(request, uid=0):
    id = request.session.get('uid')
    if id:
        admin = Userdetail.objects.filter(user_uid=id).first()
        if request.method == 'POST':
            print(request.POST)
            admin.real_name = request.POST.get('real_name')
            admin.id_num = request.POST.get('id_num')
            admin.age = request.POST.get('age')
            admin.birthday = request.POST.get('birthday').replace('年', '-').replace('月', '-').replace('日', '')
            # admin.birthday = datetime.datetime.strptime(request.POST.get('birthday'), '%Y-%m-%d')
            admin.address = request.POST.get('address')
            admin.user_uid.phone = request.POST.get('phone')
            ad = request.POST.get('gender')
            if ad == '男':
                admin.gender = 1
            if ad == '女':
                admin.gender = 2
            print(admin.gender)
            admin.save()
        return render(request, 'niupih/admin_detail.html', locals())
    return redirect(reverse('myadmin:login'), locals())


def bus_list(request):
    id = request.session.get('uid')
    if id:
        admin = Userdetail.objects.filter(user_uid=id).first()
        bus_list = Bus.objects.all().order_by('-bid')
        paginator = Paginator(bus_list, 5)
        page = request.GET.get('page')
          # 从前端获取当前的页码数,默认为1
        page = request.GET.get('page', 1)
          # 把当前的页码数转换成整数类型
        currentPage = int(page)
        try:
            print(page)
            bus_list = paginator.page(page)  # 获取当前页码的记录
        except PageNotAnInteger:
            bus_list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
        except EmptyPage:
            bus_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
        return render(request, 'niupih/bus_list2.html', locals())
    return redirect(reverse('myadmin:login'), locals())


def bus_detail(request, bid):
    id = request.session.get('uid')
    if id:
        admin = Userdetail.objects.filter(user_uid=id).first()
        print(bid)
        bus = Bus.objects.filter(bid=bid).first()
        return render(request, 'niupih/bus_detail1.html', locals())
    return redirect(reverse('myadmin:login'), locals())


# 不用add,使用add2
def bus_add(request):
    id = request.session.get('uid')
    if id:
        admin = Userdetail.objects.filter(user_uid=id).first()
        if request.method == 'POST':
            print(request.POST, 222222)
            bus = Bus()
            bus.num = request.POST.get('num')
            bus.bus_num = request.POST.get('bus_num')
            bus.start_city = request.POST.get('start_city')
            bus.end_city = request.POST.get('end_city')
            bus.start_station = request.POST.get('start_station')
            bus.end_station = request.POST.get('end_station')
            # bus.start_time = (request.POST.get('start_time') + ' ' + request.POST.get('start_time1'))
            bus.start_time = (request.POST.get('start_time').replace('年', '-').replace('月', '-').replace('日', ''))
            bus.ticket = request.POST.get('ticket')
            bus.price = request.POST.get('price')
            bus.standby_ticket = request.POST.get('ticket')
            hours = request.POST.get('hours')
            res = datetime.datetime.strptime(bus.start_time, "%Y-%m-%d %H:%M")
            bus.end_time = res + datetime.timedelta(hours=int(hours))
            time = datetime.datetime.now()
            bus.save()
            print(bus.end_time, bus.start_time)
            return redirect(reverse('myadmin:bus_list'), locals())
            # form = BusForm(request.POST)
            # if form.is_valid():
            #     print(form.cleaned_data, 11111111)
            #     bus = Bus()
            #     bus.num = form.cleaned_data.get('num')
            #     bus.bus_num = form.cleaned_data.get('bus_num')
            #     bus.start_city = form.cleaned_data.get('start_city')
            #     bus.end_city = form.cleaned_data.get('end_city')
            #     bus.start_station = form.cleaned_data.get('start_station')
            #     bus.end_station = form.cleaned_data.get('end_station')
            #     bus.start_time = (form.cleaned_data.get('start_time') + ' ' + form.cleaned_data.get('start_time1'))
            #     bus.price = form.cleaned_data.get('price')
            #     bus.ticket = form.cleaned_data.get('ticket')
            #     bus.standby_ticket = form.cleaned_data.get('ticket')
            #     hours = form.cleaned_data.get('hours')
            #     res = datetime.datetime.strptime(bus.start_time, "%Y-%m-%d %H:%M")
            #     bus.end_time = res + datetime.timedelta(hours=int(hours))
            #     print(bus.start_time, bus.end_time, 1111111)
            #     return redirect(reverse('myadmin:bus_list'), locals())
            # return render(request, 'niupih/bus_add.html', locals())
        else:
            form=BusForm()
            time = datetime.datetime.now()
            return render(request, 'niupih/bus_add.html', locals())
    return redirect(reverse('myadmin:login'), locals())


def bus_add2(request):
    id = request.session.get('uid')
    if id:
        admin = Userdetail.objects.filter(user_uid=id).first()
        if request.method == 'POST':
            form = BusForm2(request.POST)
            if form.is_valid():
                print(form.cleaned_data, 11111111)
                bus = Bus()
                bus.num = form.cleaned_data.get('num')
                bus.bus_num = form.cleaned_data.get('bus_num')
                bus.start_city = form.cleaned_data.get('start_city')
                bus.end_city = form.cleaned_data.get('end_city')
                bus.start_station = form.cleaned_data.get('start_station')
                bus.end_station = form.cleaned_data.get('end_station')
                bus.start_time = (form.cleaned_data.get('start_time').replace('年', '-').replace('月', '-').replace('日', ''))
                bus.price = form.cleaned_data.get('price')
                bus.ticket = form.cleaned_data.get('ticket')
                bus.standby_ticket = form.cleaned_data.get('ticket')
                hours = form.cleaned_data.get('hour')
                res = datetime.datetime.strptime(bus.start_time, "%Y-%m-%d %H:%M")
                bus.end_time = res + datetime.timedelta(hours=int(hours))
                print(bus.start_time, bus.end_time, 1111111)
                bus.save()
                return redirect(reverse('myadmin:bus_list'), locals())
        else:
            form = BusForm()
            time = datetime.datetime.now()
            return render(request, 'niupih/bus_add.html', locals())
        time = datetime.datetime.now()
        return render(request, 'niupih/bus_add.html', locals())
    return redirect(reverse('myadmin:login'), locals())


def bus_delete(request, bid=0):
    id = request.session.get('uid')
    if id:

        admin = Userdetail.objects.filter(user_uid=id).first()
        if bid == 0:
            bus = Bus.objects.all().order_by('-bid')
            return render(request, 'niupih/bus_list3.html', locals())
        # time_obj2 = datetime.strptime(time_str2, "%Y-%m-%d %H:%M:%S")
        # time_obj3 = datetime.now()
        #
        # # print time_obj3 - time_obj1
        # print(time_obj3 - time_obj1).seconds / 60
        bus = Bus.objects.all().order_by('-bid')
        bus_de = Bus.objects.filter(bid=bid).first()
        # time1 = datetime.datetime.strptime(bus_de.start_time, "%Y-%m-%d %H:%M:%S")
        # time1 = bus_de.start_time
        # time2 = datetime.datetime.now().year
        # time2 = datetime.datetime.strftime(time1, "%Y-%m-%d %H:%M")
        # time3 = datetime.datetime.now()
        # time4 = datetime.datetime.strftime(time3, "%Y-%m-%d %H:%M")
        # time5 = datetime.datetime.strptime(time2, "%Y-%m-%d %H:%M")
        # time6 = datetime.datetime.strptime(time4, "%Y-%m-%d %H:%M")
        # print(type(time3 - time1))
        # time = time6 - time5
        # if time4 > time2:
        #     time = 1
        # else:
        #     time = 0
        # print(time)
        print(bus_de.num, bus_de.bid)
        bus_de.delete()
        return render(request, 'niupih/bus_list3.html', locals())
    return redirect(reverse('myadmin:login'), locals())


def bus_update(request, bid=0):
    id = request.session.get('uid')
    if id:
        admin = Userdetail.objects.filter(user_uid=id).first()
        bus = Bus.objects.filter(bid=bid).first()
        if request.method == 'POST':
            print(1111111111)
            form = BusForm2(request.POST)
            if form.is_valid():
                print(form.cleaned_data, 11111111)
                bus = Bus.objects.filter(bid=bid).first()
                bus.num = form.cleaned_data.get('num')
                bus.bus_num = form.cleaned_data.get('bus_num')
                bus.start_city = form.cleaned_data.get('start_city')
                bus.end_city = form.cleaned_data.get('end_city')
                bus.start_station = form.cleaned_data.get('start_station')
                bus.end_station = form.cleaned_data.get('end_station')
                bus.start_time = (form.cleaned_data.get('start_time').replace('年', '-').replace('月', '-').replace('日', ''))
                bus.price = form.cleaned_data.get('price')
                bus.ticket = form.cleaned_data.get('ticket')
                bus.standby_ticket = form.cleaned_data.get('ticket')
                bus.save()
                return redirect(reverse('myadmin:bus_list'), locals())
            else:
                form = BusForm2()
                time = datetime.datetime.now()
                return render(request, 'niupih/bus_detail2.html', locals())
            # return redirect(reverse('myadmin:bus_update'), locals())
        form = BusForm2()
        time = datetime.datetime.now()
        return render(request, 'niupih/bus_detail2.html', locals())
        # id = request.session.get('uid')
        # admin = Userdetail.objects.filter(user_uid=id).first()
        # print(bid)
        # bus = Bus.objects.filter(bid=bid).first()
        # if request.method == 'POST':
        #     print(request.POST)
        #     bus.start_time = request.POST.get('start_time').replace('年', '-').replace('月', '-').replace('日', '')
        #     bus.start_city = request.POST.get('start_city')
        #     bus.end_city = request.POST.get('end_city')
        #     bus.num = request.POST.get('num')
        #     bus.bus_num = request.POST.get('bus_num')
        #     bus.start_station = request.POST.get('start_station')
        #     bus.end_station = request.POST.get('end_station')
        #     bus.ticket = request.POST.get('ticket')
        #     bus.standby_ticket = request.POST.get('ticket')
        #     bus.price = request.POST.get('price')
        #     print(bus.standby_ticket, bus.start_time)
        #     bus.save()
        # return redirect(reverse('myadmin:bus_list'), locals())
    return redirect(reverse('myadmin:login'), locals())


def car_list(request):
    id = request.session.get('uid')
    if id:
        admin = Userdetail.objects.filter(user_uid=id).first()
        cars = Car.objects.all()
        return render(request, 'niupih/car_list.html', locals())
    return redirect(reverse('myadmin:login'), locals())


def car_detail(request, cid):
    id = request.session.get('uid')
    if id:
        admin = Userdetail.objects.filter(user_uid=id).first()
        car = Car.objects.filter(cid=cid).first()
        print(cid)
        return render(request, 'niupih/car_detail.html', locals())
    return redirect(reverse('myadmin:login'), locals())


def page_not_found(request):
    return render(request, '404.html')


def server_error(request):
    return render(request, '500.html')

