from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import redirect
from .models import Pegasus

def SearchWo(request):
    #params = Pegasus.objects.all()
    if request.method == 'POST':
        searchcriteria = request.POST.get('Criteria', 'ProjectId')
        searchvalue = request.POST.get('text')
        if searchcriteria == 'ProjectId':
            P = Pegasus.objects.filter(ProjectId=searchvalue)
        else:
            P = Pegasus.objects.filter(SvcNo=searchvalue)
        params = {'data' : P}
        list_teams = request.POST.getlist('team')
        return render(request,'SearchWo.html',params)
    else:
        return render(request,'SearchWo.html')

