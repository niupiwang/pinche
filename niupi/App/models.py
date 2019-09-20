from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


#1用户表
class User(AbstractUser):
    uid = models.AutoField(primary_key=True)
    #username = models.CharField(max_length=100, verbose_name='用户名')
    #password = models.CharField(max_length=128, verbose_name='密码')
    phone = models.CharField(max_length=64,verbose_name='手机号')
    is_active = models.IntegerField(default=1) # 1代表激活 0代表锁定
    type = models.IntegerField(default=0) # 0为普通用户 1为司机 2为管理员用户
    portrait = models.CharField(max_length=196,verbose_name='手机号')
    friends = models.CharField(max_length=128,null=True)

    class Meta:
        db_table = 'user'
        verbose_name_plural = '用户表'

#2用户详情
class Userdetail(models.Model):
    eid = models.AutoField(primary_key=True)
    is_vip = models.IntegerField(default=0) # 0否 1是
    real_name = models.CharField(null=True, max_length=20, verbose_name='真实姓名')
    id_num = models.CharField(null=True, unique=True,max_length=254, verbose_name='身份证号')
    birthday = models.DateTimeField(null=True, verbose_name='生日')
    address = models.CharField(null=True, max_length=200, verbose_name='地址')
    age = models.IntegerField(null=True, verbose_name='年龄')
    pic = models.CharField(null=True,max_length=128) # 头像
    g_type = ((0, '保密'), (1, '男'), (2, '女'))
    gender = models.IntegerField(null=True, default=0, choices=g_type, verbose_name='性别')
    car_num = models.CharField(max_length=10, unique=True, verbose_name='车牌号码',null=True)
    user_uid = models.ForeignKey(User,models.DO_NOTHING,db_column='uid',blank=True,null=False)
    class Meta:
        db_table = 'userdetail'
        verbose_name_plural = '用户详情'



#3汽车信息表
class Bus(models.Model):
    bid = models.AutoField(primary_key=True)
    num = models.CharField(max_length=128, verbose_name='列车编号')
    bus_num = models.CharField(max_length=10, unique=True, verbose_name='车牌号码')
    start_time = models.DateTimeField(verbose_name='起始时间')
    end_time = models.DateTimeField(verbose_name='到达时间')
    start_city = models.CharField(max_length=128, verbose_name='起始城市')
    end_city = models.CharField(max_length=128, verbose_name='到达城市')
    start_station = models.CharField(max_length=128, verbose_name='始发车站')
    end_station = models.CharField(max_length=128, verbose_name='到达车站')
    price = models.IntegerField(verbose_name='价格')
    ticket = models.IntegerField(verbose_name='总票数')
    standby_ticket = models.IntegerField(verbose_name='余票')
    class Meta:
        db_table = 'bus'
        verbose_name_plural = '车次表'


#4汽车信息表
class Car(models.Model):
    cid = models.AutoField(primary_key=True)
    car_num = models.IntegerField(unique=True, verbose_name='车牌号码',null=True)
    car_type = models.CharField(max_length=100, verbose_name='车型描述（品牌，名称，座位数）')
    start_time = models.DateTimeField(verbose_name='出发时间')
    start_city = models.CharField(max_length=128, verbose_name='起始城市')
    end_city = models.CharField(max_length=128, verbose_name='到达城市')
    price = models.IntegerField(null=True, verbose_name='价格')
    seats = models.IntegerField(null=True, verbose_name='总座位数')
    left_seats = models.IntegerField(null=True, verbose_name='剩余座位')
    car_uid = models.ForeignKey(User, models.DO_NOTHING, db_column='uid', blank=True, null=True)

    class Meta:
        db_table = 'car'
        verbose_name_plural = '拼车表'


#5我的订单表
class List(models.Model):
    lid = models.AutoField(primary_key=True)
    # 订单号
    num_list = models.CharField(max_length=128)
    # 订单金额
    price_list = models.IntegerField(null=True)
    s_list = ((0, '未完成'), (1, '已取消'), (2, '已完成'))
    status = models.IntegerField(default=0, choices=s_list, verbose_name='订单状态')
    list_time = models.DateTimeField(default=datetime.now, verbose_name='下单时间')
    list_uid = models.ForeignKey(User, models.DO_NOTHING, db_column='uid', blank=True, null=False)
    list = models.CharField(max_length=128, null=False) # 订单的乘客列表
    traffic = models.ForeignKey(Bus, models.DO_NOTHING, db_column='bid', blank=True, null=False)

    class Meta:
        db_table = 'list'
        verbose_name_plural = '订单表'


# 消息
class News(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128,null=True)
    content = models.CharField(max_length=128,null=True)
    set_time = models.DateTimeField(null=True)
    from_user = models.IntegerField(null=True)
    belong_user = models.ForeignKey(User, models.DO_NOTHING, db_column='uid', blank=True, null=False)

    class Meta:
        db_table = 'news'


