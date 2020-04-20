from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import *
from django.shortcuts import redirect
from WorkOrderEscalation.models import WorkOrderEscalation

def ClosureApproval(request):
    dict_teams={}
    params = WorkOrderEscalation.objects.all()
    if request.method == 'POST':
        list_teams = request.POST.getlist('team')
        dict_teams['Teams']=list_teams
        return render(request,"OutlookEsc.html",dict_teams)
    else:
      return render(request,'ClosureApproval.html',{'params':params})
