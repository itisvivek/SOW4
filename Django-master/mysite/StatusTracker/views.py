from django.shortcuts import render
import sys
#sys.path.append("..")
# Creaste your views here.
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from SearchWo.models import Pegasus

def StatusTracker(request):
    username = request.user.get_username()
    if request.method=='POST':
        if request.POST.get('Logout'):
            logout(request)
            return redirect('/')
        SubmitCriteria=request.POST.get('Search1')
        import xlwt
        from django.http import HttpResponse
        from django.contrib.auth.models import User

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="users.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Users Data')  # this will make a sheet named Users Data

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['ProjectId', 'SvcNo', 'SvcOrderStatus', 'WorkOrder', 'WorkOrderStatus', 'CRD', 'Speed', 'Updates']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        rows = Pegasus.objects.all().values_list('ProjectId', 'SvcNo', 'SvcOrderStatus', 'WorkOrder', 'WorkOrderStatus',
                                                 'CRD', 'Speed', 'Updates')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)

        return response

    else:
        P = Pegasus.objects.all()
        params = {'data': P,'Username':username}
        return render(request,'StatusTracker.html',params)


