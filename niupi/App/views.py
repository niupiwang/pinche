from django.shortcuts import render

# Create your views here.
from django.views import View


def index(request):
    return render(request,'index.html')


def userinfo(request):
    return render(request,'userinfo.html')


class UserView(View):
    pass