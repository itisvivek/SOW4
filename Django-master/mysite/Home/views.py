from django.shortcuts import render
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from . import models
from Home.models import Pol
import sqlite3
import pandas as pd
import io
import datetime
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
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
        a=os.path.join(BASE_DIR, 'db.sqlite3')
        con = sqlite3.connect(a)
        cur = con.cursor()
        df = pd.read_sql_query("SELECT * from POL", con)
        df1 = pd.read_sql_query("SELECT * from SearchWo_pegasus", con)

        con.close()

        # print(df.head())
        # print(df1.head())

        esd = df.groupby('ProjectStatus', as_index=False).agg({"ProjectID": "count"})
        print('Columns: ', esd.columns)
        Tasks = []
        Tasks = esd['ProjectID'].values.tolist()
        my_labels = esd['ProjectStatus'].values.tolist()

        # df1 = pd.read_excel(xls, 'Pegasus table')

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

        fig = px.pie(esd, values=Tasks, names=my_labels,
                     color_discrete_sequence=px.colors.sequential.Blugrn)  # diverging.Tropic)
        fig.update_traces(hoverinfo='label+percent', textinfo='value')
        # fig.show()

        fig1 = px.pie(wo, values=wo_tasks, names=wo_labels, color_discrete_sequence=px.colors.sequential.Oryel)
        fig1.update_traces(hoverinfo='label+percent', textinfo='value')
        graph = fig.to_html(full_html=False, default_height=350, default_width=500)
        graph1 = fig1.to_html(full_html=False, default_height=350, default_width=500)

        context = {'graph': graph, 'graph1': graph1, 'count_wo_closed': count_wo_closed, 'count_wo': count_wo,
                   'count_ckts_closed': count_ckts_closed, 'count_ckts': count_ckts,'Username':username}  # , 'graph2': graph2}
        # response = render(request, 'graph.html', context)
        response = render(request, 'Home.html', context)
        # response = render(request, '../Home/templates/Home.html', context)
        return (response)


