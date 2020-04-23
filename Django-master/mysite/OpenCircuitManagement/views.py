from django.contrib.auth import logout
from django.shortcuts import render

# Create your views here.
from django import forms
from django.shortcuts import render
import sys
# sys.path.append("..")
# Creaste your views here.
from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.
from BillingStatusTracker.views import username
from SearchWo.models import Pegasus


def OpenCircuits(request):
    if request.POST.get('Logout'):
        logout(request)
        return redirect('/')

    print(request.GET)
    # Username = request.user.get_username()
    if request.method == 'POST':
        print(request.POST)
        print(request.GET)
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

            # global username
            print("Inside second if_after clicking on search")
            Username = request.user.get_username()
            if request.GET.get('team'):
                print(request.POST.get('area'))
                print("Hey...........")

            if SubmitComments == 'UpdateComments':
                print("Hi...")
                UpdateValueArea = request.GET.get("area")
                area_act = UpdateValueArea
                # UpdateValueTeam=request.POST.get("team")
                print("Area: ", area_act)
                print("UpdateValueArea: ", UpdateValueArea)
                # print("UpdateValueTeam: ", UpdateValueTeam)
            else:
                print("Hi....hey")

            # UpdateValue=forms.CharField(widget=forms.Textarea(), required=False) #forms.Textarea()
            params = {'data': O, 'Username': username}
            # render(request, '')
            # params['msg'] = ''

            # return render(request, 'OpenCircuitManagement.html', {'msg': 'Hey!!'})
            return render(request, 'OpenCircuitManagement.html', params)

        # else:
        if SubmitCriteria == 'Search1':
            import xlwt
            from django.http import HttpResponse
            from django.contrib.auth.models import User
            # elif SubmitCriteria == "Search1":
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
        P = Pegasus.objects.all()
        params = {'data': P, 'Username': username}
    return render(request, 'OpenCircuitManagement.html')

    # djtext = request.GET.get('text','default')
    # print(djtext)
    # removepunc = request.GET.get('removepunc', 'off')
    # if removepunc == "on":
    #     punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    #     analyzed = ""
    #     for char in djtext:
    #         if char not in punctuations:
    #             analyzed = analyzed + char
    #
    #     params = {'purpose': 'Removed Punctuations', 'analyzed_text': analyzed}
    #     return render(request, 'OpenCircuitManagement.html', params)
    # else:
    #     return render(request,'OpenCircuitManagement.html')
