from datetime import datetime

from django.contrib.auth import logout
from django.shortcuts import render
# Create your views here.
from django import forms
from django.shortcuts import render
import sys
from django.shortcuts import render
from django.shortcuts import redirect
from SearchWo.models import Pegasus
from django.contrib.auth.decorators import login_required

new_dict = {}
texta = ''
O = Pegasus.objects.none()
a = ''
list_result = []
c = ''
params = {}
list_upd = []
Flag = 0

@login_required(login_url='/')
def StatusTracker(request):
    username = request.user.get_username()
    global texta, O, a, new_dict, list_result, c, params, list_upd, Flag
    if request.POST.get('Logout'):
        logout(request)
        print("Logout")
        return redirect('/')

    if request.method == 'POST':

        SubmitCriteria = request.POST.get('Search', 'Export')

        if SubmitCriteria == "Search":
            searchcriteria = request.POST.get('Criteria', 'ProjectId')
            searchvalue = request.POST.get('text')
            SubmitComments = request.POST.get('Comments', 'UpdateComments')

            if searchcriteria == 'ProjectId':
                O = Pegasus.objects.filter(ProjectId=searchvalue).distinct()
                C = Pegasus.objects.filter(ProjectId=searchvalue).count()
            else:
                O = Pegasus.objects.filter(SvcNo=searchvalue).distinct()
                C = Pegasus.objects.filter(SvcNo=searchvalue).count()

            if C == 0:
                params['style'] = "alert-danger"
                params['msg'] = searchcriteria + " " + searchvalue + " not found"
            elif O.count() == 0:
                params['style'] = "alert-info"
                params['msg'] = searchcriteria + " " + searchvalue + " is not Open"
            else:
                params['msg'] = ''
            result = O.values('id')  # return ValuesQuerySet object
            list_result = [entry for entry in result]  # converts ValuesQuerySet into Python list
            upd = O.values('Updates')
            list_upd = [upd_entry for upd_entry in upd]
            res = [sub['Updates'] for sub in list_upd]

            if len(res) == 0 or res[0] == '':
                res = '-----'
                list_upd = res
            else:
                list_upd = res

            myDict = {}
            for Dict in list_result:
                for key in Dict:
                    new_dict[key] = Dict[key]
            from collections import ChainMap
            myDict = dict(ChainMap(*list_result))
            old_dict = dict((key, d[key]) for d in list_result for key in d)
            adict = {k: v for elem in list_result for (k, v) in elem.items()}

            a = O.filter(ProjectId=searchvalue)
            params['data'] = O
            params['Username'] = username
            params['Flag'] = 0
            return render(request, 'StatusTracker.html', params)

        if SubmitCriteria == 'Export':
            import xlwt
            from django.http import HttpResponse
            # from django.contrib.auth.models import User
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="List of open work orders.xls"'

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Users Data')  # this will make a sheet named Users Data
            row_num = 0

            font_style = xlwt.XFStyle()
            font_style.font.bold = True

            columns = ['ProjectId', 'SvcNo', 'SvcOrderStatus', 'WorkOrder', 'WorkOrderStatus', 'CRD', 'Speed',
                       'Updates']

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()

            rows = O.values_list('ProjectId', 'SvcNo', 'SvcOrderStatus', 'WorkOrder',
                                 'WorkOrderStatus',
                                 'CRD', 'Speed', 'Updates')
            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)

            wb.save(response)

            return response

    elif request.method == 'GET':
        print("Inside elseif Flag value is" + str(Flag))
        area_req = dict(request.GET)
        print(area_req)
        print("area: ",area_req.get('area'))
        P = Pegasus.objects.all()
        if area_req.get('area') == None:
            Flag = 1
            P = Pegasus.objects.all()
            return render(request, 'StatusTracker.html',
                          {'msg': '', 'Username': username, 'Flag': Flag, 'DefaultDData': P})

        for ren in range(len(list_result)):
            print(list_result[ren])
            my_dict = {}
            my_dict = list_result[ren]

            # print('30: Value of area_req[area]: ', area_req['area'][ren])
            #print(list_result[ren])

            textb = area_req['area'][ren]
            if textb != "":
            #print('31: Value of list_upd[ren]: ', list_upd[ren])
                old_text = list_upd[ren]
                #print("32: value of old_text: ", old_text)
                #print("33: type(old_text) : ", type(old_text))
                # now = datetime.now()
                dt = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
                textb = str(dt) + " : " + textb + '\n' + '-------------------------' + '\n' + str(old_text)
                # print("34: Value of textb or final comments are: ", textb)
                c = O.filter(id=my_dict.get("id"))
                c.update(Updates=textb)
                # c.save()
                Flag = 1
            params = {'DefaultDData': P, 'Username': username, 'msg': '', 'Flag': Flag}

        context = params
        return render(request, 'StatusTracker.html', context)
    else:

        D = {'msg': '', 'Username': username, 'F': Flag, 'DefaultData': P}

        return render(request, 'StatusTracker.html', D)
