import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly
import settings
import pymysql
import redis

from pyorbital.orbital import Orbital
satellite = Orbital('TERRA')

app = dash.Dash()
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

app.layout = html.Div(children=[
    html.H1(children='狗日的知乎用户群分析', style={'textAlign': 'center'}),
    html.Div(className = 'container',children = [
        html.Section(className = 'header',id = 'live-update-text'),
        #知乎男女性别
        dcc.Graph(id = 'male-vs-female'),
        dcc.Interval(
        id='interval-component',
        interval=1*8000, # in milliseconds
        n_intervals=0
    )

    ]),
])

@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    #Mysql Connection
    connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)

    cursor = connect.cursor()

    sql = 'SELECT gender, count(*) AS num FROM person_info GROUP BY gender'

    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        ans = []
        for row in results:
            ans.append(row[1])
    except:
        print('network Error')


    try:
        cursor.execute('SELECT COUNT(*) AS total FROM person_info')
        results = cursor.fetchall()
    except:
        print('network Error')

    red = redis.StrictRedis(host = settings.REDIS_HOST, port = settings.REDIS_PORT, db = 0)
    p = int(str(red.ttl('zhihu:cookie')))
    return [
            html.P('待爬虫的用户队列数：%s' % red.scard('zhihu:request_ID')),
            html.P(children = '已经爬到的用户数目：%s' % results[0][0]),
            html.P('Cookie距离过期还有：%d天, %d小时,%d分, %d秒' % (p / 3600 / 24 ,p / 3600 / 24 % 24, p / 3600 % 60, p % 60))

        ]

@app.callback(Output('male-vs-female', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_male_vs_female(n):
    return {
            'data':[
                go.Pie(
                    labels = [u'未知', u'女','男'],
                    values = [1,2,3]
                    )
            ],
            'layout':{
                'title':'知乎用户性别分布'
            }
        }
if __name__ == '__main__':
    app.run_server(debug=True)