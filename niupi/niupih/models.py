from __future__ import unicode_literals
from django.db import models


class Bus(models.Model):
    bid = models.AutoField(primary_key=True)
    num = models.CharField(max_length=10)
    bus_num = models.CharField(unique=True, max_length=10)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    start_city = models.CharField(max_length=128)
    end_city = models.CharField(max_length=128)
    start_station = models.CharField(max_length=128)
    end_station = models.CharField(max_length=128)
    price = models.IntegerField()
    ticket = models.IntegerField()
    standby_ticket = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'bus'


class Car(models.Model):
    cid = models.AutoField(primary_key=True)
    car_type = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    start_city = models.CharField(max_length=128)
    end_city = models.CharField(max_length=128)
    price = models.IntegerField(blank=True, null=True)
    seats = models.IntegerField(blank=True, null=True)
    left_seats = models.IntegerField(blank=True, null=True)
    uid = models.ForeignKey('User', models.DO_NOTHING, db_column='uid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'car'


class List(models.Model):
    lid = models.AutoField(primary_key=True)
    num_list = models.CharField(max_length=128)
    status = models.IntegerField()
    list_time = models.DateTimeField()
    list = models.CharField(max_length=128)
    uid = models.ForeignKey('User', models.DO_NOTHING, db_column='uid')

    class Meta:
        managed = False
        db_table = 'list'


class User(models.Model):
    uid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=64)
    is_active = models.IntegerField()
    type = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user'


class Userdetail(models.Model):
    eid = models.AutoField(primary_key=True)
    is_vip = models.IntegerField()
    real_name = models.CharField(max_length=20, blank=True, null=True)
    id_num = models.IntegerField(unique=True, blank=True, null=True)
    birthday = models.DateTimeField(blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    pic = models.CharField(max_length=128, blank=True, null=True)
    gender = models.IntegerField(blank=True, null=True)
    car_num = models.CharField(unique=True, max_length=10, blank=True, null=True)
    uid = models.ForeignKey(User, models.DO_NOTHING, db_column='uid')

    class Meta:
        managed = False
        db_table = 'userdetail'
