from django import forms


class AdminForm(forms.Form):
    admin = forms.CharField(max_length=20, min_length=6, error_messages={
        'max_length': '最大长度不超过20位',
        'min_length': '最小长度不少于6位'
    })
    password = forms.CharField(max_length=20)
