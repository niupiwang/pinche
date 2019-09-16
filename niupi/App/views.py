from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html')


def userinfo(request):
    return render(request,'userinfo.html')