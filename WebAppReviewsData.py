import justpy as jp
import pandas
from datetime import datetime
from pytz import utc
from spline import spline_chart_def
from multspline import multspline_chart_def
from stream import stream_chart_def
from pie import pie_chart_def

data=pandas.read_csv("reviews.csv",parse_dates=['Timestamp'])

data['day']=data['Timestamp'].dt.date 
day_avg=data.groupby(['day']).mean()

data['week']=data['Timestamp'].dt.strftime('%Y-%U')
week_avg=data.groupby(['week']).mean()

data['month']=data['Timestamp'].dt.strftime('%Y-%m')
mo_avg=data.groupby(['month']).mean()

mo_crs_avg=data.groupby(['month','Course Name'])['Rating'].count().unstack()

data['dayofwk'] = data['Timestamp'].dt.strftime('%A')
data['nbrday'] = data['Timestamp'].dt.weekday 
happy = data.groupby(['dayofwk','nbrday']).mean() 
happy = happy.sort_values('nbrday')

share=data.groupby(['Course Name'])['Rating'].count()

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
    
    hc_crs_mult = jp.HighCharts(a=wp,options=multspline_chart_def)
    hc_crs_mult.options.title.text = "Number of Ratings by Month by Course"
    hc_crs_mult.options.xAxis.categories = list(mo_crs_avg.index) 
    hc_crs_mult_data = [{"name":v1, "data": [v2 for v2 in mo_crs_avg[v1]]} for v1 in mo_crs_avg.columns]
    hc_crs_mult.options.series = hc_crs_mult_data
    
    hc_crs_stream = jp.HighCharts(a=wp,options=stream_chart_def)
    hc_crs_stream.options.title.text = "Number of Ratings by Month by Course"
    hc_crs_stream.options.xAxis.categories = list(mo_crs_avg.index) 
    hc_crs_stream_data = [{"name":v1, "data": [v2 for v2 in mo_crs_avg[v1]]} for v1 in mo_crs_avg.columns]
    hc_crs_stream.options.series = hc_crs_stream_data
  
    hc_pie = jp.HighCharts(a=wp,options=pie_chart_def)
    hc_pie.options.title.text = "Number of Ratings by Month by Course - Pie Chart"
    hc_pie_data = [{"name":v1, "y": v2} for v1,v2 in zip(share.index,share)]
    hc_pie.options.series[0].data = hc_pie_data

    hc_happy = jp.HighCharts(a=wp,options=spline_chart_def)
    hc_happy.options.title.text = "Aggregated Average Rating by Day of the Week"
    hc_happy.options.xAxis.categories = list(happy.index.get_level_values(0)) 
    hc_happy.options.series[0].data = list(happy['Rating']) #replacing 'data' key's list w another list
    
    return wp 

jp.justpy(app)
