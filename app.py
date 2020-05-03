import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_table


# external CSS stylesheets
external_stylesheets = [
   {
       'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
       'rel': 'stylesheet',
       'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
       'crossorigin': 'anonymous'
   }
]

trimc= pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv').iloc[:, 1:]
trimd= pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv').iloc[:, 1:]
trimr= pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv').iloc[:, 1:]

trimc.rename(columns={'Country/Region': 'Country'}, inplace=True)

trimc.rename(columns={'Country/Region': 'Country'}, inplace=True)
trimd.rename(columns={'Country/Region': 'Country'}, inplace=True)
trimr.rename(columns={'Country/Region': 'Country'}, inplace=True)

#for the map

dates = pd.DataFrame(trimc.columns[3:], columns=['Date'])
countries= trimc.iloc[:, 0:3]
final=pd.DataFrame()
for i in dates['Date']:
    countries['Date']=i
    countries['Confirmed']=trimc[[i]]
    final=final.append(countries,ignore_index=True)

trimc=trimc.groupby('Country').sum().reset_index()
trimd=trimd.groupby('Country').sum().reset_index()
trimr=trimr.groupby('Country').sum().reset_index()



#Number of Confirms and Deaths
sums= trimc.sum()[3:]
diffsc=[]
for i in range(1,len(sums)):
    diffsc.append(sums[i]-sums[i-1])

sums= trimd.sum()[3:]
diffsd=[]
for i in range(1,len(sums)):
    diffsd.append(sums[i]-sums[i-1])

sums= trimr.sum()[3:]
diffsr=[]
for i in range(1,len(sums)):
    diffsr.append(sums[i]-sums[i-1])

#Worldwide trends of new confirms and deaths
fig3=go.Figure(data=[go.Bar(x=list(trimc.columns[4:]),
                            y=diffsc,
                            name='New Positive Cases'),
                     go.Bar(x=list(trimd.columns[4:]),
                            y=diffsd,
                            name='New Deaths'),
                            go.Bar(x=list(trimr.columns[4:]),
                                   y=diffsr,
                                   name='New Recovered Cases'),
                     ],
               layout=go.Layout(
                    title = 'Number of cases per day',
                   xaxis = {'title': 'Dates'},
                   yaxis = {'title': 'New cases per day'},
                   barmode='stack'))


options=[{'label':'World','value':'All'}]
for i in trimc['Country']:
    options.append({'label':i,'value':i})


#Card Values
total= trimc.iloc[:, -1].sum() + trimd.iloc[:, -1].sum() + trimr.iloc[:, -1].sum()
active=trimc.iloc[:, -1].sum()
deaths= trimd.iloc[:, -1].sum()
recovered= trimr.iloc[:, -1].sum()


#display table
display=pd.DataFrame(list(zip(trimc['Country'].values,trimc.iloc[:,-1].values,)),columns=['Country','Total Cases'])
x=[]
for i in range(0,len(trimc)):
    x.append(trimc.iloc[i,-1]-trimc.iloc[i,-2])
display['New Infections']=x

display['Total Deaths']=trimd.iloc[:,-1].values
x=[]
for i in range(0,len(trimd)):
    x.append(trimd.iloc[i,-1]-trimd.iloc[i,-2])
display['New Deaths']=x

display['Total Recoveries']=trimr.iloc[:,-1].values
x=[]
for i in range(0,len(trimr)):
    x.append(trimr.iloc[i,-1]-trimr.iloc[i,-2])
display['New Recoveries']=x


app = dash.Dash('app', external_stylesheets=external_stylesheets,)
server = app.server


