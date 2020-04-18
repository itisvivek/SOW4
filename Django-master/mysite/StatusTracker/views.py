from django.shortcuts import render
import sys
#sys.path.append("..")
# Creaste your views here.
from django.shortcuts import render
from django.shortcuts import redirect

from SearchWo.models import Pegasus

def StatusTracker(request):
    P = Pegasus.objects.all()
    params = {'data': P}
    return render(request,'StatusTracker.html',params)


