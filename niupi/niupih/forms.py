import re

from django import forms
from django.core.exceptions import ValidationError

from App.models import User


def check_password(password):
    if re.search(r'\d+', password):
        return password
    raise ValidationError('密码强度不满足要求')


def check_phone(phone):
    if re.match(r'^1[3|5|7|8]\d{9}$',phone):
        return phone
    raise ValidationError('请输入正确的手机号')


class AdminForm(forms.Form):
    username = forms.CharField(label='用户名',
                               max_length=12,
                               min_length=3,
                               error_messages={
                                   'max_length': '用户名最大长度是12字符',
                                   'min_length': '用户名长度不能小于3字符',
                                   'required': '用户名必须输入'
                               })

    password = forms.CharField(label='密码',
                               max_length=12,
                               min_length=3,
                               widget=forms.PasswordInput(attrs={
                                   'placehold': '请输入密码',
                                   'class': 'hahaha'
                               }),
                               validators=[check_password],
                               error_messages={
                                   'max_length': '密码最大长度是128字符',
                                   'min_length': '密码长度不能小于6个字符',
                                   'required': '用户名必须输入'
                               })

    repassword = forms.CharField(label='确认密码',
                                 max_length=12,
                                 min_length=3,
                                 widget=forms.PasswordInput(attrs={
                                     'placehold': '请输入确认密码',
                                     'class': '994'
                                 }),
                                 validators=[check_password],
                                 error_messages={
                                     'max_length': '密码最大长度是128字符',
                                     'min_length': '密码长度不能小于6个字符',
                                     'required': '确认密码必须输入'
                                 })

    phone = forms.CharField(label='手机号',
                               widget=forms.PasswordInput(attrs={
                                   'placehold': '请输入手机号',
                                   'class': 'hahahaya'
                               }),
                               validators=[check_phone],
                               error_messages={
                                   'required': '手机号必须输入'
                               })

    def clean_username(self):
        res = User.objects.filter(username=self.cleaned_data.get('username'))
        if res:
            raise ValidationError('用户名已存在')
        return self.cleaned_data.get('username')

    def clean(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('repassword')
        if password1 != password2:
            raise ValidationError({'repassword': '两次密码不一致'})
        return self.cleaned_data


class BusForm(forms.Form):
    num = forms.CharField(max_length=20, error_messages={
        'required': '必须输入'
    })
    bus_num = forms.CharField(max_length=200, error_messages={
        'required': '必须输入'
    })
    start_station = forms.CharField(max_length=200, error_messages={
        'required': '必须输入'
    })
    end_station = forms.CharField(max_length=200, error_messages={
        'required': '必须输入'
    })
    start_city = forms.CharField(max_length=200, error_messages={
        'required': '必须输入'
    })
    end_city = forms.CharField(max_length=200, error_messages={
        'required': '必须输入'
    })
    start_time = forms.DateTimeField(error_messages={
        'required': '必须输入'
    })
    start_time1 = forms.DateTimeField(error_messages={
        'required': '必须输入'
    })
    price = forms.CharField(max_length=200, error_messages={
        'required': '必须输入'
    })
    ticket = forms.CharField(max_length=200, error_messages={
        'required': '必须输入'
    })
    standby_ticket = forms.CharField(max_length=200, error_messages={
        'required': '必须输入'
    })
    hours = forms.IntegerField(error_messages={
        'required': '必须输入'
    })


class BusForm2(forms.Form):
    num = forms.CharField(max_length=10, error_messages={
        'max_length': '最大长度为10位',
        'required': '必须输入',
    })
    bus_num = forms.CharField(max_length=10, error_messages={
        'max_length': '最大长度为10位',
        'required': '必须输入',
    })
    start_city = forms.CharField(max_length=200, error_messages={
        'required': '必须输入'
    })
    end_city = forms.CharField(max_length=200, error_messages={
        'required': '必须输入'
    })
    start_station = forms.CharField(max_length=200, error_messages={
        'required': '必须输入'
    })
    end_station = forms.CharField(max_length=200, error_messages={
        'required': '必须输入'
    })
    start_time = forms.CharField(error_messages={
        'required': '必须输入'
    })
    # hours = forms.CharField(error_messages={
    #     'required': '必须输入'
    # })
    ticket = forms.CharField(error_messages={
        'required': '必须输入'
    })
    price = forms.CharField(error_messages={
        'required': '必须输入'
    })
