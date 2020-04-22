from django.shortcuts import render

# Create your views here.
def OpenCircuits(request):
    return render(request,'OpenCircuitManagement.html')
