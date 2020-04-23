from datetime import datetime

from django.contrib.auth import logout
from django.shortcuts import render
# Create your views here.
from django import forms
from django.shortcuts import render
import sys
# sys.path.append("..")
# Create your views here.
from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.
#from BillingStatusTracker.views import username
from SearchWo.models import Pegasus

new_dict={}
texta=''
O=Pegasus.objects.none()
a=''
list_result=[]
c=''
params={}

def OpenCircuits(request):
    username = request.user.get_username()
    global texta
    global O
    global a
    global new_dict
    global list_result
    global c
    global params
    if request.POST.get('Logout'):
        logout(request)
        return redirect('/')

    print(request.GET)
    #username = request.user.get_username()
    if request.method == 'POST':
        SubmitCriteria = request.POST.get('Search', 'Search1')
        print("Inside first if_post method")
        # if(Updatebut == 'Sub'):
        #     print(request.POST.get('area'))
        if SubmitCriteria == "Search":
            searchcriteria = request.POST.get('Criteria', 'ProjectId')
            searchvalue = request.POST.get('text')
            SubmitComments = request.POST.get('Comments', 'UpdateComments')
            if searchcriteria == 'ProjectId':
                O = Pegasus.objects.filter(ProjectId=searchvalue, SvcOrderStatus='OPEN',
                                           WorkOrderStatus='OPEN').distinct()
            else:
                O = Pegasus.objects.filter(SvcNo=searchvalue, SvcOrderStatus='OPEN',
                                           WorkOrderStatus='OPEN').distinct()

            print('ID of current line: ',O.values('id'))
            result = O.values('id')  # return ValuesQuerySet object

            list_result = [entry for entry in result]  # converts ValuesQuerySet into Python list

            print('Value of list_result: ',list_result)
            print('Value of count of list_result inside POST: ', len(list_result))
            myDict = {}
            for Dict in list_result:
                for key in Dict:
                    new_dict[key] = Dict[key]
            from collections import ChainMap
            myDict = dict(ChainMap(*list_result))
            # print(new_dict)
            old_dict = dict((key,d[key]) for d in list_result for key in d)
            adict = {k: v for elem in list_result for (k, v) in elem.items()}
            print('Value of adict inside POST: ',adict)
            print('Value of old_dict inside POST: ',old_dict)
            print('Value of new_dict inside POST: ', new_dict)
            print('Value of myDict inside POST: ', myDict)

            print('Value of GET inside POST: ', request.GET)
            print('Value of POST inside POST: ', request.POST)

            a = O.filter(ProjectId=searchvalue)
            print('Value of a in POST: ', a)
            print('Value of texta inside POST: ', texta)
            # UpdateValue=forms.CharField(widget=forms.Textarea(), required=False) #forms.Textarea()
            params = {'data': O, 'Username': username}
            return render(request, 'OpenCircuitManagement.html', params)

        if SubmitCriteria == 'Search1':
            import xlwt
            from django.http import HttpResponse
            from django.contrib.auth.models import User
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="List of open work orders.xls"'

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Users Data')  # this will make a sheet named Users Data

            # Sheet header, first row
            row_num = 0

            font_style = xlwt.XFStyle()
            font_style.font.bold = True

            columns = ['ProjectId', 'SvcNo', 'SvcOrderStatus', 'WorkOrder', 'WorkOrderStatus', 'CRD', 'Speed',
                       'Updates']

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()

            rows = Pegasus.objects.all().values_list('ProjectId', 'SvcNo', 'SvcOrderStatus', 'WorkOrder',
                                                        'WorkOrderStatus',
                                                     'CRD', 'Speed', 'Updates')
            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)

            wb.save(response)

            return response

    else:

        print('Value of GET inside GET: ', request.GET)
        # print('Value of POST inside GET: ', request.POST)
        area_req=dict(request.GET)
        print('Value of area_req from request.GET: ', area_req)
        print('type(area_req): ', type(area_req))
        print('area_req[area]: ', area_req.get('area'))


        print("Value of list_result inside GET: ", list_result)
        for ren in range(len(list_result)):
            print('Value of list_result: ', list_result[ren])
            my_dict={}
            my_dict=list_result[ren]
            print('Value of area_req[area]: ', area_req['area'][ren])
            textb=area_req['area'][ren]
            # now = datetime.now()
            dt = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            textb= str(dt) + " : " + textb
            c = O.filter(id=my_dict.get("id"))
            c.update(Updates=textb)
            # c.save()
            params = {'data': c, 'Username': username}

        context=params

    return render(request, 'OpenCircuitManagement.html', context)