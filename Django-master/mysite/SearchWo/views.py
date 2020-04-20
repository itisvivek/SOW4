from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import redirect
from .models import Pegasus

searchcriteria=''
searchvalue=''

def SearchWo(request):
    #params = Pegasus.objects.all()
    global searchcriteria
    global searchvalue
    if request.method == 'POST':
            Button_Criteria=request.POST.get('Search', 'Search1')
            if Button_Criteria=='Search':

                searchcriteria = request.POST.get('Criteria', 'ProjectId')
                searchvalue = request.POST.get('text')
                if searchcriteria == 'ProjectId':
                    P = Pegasus.objects.filter(ProjectId=searchvalue)
                else:
                    P = Pegasus.objects.filter(SvcNo=searchvalue)
                params = {'data' : P}
                return render(request,'SearchWo.html',params)
            else:

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
        return render(request,'SearchWo.html')