app.layout = html.Div([
    html.Div(html.H1("Covid-19 Global Pandemic Real-time Tracker",style={'color':'#fff','text-align':'center','margin':15,'text-decoration':'underline'}),),
    html.Hr([],style={'border-top': '1px solid white', 'width':'50%'}),
    #cards
    html.Div([
        #cards
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Total Cases", className='text-light'),
                    html.H4(total, className='text-light')
                ], className='card-body')
            ], className='card bg-danger')
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Active Cases", className='text-light'),
                    html.H4(active, className='text-light')
                ], className='card-body')
            ], className='card bg-info')
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Death Cases", className='text-light'),
                    html.H4(deaths, className='text-light')
                ], className='card-body')
            ], className='card', style={'background-color':'#d6b600'})
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Recovery Cases", className='text-light'),
                    html.H4(recovered, className='text-light')
                ], className='card-body')
            ], className='card bg-success')
        ], className='col-md-3'),
    ], className='row', style={'margin':30}),
    html.Hr([], style={'border-top': '1px solid white', 'width': '80%',}),

    #graphs



    #heatmap
    html.Div([
        # html.H4('Heatmap of current positive cases around the globe',style={'color':'#fff','text-align':'right','text-decoration':'underline'}),
        dcc.Graph(figure=px.density_mapbox(final, lat='Lat', lon='Long', z='Confirmed', radius=25,
                        # center=dict(lat=0, lon=180),
                              height=800, zoom=1,
                        mapbox_style="stamen-terrain",
                        hover_name='Country',
                        # labels={dfc.columns[-1]:'Current Cases'},
                        animation_frame='Date',
                        title='Heat Map of positive cases around the globe. Hit the play button to see how it spread.'
                        ),
                  )
    ], style={'margin':40}),



    html.Hr([], style={'border-top': '1px solid white', 'width': '80%', }),

    html.H2('Global trends', style={'color':'#fff','text-align':'center','text-decoration':'underline','margin-top':15}),

    #dropdown country
    html.Div([
        dcc.Dropdown(id='country-picker', options=options, value='All'),
    ],style={'margin-bottom':15,'margin-top':15,'margin-left':35,'margin-right':35},),

    html.Div([
    #checklist for kind

        html.Div([
                dcc.Checklist(
                    options=[
                        {'label': 'Positive', 'value': 'con'},
                        {'label': 'Deceased', 'value': 'ded'},
                        {'label': 'Recovered', 'value': 'rec'}
                    ],
                    value=['con', 'ded', 'rec'],
                    id='check-kind', style={'color':'#fff'}
                )
        ],className='col'),
        html.Div([
                #death ratef06a1d
                html.H4(id='death-rate',style={'background-color':'#d6b600', 'border-radius':'10%','color':'#fff','text-align':'center'}),
                ],className='col-sm',style={'width':'5%'}),

        html.Div([
                #recovery rate1ac486
                html.H4(id='recovery-rate',style={'background-color':'#28a746', 'border-radius':'10%','color':'#fff','text-align':'center'}),
        ],className='col-sm',style={'width':'5%'}),
    ],className='row',style={'margin-bottom':0,'margin-top':15,'margin-left':35,'margin-right':35}),
    #graphs country
    html.Div([
        html.Div([
            dcc.RadioItems(
                options=[
                    {'label': 'Logarithmic', 'value': 'log'},
                    {'label': 'Linear', 'value': 'lin'},
                ],
                value='lin',
                labelStyle={'display': 'inline-block'},
                id='radio',
                style={'color':'#fff'}
            ),
            dcc.Graph(id='country-case-cumulative'),
        ],className='col', style={'margin':5}),
        html.Div([
            dcc.Graph(id='country-case-daily'),
        ], className='col', style={'margin-top': '32px'}),
    ],className='row', style={'padding':30}),
    html.Hr([], style={'border-top': '1px solid white', 'width': '80%', }),

    html.H2('Country vs Country comparisons',
            style={'color': '#fff', 'text-align': 'center', 'text-decoration': 'underline', 'margin-top': 15}),
