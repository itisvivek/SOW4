from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import redirect
from SearchWo.models import Pegasus
from django.contrib.auth import authenticate, login, logout

P=''
params={}
def WorkOrderEscalate(request):
    #params = Pegasus.objects.all()
    username = request.user.get_username()

    global searchcriteria, searchvalue, params, P

    if request.method == 'POST':
        if request.method == 'POST':
            if request.POST.get('Logout'):
                logout(request)
                return redirect('/')

            Button_Criteria=request.POST.get('Search', 'Export')
            # print(Button_Criteria)
            if Button_Criteria == 'Search':

                searchcriteria = request.POST.get('Criteria', 'ProjectId')
                searchvalue = request.POST.get('text')

                if searchcriteria == 'ProjectId':
                    P = Pegasus.objects.filter(ProjectId=searchvalue,WorkOrderStatus='OPEN')
                    C = Pegasus.objects.filter(ProjectId=searchvalue).count()
                else:
                    P = Pegasus.objects.filter(SvcNo=searchvalue,WorkOrderStatus='OPEN')
                    C = Pegasus.objects.filter(SvcNo=searchvalue).count()

                if C == 0:
                    params['style'] = "alert-danger"
                    params['msg'] = searchcriteria + " " + searchvalue + " not found"
                elif P.count() == 0:
                    params['style'] = "alert-info"
                    params['msg'] = searchcriteria + " " + searchvalue + " is not Open"
                else:
                    params['msg'] = ''

                username = request.user.get_username()
                params['data'] = P
                params['Username'] = username
                return render(request,'WorkOrderEscalation.html',params)
            else:
                # print('export')
                import xlwt
                from django.http import HttpResponse
                from django.contrib.auth.models import User

                # if searchcriteria == 'ProjectId':
                #     P = Pegasus.objects.filter(ProjectId=searchvalue,WorkOrderStatus='OPEN')
                #
                # else:
                #     P = Pegasus.objects.filter(SvcNo=searchvalue,WorkOrderStatus='OPEN')


                response = HttpResponse(content_type='application/ms-excel')
                response['Content-Disposition'] = 'attachment; filename="users.xls"'

                wb = xlwt.Workbook(encoding='utf-8')
                ws = wb.add_sheet('Users Data')  # this will make a sheet named Users Data

                # Sheet header, first row
                row_num = 0

                font_style = xlwt.XFStyle()
                font_style.font.bold = True

                columns = ['ProjectId', 'SvcNo', 'SvcOrderStatus', 'WorkOrder','WorkOrderStatus','CRD','Speed','Updates']

                for col_num in range(len(columns)):
                    ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

                # Sheet body, remaining rows
                font_style = xlwt.XFStyle()

                rows = P.values_list('ProjectId', 'SvcNo', 'SvcOrderStatus', 'WorkOrder','WorkOrderStatus','CRD','Speed','Updates')
                for row in rows:
                    row_num += 1
                    for col_num in range(len(row)):
                        ws.write(row_num, col_num, row[col_num], font_style)

                wb.save(response)

                return response

    else:
        #print(request.GET.get())
        return render(request,'WorkOrderEscalation.html',{'msg':'', 'Username':username})

