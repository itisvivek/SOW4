from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import redirect
from SearchWo.models import Pegasus
from django.contrib.auth import authenticate, login, logout

searchcriteria=''
searchvalue=''

def ClosureApproval(request):
    #params = Pegasus.objects.all()
    username = request.user.get_username()
    global searchcriteria
    global searchvalue

    if request.method == 'POST':
            if request.POST.get('Logout'):
                logout(request)
                return redirect('/')
            Button_Criteria=request.POST.get('Search', 'Search1')
            if Button_Criteria=='Search':
                res=1
                searchcriteria = request.POST.get('Criteria', 'ProjectId')
                searchvalue = request.POST.get('text')
                if searchcriteria == 'ProjectId':
                    res = Pegasus.objects.filter(ProjectId=searchvalue,WorkOrderStatus='OPEN').count()
                    if res == 0:
                        P = Pegasus.objects.filter(ProjectId=searchvalue)
                        params = {'data': P, 'Username': username, 'res': res}
                    else:
                        params = {'Username': username, 'res': res}

                else:
                    res = Pegasus.objects.filter(SvcNo=searchvalue, WorkOrderStatus='OPEN').count()
                    if res == 0:
                        P = Pegasus.objects.filter(SvcNo=searchvalue,WorkOrderStatus='CLOSED')
                        params = {'data': P, 'Username': username, 'res': res}
                    else:
                        params = {'Username': username, 'res': res}


                return render(request,'ClosureApproval.html',params)
            else:
                print(searchcriteria)
                import xlwt
                from django.http import HttpResponse
                from django.contrib.auth.models import User

                print(searchcriteria)
                print(searchvalue)
                if searchcriteria == 'ProjectId':
                    P = Pegasus.objects.filter(ProjectId=searchvalue)

                else:
                    P = Pegasus.objects.filter(SvcNo=searchvalue)

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
        return render(request,'ClosureApproval.html',{'Username':username, 'res': 0})

