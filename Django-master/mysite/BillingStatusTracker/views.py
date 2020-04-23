from django.shortcuts import render
import sys
# sys.path.append("..")
# Create your views here.
from django.shortcuts import render
from django.shortcuts import redirect
from SearchWo.models import Pegasus
from Login.models import Mydb
import django.contrib.auth
from BillingStatusTracker.models import Billing
from django.contrib.auth import authenticate, login, logout
from datetime import datetime


B=''
username=''
params={}
searchvalue=''

def BillingTracker(request):
    global params, searchvalue

    if request.method == 'POST':
        if request.method == 'POST':
            if request.POST.get('Logout'):
                logout(request)
                return redirect('/')
        Button_Criteria = request.POST.get('Search', 'Bill_Button')
        if Button_Criteria == 'Search':

            searchcriteria = request.POST.get('Criteria', 'ProjectId')
            searchvalue = request.POST.get('text')
            global B
            if searchcriteria != 'ProjectId':
                B = Pegasus.objects.filter(ProjectId=searchvalue, SvcOrderStatus='CLOSED',
                                           WorkOrderStatus='CLOSED').distinct()
            else:
                B = Pegasus.objects.filter(SvcNo=searchvalue, SvcOrderStatus='CLOSED', WorkOrderStatus='CLOSED').distinct()

            global username
            username = request.user.get_username()

            # print(type(B))

            params = {'data': B, 'Username': username}
            # render(request, '')
            params['msg'] = ''
            return render(request, 'BillingTracker.html', params)
        else:
            print("Alert!!!!")
            # bt = Billing.objects.all()
            print(Billing.objects.filter(svcno=searchvalue).count())
            if Billing.objects.filter(svcno=searchvalue).count()==0:
                params['msg'] = "Bill generated successfully !!"
                params['style'] = "alert-success"

                for ins in B:
                    # print(ins.id)
                    # Billing.objects.create()  # , Billed_status="Billed", Billed_by=username,Billed_date=datetime)


                    bill = Billing(id=ins.id, projectid=ins.ProjectId,
                                   svcno=ins.SvcNo, svcorderstatus=ins.SvcOrderStatus, workorder=ins.WorkOrder,
                                   workorderstatus=ins.WorkOrderStatus, crd=ins.CRD, speed=ins.Speed,
                                   updates=ins.Updates, Billed_status="Billed", Billed_by=username, Billed_date=datetime.now())
                    bill.save()
            else:
                params['style'] = "alert-warning"
                params['msg'] = "Already billed, you cannot billed on the same circuit ID again!"
            return render(request, 'BillingTracker.html', params)

    else:
        # params['msg']=''
        username = request.user.get_username()
        return render(request, 'BillingTracker.html', {'msg':'', 'Username': username})
