from django.shortcuts import render
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required




def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@login_required(login_url='/')
def Home(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')
    else:
        xdata = ["Apple", "Apricot", "Avocado", "Banana", "Boysenberries", "Blueberries", "Dates", "Grapefruit", "Kiwi",
                 "Lemon"]
        ydata = [52, 48, 160, 94, 75, 71, 490, 82, 46, 17]

        extra_serie = {"tooltip": {"y_start": "", "y_end": " cal"}}
        chartdata = {'x': xdata, 'y1': ydata, 'extra1': extra_serie}
        charttype = "pieChart"

        data = {
            'charttype': charttype,
            'chartdata': chartdata,}
        return render(request,'Home.html',{'data':data})