#
    #dropdown kind
    html.Div([
        dcc.Dropdown(
                    id='countryvs',
                    options=[
                        {'label': 'All', 'value': 'all'},
                        {'label': 'Confirmed', 'value': 'confirmed'},
                        {'label': 'Deceased', 'value': 'deceased'},
                        {'label': 'Recovered', 'value': 'recovered'},
                    ],
                    value='all'
                ),
    ],
    style={'margin-bottom':15,'margin-top':25,'margin-left':35,'margin-right':35}),

    #Slider for range of countries
    html.Div([
html.Div([
    dcc.RangeSlider(
        id='country-range-slider',
        min=0,
        max=180,
        step=5,
        value=[0, 20],
        # allowCross=False,
        tooltip={'always_visible':False, 'placement':'bottomLeft'},
        updatemode='drag',
        pushable=5
    ),
    html.Div(id='output-container-range-slider')
])
    ],style={'margin-bottom':15,'margin-top':25,'margin-left':35,'margin-right':35}),

    #Country vs Country Graphs
    html.Div([
        html.Div([
            dcc.Graph(id='countryvs_totals')
        ],className='col'),
        html.Div([
            dcc.Graph(id='countryvs_daily')
        ],className='col'),
],className='row',style={'margin-bottom':35,'margin-top':25,'margin-left':35,'margin-right':35}),

    html.Hr([], style={'border-top': '1px solid white', 'width': '80%', }),

    #pie
    html.Div([
        html.H4('Total number of positive cases currently= {}'.format(total),style={'color':'#fff','text-align':'right','text-decoration':'underline'}),
        dcc.Graph(figure=px.pie(trimc, values=trimc.iloc[:, -1], names='Country', hover_name='Country', title='Percentage contribution to positive cases of each country').update_traces(textposition='inside', textinfo='percent+label'),)
    ], style={'margin':40,'padding-left':40,'padding-right':40}),
    html.Hr([], style={'border-top': '1px solid white', 'width': '80%', }),

    html.H2('Tabular Data of all countries',
            style={'color': '#fff', 'text-align': 'center', 'text-decoration': 'underline', 'margin-top': 15}),

    #table
    html.Div([
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in display.columns],
            data=display.to_dict('records'),

                style_cell={
                    'fontFamily': 'Open Sans',
                    'textAlign': 'center',
                    'height': '60px',
                    'padding': '2px 22px',
                    'whiteSpace': 'inherit',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                },
                style_cell_conditional=[
                    {
                        'if': {'column_id': 'State'},
                        'textAlign': 'left'
                    },
                ],
                # style header
                style_header={
                    'fontWeight': 'bold',
                    'fontColor': 'white',
                    'backgroundColor': '#bec4d1',
                },
                # style filter
                # style data
                style_data_conditional=[
            {
                # stripped rows
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            },
        ]
    )
    ],style={'padding':30,'margin':25}),

],className='col')

#For Country Specific trends
#Cumulative
@app.callback(Output('country-case-cumulative','figure'), [Input('country-picker','value'),Input('radio','value'),Input('check-kind','value')])
def country_specific_cumulative(type, kind, graph):
    data=[]
    #if one of the countries
    if type in trimc['Country'].values:
        #confirmed graph trace
        if 'con' in graph:
            data.append(go.Scatter(x=list(trimc[trimc['Country']==type].iloc[:,3:].columns),
                               y=trimc[trimc['Country']==type].iloc[:,3:].values.tolist()[0],
                               mode='lines',
                               marker={'color': '#a0065a'},
                               name='Confirmed'),)
        #death graph trace
        if 'ded' in graph:
            data.append(go.Scatter(x=list(trimd[trimd['Country']==type].iloc[:,3:].columns),
                               y=trimd[trimd['Country']==type].iloc[:,3:].values.tolist()[0],
                               mode='lines',
                               marker={'color': '#6b6c6e'},
                               name='Deceased'),)
        #recovered trace
        if 'rec' in graph:
            data.append(go.Scatter(x=list(trimr[trimr['Country']==type].iloc[:,3:].columns),
                               y=trimr[trimr['Country']==type].iloc[:,3:].values.tolist()[0],
                               mode='lines',
                               marker={'color': '#1b63f2'},
                               name='Recovered', ))

    #if all in selected
    if type not in trimc['Country'].values:
        if 'con' in graph:
            data.append(go.Scatter(x=trimc.sum()[3:].reset_index().iloc[:, 0],
                                   y=trimc.sum()[3:].reset_index().iloc[:, 1],
                                   mode='lines',
                                   marker={'color': '#a0065a'},
                                   name='Confirmed'))
        #death graph trace
        if 'ded' in graph:
            data.append( go.Scatter(x=trimd.sum()[3:].reset_index().iloc[:, 0],
                                    y=trimd.sum()[3:].reset_index().iloc[:, 1],
                                    mode='lines',
                                    marker={'color': '#6b6c6e'},
                                    name='Deceased'))
        #recovered trace
        if 'rec' in graph:
            data.append(go.Scatter(x=trimr.sum()[3:].reset_index().iloc[:, 0],
                                   y=trimr.sum()[3:].reset_index().iloc[:, 1],
                                   mode='lines',
                                   marker={'color': '#1b63f2'},
                                   name='Recovered', ))

    if kind=='log':
        return {
            'data': data,
            'layout': go.Layout({
                'xaxis': dict(
                    title='Date'
                ),
                'yaxis': dict(
                    title='Number of people affected',
                    type='log',
                    autorange=True
                ),
                'title': 'Cumulative Cases Confirmed, Deceased and Recovered (Logarithm)'
            })
        }
    if kind == 'lin':
        return {
            'data': data,
            'layout': go.Layout({
                'xaxis': dict(
                    title='Date'
                ),
                'yaxis': dict(
                    title='Number of people affected',
                    # type='log',
                    #  autorange='True'

                ),
                'title': 'Cumulative Cases Confirmed, Deceased and Recovered',
            })
        }

