from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import *
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

from .models import Mydb
# Create your views here.

def index(request):
    context={}
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['pass']
        user=authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            #return render(request, "Home.html")
            return redirect('Home')
        else:
            context["error"]=1
            return render(request, "index.html",context)
    else:
        return render(request,"Index.html")



