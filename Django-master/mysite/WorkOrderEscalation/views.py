from django.shortcuts import render
from django.http import *
from .models import WorkOrderEscalation
from django.shortcuts import redirect
from django.template.loader import get_template

def WorkOrderEscalate(request):

   params=WorkOrderEscalation.objects.all()
   if request.method == 'POST':
      list_teams=request.POST.getlist('team')
      return redirect('/Home/WorkOrderEscalation/OutlookEscalate',{'dict_teams':list_teams})
   else:
      return render(request,"WorkOrderEscalation.html",{'params':params})