#daily treends per country
@app.callback(Output('country-case-daily', 'figure'), [Input('country-picker','value'),Input('check-kind','value')])
def country_specific_daily(type, graph):
    data =[]
    if type in trimc['Country'].values:
       sums = trimc[trimc['Country'] == type].values.tolist()[0][3:]
       diffsc = []
       for i in range(1, len(sums)):
           diffsc.append(sums[i] - sums[i - 1])

       sums = trimd[trimd['Country'] == type].values.tolist()[0][3:]
       diffsd = []
       for i in range(1, len(sums)):
           diffsd.append(sums[i] - sums[i - 1])

       sums = trimr[trimr['Country'] == type].values.tolist()[0][3:]
       diffsr = []
       for i in range(1, len(sums)):
           diffsr.append(sums[i] - sums[i - 1])

       if  'con' in graph:
           data.append(go.Bar(x=list(trimc.columns[4:]),
                            y=diffsc,
                            name='New Positive Cases'),)
       # death graph trace
       if 'ded' in graph:
           data.append(go.Bar(x=list(trimd.columns[4:]),
                        y=diffsd,
                        name='New Deaths'),)
       # recovered trace
       if 'rec' in graph:
           data.append(go.Bar(x=list(trimr.columns[4:]),
                        y=diffsr,
                        name='New Recovered Cases'))

       #World data
    else:
       sums = trimc.sum()[3:]
       diffsc = []
       for i in range(1, len(sums)):
           diffsc.append(sums[i] - sums[i - 1])

       sums = trimd.sum()[3:]
       diffsd = []
       for i in range(1, len(sums)):
           diffsd.append(sums[i] - sums[i - 1])

       sums = trimr.sum()[3:]
       diffsr = []
       for i in range(1, len(sums)):
           diffsr.append(sums[i] - sums[i - 1])

       if 'con' in graph:
           data.append(go.Bar(x=list(trimc.columns[4:]),
                              y=diffsc,
                              name='New Positive Cases'), )
       # death graph trace
       if 'ded' in graph:
           data.append(go.Bar(x=list(trimd.columns[4:]),
                              y=diffsd,
                              name='New Deaths'), )
       # recovered trace
       if 'rec' in graph:
           data.append(go.Bar(x=list(trimr.columns[4:]),
                              y=diffsr,
                              name='New Recovered Cases'))

    return {
       'data': data,
       'layout': go.Layout({
           'xaxis': dict(
               title='Dates'
           ),
           'yaxis': dict(
               title='New cases per day'
           ),
           'title': 'Number of cases per day',
           'barmode':'stack'
       })
    }

#death rate
@app.callback(Output('death-rate', 'children'), [Input('country-picker','value')])
def death_rate(type):
    if type in display['Country'].values:
        return 'Death Rate= '+str(round(display[display['Country']==type]['Total Deaths'].values[0]/display[display['Country']==type]['Total Cases'].values[0],2))+'%'
    else:
        return 'Death Rate= '+str(round(deaths/active,2))+'%'

#recovery rate
@app.callback(Output('recovery-rate', 'children'), [Input('country-picker','value')])
def recovery_rate(type):
    if type in display['Country'].values:
        return 'Recovery Rate= '+str(round(display[display['Country']==type]['Total Recoveries'].values[0]/display[display['Country']==type]['Total Cases'].values[0],2))+'%'
    else:
        return 'Recovery Rate= '+str(round(recovered/active,2))+'%'






#Country vs country
#country vs country totals

