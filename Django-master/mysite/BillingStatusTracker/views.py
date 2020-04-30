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
from django.contrib.auth.decorators import login_required

B=''
username=''
params={}
searchvalue=''

@login_required(login_url='/')
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
                C= Pegasus.objects.filter(ProjectId=searchvalue).count()
            else:
                B = Pegasus.objects.filter(SvcNo=searchvalue, SvcOrderStatus='CLOSED', WorkOrderStatus='CLOSED').distinct()
                C = Pegasus.objects.filter(SvcNo=searchvalue).count()
            global username


            if C == 0:
                params['style'] = "alert-danger"
                params['msg'] = "Circuit " + searchvalue + " not found"
            elif B.count() == 0:
                params['style'] = "alert-info"
                params['msg'] = "Circuit " + searchvalue + " is not closed"
            else:
                params['msg'] = ''

            username = request.user.get_username()
            params['data']=B
            params['Username']= username
            # render(request, '')

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
