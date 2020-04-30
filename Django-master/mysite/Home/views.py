from django.shortcuts import render
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from SearchWo.models import Pegasus
from . import models
from Home.models import Pol
import sqlite3
import pandas as pd
import io
import datetime
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
from plotly.subplots import make_subplots


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@login_required(login_url='/')
def Home(request):
    username = request.user.get_username()
    if request.method == 'POST':
        logout(request)
        return redirect('/')
    else:

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        a = os.path.join(BASE_DIR, 'db.sqlite3')
        con = sqlite3.connect(a)
        cur = con.cursor()
        df = pd.read_sql_query("SELECT * from POL", con)
        df1 = pd.read_sql_query("SELECT * from SearchWo_pegasus", con)

        con.close()

        # print(df.head())
        # print(df1.head())
        ## Get the data for projects
        esd = df.groupby('ProjectStatus', as_index=False).agg({"ProjectID": "count"})
        print('Columns: ', esd.columns)
        Tasks = []
        Tasks = esd['ProjectID'].values.tolist()
        my_labels = esd['ProjectStatus'].values.tolist()

        # df1 = pd.read_excel(xls, 'Pegasus table')
        ## get the data for work orders
        wodf1 = df1[['WorkOrder', 'WorkOrderStatus']]
        wodf1 = wodf1.drop_duplicates(subset=None, keep='first', inplace=False)
        wo = wodf1.groupby('WorkOrderStatus', as_index=False).agg({"WorkOrder": "count"})
        wo_tasks = wo['WorkOrder'].values.tolist()
        wo_labels = wo['WorkOrderStatus'].values.tolist()

        c_df = df1[['SvcNo', 'SvcOrderStatus']]
        c_df = c_df.drop_duplicates(subset=None, keep='first', inplace=False)
        count_ckts = len(c_df['SvcNo'])
        count_ckts_closed = len(c_df.loc[(c_df['SvcOrderStatus'] == 'CLOSED')])
        count_wo = len(wodf1['WorkOrder'])
        count_wo_closed = len(wodf1.loc[(wodf1['WorkOrderStatus'] == 'CLOSED')])
        ckt = c_df.groupby('SvcOrderStatus', as_index=False).agg({'SvcNo': 'count'})
        ckt_tasks = ckt['SvcNo'].values.tolist()
        ckt_labels = ckt['SvcOrderStatus'].values.tolist()

        # count_prjts = len(c_df['SvcNo'])
        # count_prjts_closed = len(c_df.loc[(c_df['SvcOrderStatus'] == 'CLOSED')])


        print('Total counts of ckts: ', count_ckts)
        print('Total completed ckts: ', count_ckts_closed)

        # To plot 2 pie charts side by side
        # seperator = ', '
        #
        # def converttostr(input_seq, seperator):
        #     final_string = seperator.join(input_seq)
        #     return final_string
        #
        # name_product = converttostr(my_labels, seperator)
        # name_wo = converttostr(wo_labels, seperator)
        #
        # fig_img = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "pie"}]])
        # # pd1 = "(esd, values=Tasks, names=my_labels, color_discrete_sequence=px.colors.sequential.RdBu)"
        # # pd2 = "(wo, values=wo_tasks, names=wo_labels, color_discrete_sequence=px.colors.sequential.RdBu)"
        #
        # fig_img.add_trace(
        #     go.Pie(values=Tasks, domain=dict(x=[0, 0.5]), name=name_product), row=1, col=1
        #     # color_discrete_sequence=px.colors.sequential.RdBu)
        # )
        #
        # fig_img.add_trace(
        #     go.Pie(values=wo_tasks, domain=dict(x=[0.5, 1.0]), name=name_wo), row=1, col=2
        #     # color_discrete_sequence=px.colors.sequential.RdBu)
        # )
        #
        # fig_img.update_layout(height=600, width=800, title_text="Side By Side Subplots")
        # fig.show()

        # graph2 = fig_img.to_html(full_html=False, default_height=500, default_width=700)

        ## Creating graphs and passing it to table

        fig = px.pie(esd, values=Tasks, names=my_labels,
                     color_discrete_sequence=px.colors.sequential.Blugrn)  # diverging.Tropic)
        fig.update_traces(hoverinfo='label+percent', textinfo='value')

        fig1 = px.pie(wo, values=wo_tasks, names=wo_labels, color_discrete_sequence=[px.colors.sequential.PuBu[4]])#px.colors.sequential.PuBu)
        fig1.update_traces(hoverinfo='label+percent', textinfo='value')

        fig2 = px.pie(c_df, values=ckt_tasks, names=ckt_labels, color_discrete_sequence=[px.colors.sequential.speed[2]])
        fig2.update_traces(hoverinfo='label+percent', textinfo='value')

        graph = fig.to_html(full_html=False, default_height=300, default_width=300)
        graph1 = fig1.to_html(full_html=False, default_height=300, default_width=300)
        graph2 = fig2.to_html(full_html=False, default_height=300, default_width=300)

        ## Pass the table contents
        P = Pegasus.objects.filter(SvcOrderStatus='OPEN',WorkOrderStatus='OPEN').order_by('CRD')

        ## Pass the pie charts using go
        # import plotly.graph_objects as go
        # fig4 = go.Figure()
        # fig4.add_trace(go.Funnel(name='Test',orientation="h", y=[my_labels,wo_labels,ckt_labels], x=[Tasks,wo_tasks,ckt_tasks],
        #                          textposition = "inside", textinfo = "label"))
        #
        # fig4.update_layout(yaxis={'type': df1['ProjectId']})
        # graph4 = fig4.to_html(full_html=False, default_height=300, default_width=300)

        #############################################
        ##Sunburst chart:
        fig3 = px.sunburst(df1, path=['ProjectId', 'SvcNo', 'SvcOrderStatus', 'WorkOrder', 'WorkOrderStatus'], #, 'Task_Name', 'Task_Status'],
                           color='ProjectId')
            # , color_discrete_map={'ProjectId':'darkblue', 'SvcNo':'cyan', 'SvcOrderStatus':'purple',
            #                                    'WorkOrder':'cyan', 'WorkOrderStatus':'grey'}) #, color_continuous_scale='RdBu'
        # fig3 = go.Figure(go.Sunburst(
        #     labels=[wo_labels],
        #     parents=[my_labels],
        #     values=[wo_tasks],
        # ))
        fig3.update_layout(margin=dict(t=0, l=0, r=0, b=0))
        graph3 = fig3.to_html(full_html=False, default_height=400, default_width=500)
        #############################################


        context = {'graph': graph, 'graph1': graph1, 'graph2': graph2, 'graph3': graph3,
                   'count_wo_closed': count_wo_closed, 'count_wo': count_wo,
                   'count_ckts_closed': count_ckts_closed, 'count_ckts': count_ckts, 'Username': username,
                   'data': P}  # , 'graph2': graph2}
        # response = render(request, 'graph.html', context)
        response = render(request, 'Home.html', context)
        # response = render(request, '../Home/templates/Home.html', context)
        return (response)