#Country VS Country
#country vs country cumulative
@app.callback(Output('countryvs_totals', 'figure'), [Input('countryvs','value'),Input('country-range-slider','value')])
def country_vs_tot(type, ran):
   if type =='all':
       temp = display.sort_values('Total Cases', ascending=False).iloc[ran[0]:ran[1],:]
       return {
           'data': [go.Bar(x=temp['Country'],
                            y=temp['Total Cases'],
                            name='Total Infections'),
                    go.Bar(x=temp['Country'],
                           y=temp['Total Deaths'],
                           name='Total Deaths'),
                    go.Bar(x=temp['Country'],
                           y=temp['Total Recoveries'],
                           name='Total Recoveries'),
                    ],
           'layout': go.Layout({
               'xaxis': dict(
                   title='Countries'
               ),
               'yaxis': dict(
                   title='Total Cumulative Number of Cases'
               ),
               'title': 'Number of Cumulative Cases per Country',
               'barmode':'stack'
           })
       }
   elif type=='confirmed':
       temp = display.sort_values('Total Cases', ascending=False).iloc[ran[0]:ran[1],:]
       return {

           'data': [go.Bar(x=temp['Country'],
                            y=temp['Total Cases'],
                            name='Total Infections',),
                    ],
           'layout': go.Layout({
               'xaxis': dict(
                   title='Countries'
               ),
               'yaxis': dict(
                   title='Total Cumulative Number of Infections'
               ),
               'title': 'Number of Cumulative Infections per Country',
           })
       }
   elif type=='deceased':
       temp = display.sort_values('Total Deaths', ascending=False).iloc[ran[0]:ran[1],:]
       return {

           'data': [go.Bar(x=temp['Country'],
                            y=temp['Total Deaths'],
                            name='Total Deaths',),
                    ],
           'layout': go.Layout({
               'xaxis': dict(
                   title='Countries'
               ),
               'yaxis': dict(
                   title='Total Cumulative Number of Deaths'
               ),
               'title': 'Number of Cumulative Deaths per Country',
           })
       }
   elif type=='recovered':
       temp = display.sort_values('Total Recoveries', ascending=False).iloc[ran[0]:ran[1],:]
       return {

           'data': [go.Bar(x=temp['Country'],
                            y=temp['Total Recoveries'],
                            name='Total Recoveries',),
                    ],
           'layout': go.Layout({
               'xaxis': dict(
                   title='Countries'
               ),
               'yaxis': dict(
                   title='Total Cumulative Number of Recoveries'
               ),
               'title': 'Number of Cumulative Recoveries per Country',
           })
       }

#country vs country dailies
@app.callback(Output('countryvs_daily', 'figure'), [Input('countryvs','value'),Input('country-range-slider','value')])
def country_vs_daily(type,ran):
   if type =='all':
       temp = display.sort_values('New Infections', ascending=False).iloc[ran[0]:ran[1],:]
       return {
           'data': [go.Bar(x=temp['Country'],
                            y=temp['New Infections'],
                            name='New Infections'),
                    go.Bar(x=temp['Country'],
                           y=temp['New Deaths'],
                           name='New Deaths'),
                    go.Bar(x=temp['Country'],
                           y=temp['New Recoveries'],
                           name='New Recoveries'),
                    ],
           'layout': go.Layout({
               'xaxis': dict(
                   title='Countries'
               ),
               'yaxis': dict(
                   title='Increase in Number of Cases'
               ),
               'title': 'Increases in Cases per Country',
               'barmode':'stack'
           })
       }
   elif type=='confirmed':
       temp = display.sort_values('New Infections', ascending=False).iloc[ran[0]:ran[1],:]
       return {

           'data': [go.Bar(x=temp['Country'],
                            y=temp['New Infections'],
                            name='New Infections'),
                    ],
           'layout': go.Layout({
               'xaxis': dict(
                   title='Countries'
               ),
               'yaxis': dict(
                   title='New Infections'
               ),
               'title': 'New Infections per Country',
           })
       }
   elif type=='deceased':
       temp = display.sort_values('New Deaths', ascending=False).iloc[ran[0]:ran[1],:]
       return {

           'data': [go.Bar(x=temp['Country'],
                            y=temp['New Deaths'],
                            name='New Deaths',),
                    ],
           'layout': go.Layout({
               'xaxis': dict(
                   title='Countries'
               ),
               'yaxis': dict(
                   title='New Deaths'
               ),
               'title': 'New Deaths per Country',
           })
       }
   elif type=='recovered':
       temp = display.sort_values('New Recoveries', ascending=False).iloc[ran[0]:ran[1],:]
       return {

           'data': [go.Bar(x=temp['Country'],
                            y=temp['New Recoveries'],
                            name='New Recoveries',),
                    ],
           'layout': go.Layout({
               'xaxis': dict(
                   title='Countries'
               ),
               'yaxis': dict(
                   title='New Recoveries'
               ),
               'title': 'New Recoveries per Country',
           })
       }


if __name__ == "__main__":
    app.run_server(debug=True)



