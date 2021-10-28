import justpy as jp
import pandas
from datetime import datetime
from pytz import utc
data=pandas.read_csv("reviews.csv",parse_dates=['Timestamp'])

data['day']=data['Timestamp'].dt.date 
day_avg=data.groupby(['day']).mean()

data['week']=data['Timestamp'].dt.strftime('%Y-%U')
week_avg=data.groupby(['week']).mean()

data['month']=data['Timestamp'].dt.strftime('%Y-%m')
mo_avg=data.groupby(['month']).mean()

chart_def = """
{
    chart: {
        type: 'spline',
        inverted: false
    },
    title: {
        text: 'Atmosphere Temperature by Altitude'
    },
    subtitle: {
        text: ''
    },
    xAxis: {
        reversed: false,
        title: {
            enabled: true,
            text: 'Date'
        },
        labels: {
            format: '{value}'
        },
        accessibility: {
            rangeDescription: 'Range: 0 to 80 km.'
        },
        maxPadding: 0.05,
        showLastLabel: true
    },
    yAxis: {
        title: {
            text: 'Average Rating'
        },
        labels: {
            format: '{value}'
        },
        accessibility: {
            rangeDescription: 'Range: -90°C to 20°C.'
        },
        lineWidth: 2
    },
    legend: {
        enabled: false
    },
    tooltip: {
        headerFormat: '<b>{series.name}</b><br/>',
        pointFormat: '{point.x} {point.y}'
    },
    plotOptions: {
        spline: {
            marker: {
                enable: false
            }
        }
    },
    series: [{
        name: 'Average Rating',
        data: [[0, 15], [10, -50], [20, -56.5], [30, -46.5], [40, -22.1],
            [50, -2.5], [60, -27.7], [70, -55.7], [80, -76.5]]
    }]
}
"""

def app():
    wp = jp.QuasarPage() 
    h1 = jp.QDiv(a=wp,text="Analysis of Course Reviews", 
        classes="text-h4 q-pa-md text-center text-weight-bold") 
    p1 = jp.QDiv(a=wp,text="The graphs below represent course review analysis: ",
        classes="q-pl-md") 
    
    hc = jp.HighCharts(a=wp, options=chart_def)
    print(hc.options)
    print(type(hc.options))
    hc.options.title.text = "Average Rating by Day"
    #xAxis in JS code, creating key ‘categoreis'
    hc.options.xAxis.categories = list(day_avg.index) 
    #accessing data 
    hc.options.series[0].data =list(day_avg['Rating'])
    
    hc_wk = jp.HighCharts(a=wp,options=chart_def)
    hc_wk.options.title.text = "Average Rating by Week"
    hc_wk.options.xAxis.categories = list(week_avg.index) #creating for categorical data
    hc_wk.options.series[0].data = list(week_avg['Rating'])
    
    hc_mo = jp.HighCharts(a=wp,options=chart_def)
    hc_mo.options.title.text = "Average Rating by Month"
    hc_mo.options.xAxis.categories = list(mo_avg.index) 
    hc_mo.options.series[0].data = list(mo_avg['Rating'])
    
    return wp 

jp.justpy(app)
