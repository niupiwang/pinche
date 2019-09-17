from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View

from App.models import Bus


def index(request):
    if request.method == 'POST':
        start_city = request.POST.get('from')
        end_city = request.POST.get('go')
        buses = Bus.objects.filter(start_city=start_city,end_city=end_city).order_by('start_time')
        if start_city and end_city:

            return render(request, 'app/select.html',locals())
    return render(request,'app/index.html')

def select(request):
    if request.method == 'POST':
        start_city = request.POST.get('from')
        end_city = request.POST.get('go')
        print(start_city)
    # cars = Bus.objects.filter(start_city=start_city,end_city=end_city)
    return render(request,'app/select.html')

def buy(request):
    return render(request,'app/buy.html')

def userinfo(request):
    return render(request,'app/userinfo.html')




class UserView(View):
    def get(self,request):
        pass
    def post(self,request):
        pass


