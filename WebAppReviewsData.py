import justpy as jp
import pandas
from datetime import datetime
from pytz import utc
from spline import spline_chart_def
data=pandas.read_csv("reviews.csv",parse_dates=['Timestamp'])

data['day']=data['Timestamp'].dt.date 
day_avg=data.groupby(['day']).mean()

data['week']=data['Timestamp'].dt.strftime('%Y-%U')
week_avg=data.groupby(['week']).mean()

data['month']=data['Timestamp'].dt.strftime('%Y-%m')
mo_avg=data.groupby(['month']).mean()

def app():
    wp = jp.QuasarPage() 
    h1 = jp.QDiv(a=wp,text="Analysis of Course Reviews", 
        classes="text-h4 q-pa-md text-center text-weight-bold") 
    p1 = jp.QDiv(a=wp,text="The graphs below represent course review analysis: ",
        classes="q-pl-md") 
    
    hc_day = jp.HighCharts(a=wp, options=spline_chart_def)
    hc_day.options.title.text = "Average Rating by Day"
    hc_day.options.xAxis.categories = list(day_avg.index) 
    hc_day.options.series[0].data =list(day_avg['Rating'])
    
    hc_wk = jp.HighCharts(a=wp,options=spline_chart_def)
    hc_wk.options.title.text = "Average Rating by Week"
    hc_wk.options.xAxis.categories = list(week_avg.index) #creating for categorical data
    hc_wk.options.series[0].data = list(week_avg['Rating'])
    
    hc_mo = jp.HighCharts(a=wp,options=spline_chart_def)
    hc_mo.options.title.text = "Average Rating by Month"
    hc_mo.options.xAxis.categories = list(mo_avg.index) 
    hc_mo.options.series[0].data = list(mo_avg['Rating'])
    
    return wp 

jp.justpy(app)
