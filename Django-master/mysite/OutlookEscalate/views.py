from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import *
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

def OutlookEsc(request):
    return render(request,'OutlookEsc.html')
