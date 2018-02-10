
# coding: utf-8

# In[8]:


#myapp.ipynb   run "bokeh serve --show myapp.ipynb" in cmd window under same directory with this file
import os
import pandas as pd
import pymysql.cursors
from bokeh.plotting import figure
from bokeh.io import show,output_notebook,output_file,curdoc
from bokeh.layouts import row,column,widgetbox
from bokeh.models import ColumnDataSource,CDSView,BooleanFilter,Select

#change export file directory
os.chdir("d:\\Reference Documents\\Code\\Python\\WorkspaceforPython\\RNO_KPI_Chart")

#connect to database to get data by sql
def get_data_from_sql(site_name,start_date):
    connection=pymysql.connect(host='localhost',user='Test',password='1234',db='sts',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    if connection:
        try:
            with connection.cursor() as cursor:
                sql=("SELECT * FROM `daily_cell_lte_5.1` WHERE CELLNAME LIKE \'"+site_name+"%\' and Time>=\'"+start_date+"\' ORDER BY Time ASC")
                cursor.execute(sql)
                result=cursor.fetchall()
                df=pd.DataFrame(result)
        finally:
            connection.close()
    else:
        print("Failed to connect Database!")
    return df

def get_dataset(src,cellname,kpi):
    df=src[src['CELLNAME']==cellname].copy()
    df=df.loc[:,['Time','CELLNAME',kpi]]
    df['KPI']=df[kpi]
    return ColumnDataSource(data=df)

def update_plot(attrname, old, new):
    src=get_dataset(df_query_result,CELLNAME_SELECT.value,KPI_SELECT.value)
    plot.title.text=KPI_SELECT.value+"--"+CELLNAME_SELECT.value
    plot.legend.text=CELLNAME_SELECT.value
    source.data.update(src.data)
    

def make_plot(source,cellname,kpi):
    plot=figure(plot_width=800,plot_height=500,x_axis_type="datetime")
    plot.circle(x='Time',y='KPI',size=5,source=source)
    plot.title.text=kpi+"--"+cellname
    
    #set some attributes of plot in the future
    return plot


site="RS54M"

date="2018-01-22"

#use get_data_from_sql to get data
df_query_result=get_data_from_sql(site,date)

LTE_KPI=['L-S1 SIG Setup Success Rate','L-RRC Setup Success Rate (Service)']
#get cell list for dropdown selection
CELLNAME_LIST=sorted(df_query_result["CELLNAME"].unique())


#set cell name and kpi for initial plot
initial_cell_name=CELLNAME_LIST[0]
initial_kpi=LTE_KPI[0]

#set dropdown selection
CELLNAME_SELECT=Select(value=initial_cell_name,title="Cell Name",options=sorted(CELLNAME_LIST))
KPI_SELECT=Select(value=initial_kpi,title="KPI",options=LTE_KPI)

#set initial plot
source=get_dataset(df_query_result,CELLNAME_SELECT.value,KPI_SELECT.value)
plot=make_plot(source,CELLNAME_SELECT.value,KPI_SELECT.value)

CELLNAME_SELECT.on_change('value', update_plot)
KPI_SELECT.on_change('value', update_plot)

controls = column(CELLNAME_SELECT,KPI_SELECT)
main_row = row(plot, controls)

curdoc().add_root(main_row)
curdoc().title="KPI"

