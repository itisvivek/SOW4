from django.shortcuts import render
from django.http import *
from .models import WorkOrderEscalation
from django.shortcuts import redirect
from django.template.loader import get_template

def WorkOrderEscalate(request):
   dict_teams={}
   params=WorkOrderEscalation.objects.all()
   if request.method == 'POST':
      list_teams=request.POST.getlist('team')
      dict_teams['Teams']=list_teams
      print(list_teams)
      return render(request,"OutlookEsc.html",dict_teams)
   else:
      return render(request,"WorkOrderEscalation.html",{'params':params})

