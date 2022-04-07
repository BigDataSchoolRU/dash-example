import pandas as pd

import dash
from dash import html
from dash import dcc
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

# Считываем данные
df = pd.read_csv('data/stockdata.csv', index_col=0, parse_dates=True)
df.index = pd.to_datetime(df['Date'])

# Инициализируем сервер
app = dash.Dash(__name__)

#ШАГ 1---------------------------------------------------------------
# Запускаем пустое приложение
# app.layout = html.Div()

#ШАГ 1---------------------------------------------------------------

#ШАГ 2---------------------------------------------------------------
# Разграничиваем плоскость дашборда
# app.layout = html.Div(children=[
#                       html.Div(className='row',
#                                children=[
#                                   html.Div(className='Left column',
#                                         children = [
#                                             html.H2('Dash - пример'),
#                                             html.P('''Визуализация рядов'''),
#                                             html.P('''Выберете одну или несколько акций''')
#                                 ]),  # Левая часть
#                                   html.Div(className='Right column')  # Правая часть
#                                   ])
#                                 ])
#ШАГ 2---------------------------------------------------------------

#ШАГ 3---------------------------------------------------------------
# Выводим временные ряды с ценниками акций
# app.layout = html.Div(
#     children=[
#         html.Div(className='row',
#                  children=[
#                     html.Div(className='four columns div-user-controls',
#                              children=[
#                                             html.H2('Dash - пример'),
#                                             html.P('''Визуализация рядов'''),
#                                             html.P('''Выберете одну или несколько акций''')
#                                 ]
#                              ),
#                     html.Div(className='eight columns div-for-charts bg-grey',
#                              children=[
#                                  dcc.Graph(id='timeseries',
#                                     config={'displayModeBar': False},
#                                     animate=True,
#                                     figure=px.line(df,
#                                                     x='Date',
#                                                     y='value',
#                                                     color='stock',
#                                                     template='plotly_dark').update_layout(
#                                                             {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
#                                                                 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
#                                                                 )                             
#                                         ])
#                               ])
#         ]

# )
#ШАГ 3---------------------------------------------------------------


def get_options(list_stocks):
    dict_list = []
    for i in list_stocks:
        dict_list.append({'label': i, 'value': i})

    return dict_list

#ШАГ 4---------------------------------------------------------------
# Добавим меню для выбора акций для отображения их временных рядов на графике
# app.layout = html.Div(
#     children=[
#         html.Div(className='row',
#                  children=[
#                     html.Div(className='four columns div-user-controls',
#                              children=[
#                                             html.H2('Dash - пример'),
#                                             html.P('''Визуализация рядов'''),
#                                             html.P('''Выберете одну или несколько акций'''),
#                                             html.Div(className='div-for-dropdown',
#                                                         children=[
#                                                             dcc.Dropdown(id='stockselector',
#                                                                         options=get_options(df['stock'].unique()),
#                                                                         multi=True,
#                                                                         value=[df['stock'].sort_values()[0]],
#                                                                         style={'backgroundColor': '#1E1E1E'},
#                                                                         className='stockselector')
#                                                                     ],
#                                                         style={'color': '#1E1E1E'})
#                                 ]
#                              ),
#                     html.Div(className='eight columns div-for-charts bg-grey',
#                              children=[
#                                  dcc.Graph(id='timeseries',
#                                     config={'displayModeBar': False},
#                                     animate=True,
#                                     figure=px.line(df,
#                                                     x='Date',
#                                                     y='value',
#                                                     color='stock',
#                                                     template='plotly_dark').update_layout(
#                                                             {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
#                                                                 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
#                                                                 )                             
#                                         ])
#                               ])
#         ]
# )
#ШАГ 4---------------------------------------------------------------


#ШАГ 5---------------------------------------------------------------
# Свяжем меню выбора названия акции с отображением ее временного ряда на графике
app.layout = html.Div(
    children=[
        html.Div(className='row',
                 children=[
                    html.Div(className='four columns div-user-controls',
                             children=[
                                html.H2('Dash - пример'),
                                html.P('''Визуализация рядов'''),
                                html.P('''Выберете одну или несколько акций'''),
                                 html.Div(
                                     className='div-for-dropdown',
                                     children=[
                                         dcc.Dropdown(id='stockselector', options=get_options(df['stock'].unique()),
                                                      multi=True, value=[df['stock'].sort_values()[0]],
                                                      style={'backgroundColor': '#1E1E1E'},
                                                      className='stockselector'
                                                      ),
                                     ],
                                     style={'color': '#1E1E1E'})
                                ]
                             ),
                    html.Div(className='eight columns div-for-charts bg-grey',
                             children=[
                                 dcc.Graph(id='timeseries', config={'displayModeBar': False}, animate=True)
                             ])
                              ])
        ]

)

# # Callback
@app.callback(Output('timeseries', 'figure'),
              [Input('stockselector', 'value')])
def update_graph(selected_dropdown_value):
    trace1 = []
    df_sub = df
    for stock in selected_dropdown_value:
        trace1.append(go.Scatter(x=df_sub[df_sub['stock'] == stock].index,
                                 y=df_sub[df_sub['stock'] == stock]['value'],
                                 mode='lines',
                                 opacity=0.7,
                                 name=stock,
                                 textposition='bottom center'))
    traces = [trace1]
    data = [val for sublist in traces for val in sublist]
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 15},
                  hovermode='x',
                  autosize=True,
                  title={'text': 'Цены акций', 'font': {'color': 'white'}, 'x': 0.5},
                  xaxis={'range': [df_sub.index.min(), df_sub.index.max()]},
              ),

              }

    return figure
#ШАГ 5---------------------------------------------------------------

# Запускаем приложение
if __name__ == '__main__':
    app.run_server(debug=True)