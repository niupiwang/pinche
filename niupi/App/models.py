from datetime import datetime
from django.db import models


# Create your models here.


#1用户表
class User(models.Model):
    # uid = models.AutoField(primary_key=True, )
    username = models.CharField(max_length=100, verbose_name='用户名')
    password = models.CharField(max_length=128, verbose_name='密码')
    real_name = models.CharField(null=True, max_length=20, verbose_name='真实姓名')
    id_num = models.IntegerField(null=True, unique=True, max_length=18, verbose_name='身份证号')
    birthday = models.DateTimeField(null=True, verbose_name='生日')
    address = models.CharField(null=True, max_length=200, verbose_name='地址')
    age = models.IntegerField(null=True, verbose_name='年龄')
    g_type = ((0, '保密'), (1, '男'), (2, '女'))
    gender = models.IntegerField(null=True, default=0, choices=g_type, verbose_name='性别')

    class Meta:
        db_table = 'user'
        verbose_name_plural = '用户表'


#2汽车信息表
class Bus(models.Model):
    # num = models.CharField(max_length=10, verbose_name='列车编号')
    # b_type = ((0, '经济型'), (1, '豪华舒适型'), (2, '临时加车'))
    # bus_type = models.IntegerField(default=0, choices=b_type, verbose_name='汽车类型')
    driver = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='司机')
    car_type = models.CharField(max_length=100, verbose_name='车型描述（品牌，名称，座位数）')
    plate_num = models.CharField(max_length=10, unique=True, verbose_name='车牌号码')
    start_time = models.DateTimeField(verbose_name='起始时间')
    end_time = models.DateTimeField(verbose_name='到达时间')
    time = models.DateTimeField(verbose_name='耗时')
    city_list = ((0, '未选择'), (1, '石家庄'), (2, '秦皇岛'))
    start_city = models.IntegerField(default=0, choices=city_list, verbose_name='起始城市')
    end_city = models.IntegerField(default=0, choices=city_list, verbose_name='到达城市')
    # station_list = ((0, '未选择'), (1, '石家庄汽车总站'), (2, '秦皇岛长途客运站'))
    # start_station = models.IntegerField(null=True, default=0, choices=station_list, verbose_name='始发车站')
    # end_station = models.IntegerField(null=True, default=0, choices=station_list, verbose_name='到达车站')
    price = models.IntegerField(null=True, verbose_name='价格')
    ticket = models.IntegerField(null=True, verbose_name='总票数')
    standby_ticket = models.IntegerField(null=True, verbose_name='余票')

    class Meta:
        db_table = 'ticket'
        verbose_name_plural = '车次表'


#3我的订单表
class MyList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    driver = models.ForeignKey(User, on_delete=models.CASCADE, )
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE,)
    # start_time = models.DateTimeField(default=datetime.now(), null=True)
    s_list = ((0, '未完成'), (1, '已取消'), (2, '已完成'))
    status = models.IntegerField(default=0, choices=s_list, verbose_name='订单状态')
    list_time = models.DateTimeField(default=datetime.now, verbose_name='下单时间')
    # list_type = models.IntegerField(default=0, choices=((0, '我要订车'), (1, '我要拉活')), )

    class Meta:
        db_table = 'my_list'
        verbose_name_plural = '订单表'


