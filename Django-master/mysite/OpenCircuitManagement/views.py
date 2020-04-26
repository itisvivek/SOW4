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
# from BillingStatusTracker.views import username
from SearchWo.models import Pegasus

new_dict = {}
texta = ''
O = Pegasus.objects.none()
a = ''
list_result = []
c = ''
params = {}
list_upd = []

def OpenCircuits(request):
    username = request.user.get_username()
    global texta, O, a, new_dict,list_result, c, params, list_upd

    if request.POST.get('Logout'):
        logout(request)
        return redirect('/')

    if request.method == 'POST':
        SubmitCriteria = request.POST.get('Search', 'Export')

        if SubmitCriteria == "Search":
            searchcriteria = request.POST.get('Criteria', 'ProjectId')
            searchvalue = request.POST.get('text')
            SubmitComments = request.POST.get('Comments', 'UpdateComments')

            if searchcriteria == 'ProjectId':
                O = Pegasus.objects.filter(ProjectId=searchvalue, SvcOrderStatus='OPEN',WorkOrderStatus='OPEN').distinct()
                C = Pegasus.objects.filter(ProjectId=searchvalue).count()
            else:
                O = Pegasus.objects.filter(SvcNo=searchvalue, SvcOrderStatus='OPEN', WorkOrderStatus='OPEN').distinct()
                C = Pegasus.objects.filter(SvcNo=searchvalue).count()

            if C == 0:
                params['style'] = "alert-danger"
                params['msg'] = searchcriteria + " " + searchvalue + " not found"
            elif O.count() == 0:
                params['style'] = "alert-info"
                params['msg'] = searchcriteria + " " + searchvalue + " is not Open"
            else:
                params['msg'] = ''
            #print('3: ID of current line: ', O.values('id'))
            result = O.values('id')  # return ValuesQuerySet object

            list_result = [entry for entry in result]  # converts ValuesQuerySet into Python list

            upd = O.values('Updates')
            #print("4: Updated value of Updates : ", upd)
            #print("5: type(upd) : ", type(upd))

            list_upd = [upd_entry for upd_entry in upd]
            #print("6: Updated list of value of Updates : ", list_upd)
            #print("7: type(upd) : ", type(list_upd))
            #print("8: Count of elements in list_upd: ", len(list_upd))

            res = [sub['Updates'] for sub in list_upd]

            #print("9: Value of res in POST: ", res)
            #print("10: Count of res in POST: ", len(res))

            if len(res) == 0 or res[0] == '':
                #print("11: List is empty")
                res = '-----'
                list_upd = res
            else:
                #print('12: List contains some elements')
                list_upd = res


            # print('13: Value of list_result: ', list_result)
            # print('14: Value of count of list_result inside POST: ', len(list_result))
            myDict = {}
            for Dict in list_result:
                for key in Dict:
                    new_dict[key] = Dict[key]
            from collections import ChainMap
            myDict = dict(ChainMap(*list_result))
            # print(new_dict)
            old_dict = dict((key, d[key]) for d in list_result for key in d)
            adict = {k: v for elem in list_result for (k, v) in elem.items()}
            # print('15: Value of adict inside POST: ', adict)
            # print('16: Value of old_dict inside POST: ', old_dict)
            # print('17: Value of new_dict inside POST: ', new_dict)
            # print('18: Value of myDict inside POST: ', myDict)
            #
            # print('19: Value of GET inside POST: ', request.GET)
            # print('20: Value of POST inside POST: ', request.POST)

            a = O.filter(ProjectId=searchvalue)
            # print('21: Value of a in POST: ', a)
            # print('22: Value of texta inside POST: ', texta)
            # UpdateValue=forms.CharField(widget=forms.Textarea(), required=False) #forms.Textarea()
            params['data'] = O
            params['Username'] = username
            return render(request, 'OpenCircuitManagement.html', params)

        if SubmitCriteria == 'Export':
            import xlwt
            from django.http import HttpResponse
            # from django.contrib.auth.models import User
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="List of open work orders.xls"'

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Users Data')  # this will make a sheet named Users Data

            # if searchcriteria == 'ProjectId':
            #     O = Pegasus.objects.filter(ProjectId=searchvalue, SvcOrderStatus='OPEN',
            #                                WorkOrderStatus='OPEN').distinct()
            # else:
            #     O = Pegasus.objects.filter(SvcNo=searchvalue, SvcOrderStatus='OPEN',
            #                                WorkOrderStatus='OPEN').distinct()
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

        # print('23: Value of GET inside GET: ', request.GET)
        # print('Value of POST inside GET: ', request.POST)
        area_req = dict(request.GET)
        # print('24: Value of area_req from request.GET: ', area_req)
        # print('25: type(area_req): ', type(area_req))
        # print('26: area_req[area]: ', area_req.get('area'))

        if area_req.get('area') == None:
            return render(request, 'OpenCircuitManagement.html', {'msg':'', 'Username': username})

        # print("27: Value of list_result inside GET: ", list_result)
        # print("28: Value of list_upd inside GET: ", list_upd)

        for ren in range(len(list_result)):
            # print('29: Value of list_result: ', list_result[ren])
            my_dict = {}
            my_dict = list_result[ren]
            # print('30: Value of area_req[area]: ', area_req['area'][ren])
            textb = area_req['area'][ren]
            # print('31: Value of list_upd[ren]: ', list_upd[ren])
            old_text = list_upd[ren]
            # print("32: value of old_text: ", old_text)
            # print("33: type(old_text) : ", type(old_text))
            # now = datetime.now()
            dt = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            textb =  str(dt) + " : " + textb + '\n' + '-------------------------'+ '\n' + str(old_text)
            # print("34: Value of textb or final comments are: ", textb)
            c = O.filter(id=my_dict.get("id"))
            c.update(Updates=textb)
            # c.save()
            params = {'data': c, 'Username': username, 'msg':''}

        context = params
        return render(request, 'OpenCircuitManagement.html', context)
    else:
        return render(request, 'OpenCircuitManagement.html', {'msg':'','Username': username})

#
# texta = request.GET.get('area')
#         print('Value of texta inside GET: ', texta)
#         print('Value of a inside GET is: ', a)
#         print('Value of type(a): ', type(a))
#         astr=str(a)
#         print('Value of astr after converting a to str: ', astr)
#         print('Value of type(astr): ', type(astr))
#         alist = astr.split(',')
#         print('Value of type(alist)): ', type(alist))
#         print('Value of alist: ', alist)
#         for j in range(len(alist)):
#             print("alist[j]: ", alist[j])
#
#         print('Value of dict is new_dict inside GET: ', new_dict.get("id"))
#         b=O.filter(id=new_dict.get("id"))
#         b.update(Updates=texta)
#         params = {'data': b, 'Username': username}
