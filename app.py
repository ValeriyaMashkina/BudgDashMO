from flask import Flask, _app_ctx_stack
from flask_cors import CORS
from sqlalchemy.orm import scoped_session
import dash_bootstrap_components as dbc
from info.queries import *
from info.wrappers import *
from info import reference as ref
from info.database import SessionLocal, engine
from flask import Flask
from datetime import date
import plotly.graph_objs as go
import plotly.express as px
from dash_extensions.snippets import send_bytes
from plotly.io import write_image



import dash_core_components as dcc
import dash_html_components as html
import dash
from dash.dependencies import Input, Output, State
import os
from flask_login import login_user, logout_user, current_user, LoginManager, UserMixin

db = SessionLocal()

Base.metadata.create_all(bind=engine)

server  = Flask(__name__)
CORS(server)
server.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

app = dash.Dash(__name__, server=server, suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.MINTY])


server.config.update(SECRET_KEY=os.urandom(12))




#app.server.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:18FmK7@localhost:5432/BudgDashMO"
#app.server.config["SQLALCHEMY_DATABASE_URI"] = "postgres://kcfwfqwznavpjq:9473936daf43bff3d17c1dd8ab2c28144dfbf677\
#14cb30622e3017bbe55cdeac@ec2-34-197-188-147.compute-1.amazonaws.com:5432/d9eat64jon4dti"
#app.server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'


class User(UserMixin, User):
    pass

login =  html.Div([dcc.Location(id='url_login', refresh=True),
             html.Img(src='http://abali.ru/wp-content/uploads/2011/03/moskovskaya_oblast_gerb-600x805.png',
                            height='55', width='45', style={'textAlign': 'center', 'margin-top': '30px'}),
                   html.Br(),
             html.H3('''Вход:''', id='h3', style={'textAlign': 'center', 'margin-top': '15px'}),

             html.Div(
             [dcc.Input(placeholder='Ваш логин',
                    type='text',
                    id='uname-box', style={'textAlign': 'center', 'align-items': 'center', 'margin-top': '15px'}),
             html.Br(),
             dcc.Input(placeholder='Ваш пароль',
                    type='password',
                    id='pwd-box', style={'textAlign': 'center', 'align-items': 'center', 'margin-top': '15px'}),
             html.Br(),
             dbc.Button(children='Вход',
                    n_clicks=0,
                    type='submit',
                    id='login-button', color="primary",
                        className="me-1", style={'margin-top': '15px'})
              ],

                 style={'display': 'block', 'margin-top': '15px'}),
             html.Div(children='', id='output-state')
        ], style={'textAlign': 'center', 'align-items': 'center'}
)


failed = html.Div([ dcc.Location(id='url_login_df', refresh=True)
            , html.Div([html.H3('Вход не состоялся. Попробуйте еще раз')
                    , html.Br()
                    , html.Div([login])
                    , html.Br()
                    , html.Button(id='back-button', children='Обратно', n_clicks=0)])
        ])



header = html.Div([
    html.Img(src='http://abali.ru/wp-content/uploads/2011/03/moskovskaya_oblast_gerb-600x805.png',
             height = '45', width= '45'),
    html.H3('Бюджетные показатели Московской области'),
                   html.Button(id='back-button', children='Выход', className="me-1", n_clicks=0),
                 html.Br()])

min_debt_date, max_debt_date = get_min_max_date_debt(server.session)


debt = html.Div([dcc.Store(id='debt_session', storage_type='session'),
                html.H4('Государственный и муниципальный долг Московской области'),
                html.H5('Показатель:'),
                dcc.Dropdown(id='debt_dropdown', options= ref.debt_drop_down,
                    value='total_state_debt'),
                html.Br(),
                html.Div(

                    [ html.Div(html.P('c'), style={'display': 'inline-block'}),
                      html.Div(html.Br(), style={'display': 'inline-block'}),
                      html.Div(dcc.DatePickerSingle(
                    id='date_picker_debt_start',
                    min_date_allowed=min_debt_date,
                    max_date_allowed=max_debt_date,
                    date=min_debt_date,
                    month_format='DD-MM-YYYY',
                    placeholder='DD-MM-YYYY', display_format='DD-MM-YYYY'),style={'display': 'inline-block'} ) ,
                    html.Div(html.P('по'), style={'display': 'inline-block'}),
                    html.Div(html.Br(), style={'display': 'inline-block'}),
                    html.Div(dcc.DatePickerSingle(
                    id='date_picker_debt_finish',
                    min_date_allowed=min_debt_date,
                    max_date_allowed=max_debt_date,
                    date=max_debt_date,
                    month_format='DD-MM-YYYY',
                    placeholder='DD-MM-YYYY', display_format='DD-MM-YYYY'), style={'display': 'inline-block'} )
                    ], ),

                    html.Div([html.P('Периодичность'),
                              dcc.RadioItems(
                                  [{'label': 'месяц', 'value': 12},
                                    {'label': 'квартал', 'value': 4},
                                    {'label': 'год', 'value': 1}],
                                  value=1,
                                  id = 'debt_period',
                                  inline=True
                              )]),
                    html.Div([dcc.Graph(id='debt_graph')]),
                    html.Div([
                        html.Div(
                                [dbc.Button('Выгрузить данные', id='export_debt_xls',
                                            color="info", className="mr-1", n_clicks=0),
                                dcc.Download(id="download_debt_xls")],
                                style={'display': 'inline-block'}
                                ),
                        html.Div(
                                [dbc.Button('Выгрузить диаграмму', id='export_debt_png',
                                            color="secondary", className="mr-1", n_clicks=0),
                                dcc.Download(id="download_debt_png")],
                                style={'display': 'inline-block'})
                    ])])


@app.callback(Output('debt_graph', 'figure'),
              [Input('debt_dropdown', 'value'),
               Input('date_picker_debt_start', 'date'),
               Input('date_picker_debt_finish', 'date'),
               Input('debt_period', 'value')])
def update_debt(indicator, start_date, finish_date, period):
    if (indicator is not None) and (start_date is not None) and (finish_date is not None) and (period is not None):
        statement = get_debt_data(server.session, indicator, start_date, finish_date, period)
        debt_df = pd.read_sql(sql=statement.statement, con = server.session.connection())
        debt_df = prepare_debt_dataframe(debt_df)
        fig = px.bar(debt_df, x=debt_df.columns[0], y=debt_df.columns[1], width = 600, height = 500)


        server.session.close()
        return fig

@app.callback(Output('debt_session', 'data'),
              [Input('debt_dropdown', 'value'),
               Input('date_picker_debt_start', 'date'),
               Input('date_picker_debt_finish', 'date'),
               Input('debt_period', 'value')])
def update_debt(indicator, start_date, finish_date, period):
    if (indicator is not None) and (start_date is not None) and (finish_date is not None) and (period is not None):
        statement = get_debt_data(server.session, indicator, start_date, finish_date, period)
        debt_df = pd.read_sql(sql=statement.statement, con = server.session.connection())
        debt_df = prepare_debt_dataframe(debt_df)
        server.session.close()
        return debt_df.to_dict()

@app.callback(Output('download_debt_xls', 'data'),
              [Input('export_debt_xls', 'n_clicks'), Input('debt_session', 'data')],
              prevent_initial_call=True)
def generate_debt_xlsx(n_clicks, debt_data):
    def to_xlsx(bytes_io):
        df = pd.DataFrame(debt_data)
        xslx_writer = pd.ExcelWriter(bytes_io, engine="xlsxwriter")
        df.to_excel(xslx_writer, index=False, sheet_name="sheet1")
        xslx_writer.save()
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'export_debt_xls' in changed_id:
        return send_bytes(to_xlsx, "data.xlsx")


@app.callback(Output('download_debt_png', 'data'),
              [Input('export_debt_png', 'n_clicks'), Input('debt_graph', 'figure')],
              prevent_initial_call=True)
def generate_debt_png(n_clicks, figure):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'export_debt_png' in changed_id:
        return send_bytes(lambda x: write_image(figure, x, format='png'), "figure.{}".format('png'))



city_dates = get_dates_cities(server.session)
city_names = get_names_cities(server.session)

cities = html.Div([dcc.Store(id='cities_session', storage_type='session'),
                html.H4('Городские округа'),
                html.H5('Показатель: '),
                dcc.Dropdown(id='cities_indicators_dropdown', options= ref.cities_indicators_drop_down,
                    value='income'),
                html.Div([html.H4('Состояние'),
                             dcc.RadioItems(
                                 [{'label': 'утверждено', 'value': '_plan'},
                                  {'label': 'исполнено', 'value': '_fact'},
                                 ],
                                 value= '_fact',
                                 id='cities_state',
                                 inline=True
                             )]),
                html.H5('На дату: '),
                dcc.Dropdown(id='cities_date_dropdown', options= city_dates,
                            value=date(2015,1,1)),
                html.H5('Городской округ: '),
                dcc.Dropdown(id='cities_names_dropdown', options=city_names,
                                value=[1,2,3,4,5], multi=True),
                html.Div([dcc.Graph(id='cities_graph')]),
                    html.Div([
                        html.Div(
                                [dbc.Button('Выгрузить данные', id='export_cities_xls', n_clicks=0, color="info", className="mr-1"),
                                dcc.Download(id="download_cities_xls")],
                                style={'display': 'inline-block'}
                                ),
                        html.Div(
                                [dbc.Button('Выгрузить диаграмму', id='export_cities_png', n_clicks=0, color="secondary", className="mr-1"),
                                dcc.Download(id="download_cities_png")],
                                style={'display': 'inline-block'})
                    ])
                   ])

@app.callback(Output('cities_graph', 'figure'),
              [Input('cities_indicators_dropdown', 'value'),
               Input('cities_state', 'value'),
               Input('cities_date_dropdown', 'value'),
               Input('cities_names_dropdown', 'value'),
               ])
def update_cities(indicator, state, date, cities):
    if (indicator is not None) and (state is not None) and (date is not None) and (cities is not None):
        data_statement = get_cities_data(server.session, indicator, state, date, cities)
        cities_data_df = pd.read_sql(sql=data_statement.statement, con = server.session.connection())
        name_statement = get_cities_names(server.session)
        cities_names_df = pd.read_sql(sql=name_statement.statement, con = server.session.connection())
        graph_df = cities_names_df.merge(cities_data_df, how='inner', left_on='id', right_on='territory_id', suffixes=(False, False))
        graph_df = prepare_cities_dataframe(graph_df, indicator, state)
        fig = px.bar(graph_df, x=graph_df.columns[0], y=graph_df.columns[1],width = 600, height = 500)
        server.session.close()
        return fig

@app.callback(Output('cities_session', 'data'),
              [Input('cities_indicators_dropdown', 'value'),
               Input('cities_state', 'value'),
               Input('cities_date_dropdown', 'value'),
               Input('cities_names_dropdown', 'value'),
               ])
def update_cities(indicator, state, date, cities):
    if (indicator is not None) and (state is not None) and (date is not None) and (cities is not None):
        data_statement = get_cities_data(server.session, indicator, state, date, cities)
        cities_data_df = pd.read_sql(sql=data_statement.statement, con = server.session.connection())
        name_statement = get_cities_names(server.session)
        cities_names_df = pd.read_sql(sql=name_statement.statement, con = server.session.connection())
        graph_df = cities_names_df.merge(cities_data_df, how='inner', left_on='id', right_on='territory_id', suffixes=(False, False))
        graph_df = prepare_cities_dataframe(graph_df, indicator, state)
        server.session.close()
        return graph_df.to_dict()


@app.callback(Output('download_cities_xls', 'data'),
              [Input('export_cities_xls', 'n_clicks'),
               Input('cities_session', 'data')],
              prevent_initial_call=True)
def generate_cities_xlsx(n_clicks, cities_data):
    def to_xlsx(bytes_io):
        df = pd.DataFrame(cities_data)
        xslx_writer = pd.ExcelWriter(bytes_io, engine="xlsxwriter")
        df.to_excel(xslx_writer, index=False, sheet_name="sheet1")
        xslx_writer.save()
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'export_cities_xls' in changed_id:
        return send_bytes(to_xlsx, "data.xlsx")


@app.callback(Output('download_cities_png', 'data'),
              [Input('export_cities_png', 'n_clicks'),
               Input('cities_graph', 'figure')],
              prevent_initial_call=True)
def generate_cities_png(n_clicks, figure):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'export_cities_png' in changed_id:
        return send_bytes(lambda x: write_image(figure, x, format='png'), "figure.{}".format('png'))



budget_indicators_names = get_budget_indicators_names(server.session)
min_budg_date, max_budg_date = get_min_max_date_budg(server.session)

budget = html.Div([dcc.Store(id='budget_session', storage_type='session'),
                html.H4('Показатели'),
                html.H5('Показатель: '),
                dcc.Dropdown(id='budget_indicators_dropdown', options=budget_indicators_names,
                                value=[1, 41, 131], multi=True),

                html.Div([html.H5('Уровень бюджета'),
                             dcc.RadioItems(
                                 [{'label': 'консолидированный', 'value': 'consolidated'},
                                  {'label': 'областной', 'value': 'region'},
                                 ],
                                 value= 'consolidated',
                                 id='budget_level',
                                 inline=True
                             )]),
                html.Div([html.H5('Состояние'),
                             dcc.RadioItems(
                                 [{'label': 'утверждено', 'value': '_plan'},
                                  {'label': 'исполнено', 'value': '_fact'},
                                 ],
                                 value= '_fact',
                                 id='budget_state',
                                 inline=True
                             )]),

                html.Div(

                    [ html.Div(html.P('c'), style={'display': 'inline-block'}),
                      html.Div(html.Br(), style={'display': 'inline-block'}),
                      html.Div(dcc.DatePickerSingle(
                    id='date_picker_budget_start',

                    min_date_allowed=min_budg_date,
                    max_date_allowed=max_budg_date,
                    date=min_budg_date,

                    month_format='DD-MM-YYYY',
                    placeholder='DD-MM-YYYY', display_format='DD-MM-YYYY'),
                          style={'display': 'inline-block'} ) ,
                    html.Div(html.P('по'), style={'display': 'inline-block'}),
                    html.Div(html.Br(), style={'display': 'inline-block'}),
                    html.Div(dcc.DatePickerSingle(
                    id='date_picker_budget_finish',

                    min_date_allowed=min_budg_date,
                    max_date_allowed=max_budg_date,
                    date=max_budg_date,


                    month_format='DD-MM-YYYY',
                    placeholder='DD-MM-YYYY', display_format='DD-MM-YYYY'),
                        style={'display': 'inline-block'} )
                    ], ),

                    html.Div([html.P('Периодичность'),
                              dcc.RadioItems(
                                  [{'label': 'месяц', 'value': 12},
                                    {'label': 'квартал', 'value': 4},
                                    {'label': 'год', 'value': 1}],
                                  value=1,
                                  id = 'budget_period',
                                  inline=True
                              )]),

                html.Div([dcc.Graph(id='budg_graph')]),
                    html.Div([
                        html.Div(
                                [dbc.Button('Выгрузить данные', id='export_budg_xls', n_clicks=0,
                                            color="info", className="mr-1"),
                                dcc.Download(id="download_budg_xls")],
                                style={'display': 'inline-block'}
                                ),
                        html.Div(
                                [dbc.Button('Выгрузить диаграмму', id='export_budg_png', n_clicks=0,
                                            color="secondary", className="mr-1"),
                                dcc.Download(id="download_budg_png")],
                                style={'display': 'inline-block'})
                    ])
                   ])



@app.callback(Output('budg_graph', 'figure'),
              [Input('budget_indicators_dropdown', 'value'),
               Input('budget_level', 'value'),
               Input('budget_state', 'value'),
               Input('date_picker_budget_start', 'date'),
               Input('date_picker_budget_finish', 'date'),
               Input('budget_period', 'value')])
def update_budg(indicators, level, state, date_start, date_finish, period):
    if (indicators is not None) and \
            (level is not None) and \
            (state is not None) and \
            (date_start is not None) and \
            (date_finish is not None) and \
            (period is not None):
        data_statement = get_budget_data(server.session, indicators, level, state, date_start, date_finish, period)
        budget_data_df = pd.read_sql(sql=data_statement.statement, con = server.session.connection())

        budget_indicators_names_df=pd.DataFrame(budget_indicators_names)
        graph_df = budget_indicators_names_df.merge(budget_data_df, how='inner',
                                                 left_on='value', right_on='indicator_id',
                                                 suffixes=(False, False))

        graph_df = prepare_budget_dataframe(graph_df)
        fig = { 'data':
                [{'x': graph_df[graph_df['Показатель']==label]['На дату'],
                 'y': graph_df[graph_df['Показатель']==label]['Значение, тыс.рублей'],
                 'type': 'bar', 'name': label} for label in graph_df['Показатель'].unique()] ,
            'layout': {'width': 750, 'height': 550}}
        server.session.close()
        return fig

@app.callback(Output('budget_session', 'data'),
              [Input('budget_indicators_dropdown', 'value'),
               Input('budget_level', 'value'),
               Input('budget_state', 'value'),
               Input('date_picker_budget_start', 'date'),
               Input('date_picker_budget_finish', 'date'),
               Input('budget_period', 'value')])
def update_budg(indicators, level, state, date_start, date_finish, period):
    if (indicators is not None) and \
            (level is not None) and \
            (state is not None) and \
            (date_start is not None) and \
            (date_finish is not None) and \
            (period is not None):
        data_statement = get_budget_data(server.session, indicators, level, state, date_start, date_finish, period)
        budget_data_df = pd.read_sql(sql=data_statement.statement, con=server.session.connection())

        budget_indicators_names_df = pd.DataFrame(budget_indicators_names)
        graph_df = budget_indicators_names_df.merge(budget_data_df, how='inner',
                                                 left_on='value', right_on='indicator_id',
                                                 suffixes=(False, False))
        graph_df = prepare_budget_dataframe(graph_df)
        server.session.close()
        return graph_df.to_dict()


@app.callback(Output('download_budg_xls', 'data'),
              [Input('export_budg_xls', 'n_clicks'),
               Input('budget_session', 'data')],
              prevent_initial_call=True)
def generate_budg_xlsx(n_clicks, budg_data):
    def to_xlsx(bytes_io):
        df = pd.DataFrame(budg_data)
        xslx_writer = pd.ExcelWriter(bytes_io, engine="xlsxwriter")
        df.to_excel(xslx_writer, index=False, sheet_name="sheet1")
        xslx_writer.save()
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'export_budg_xls' in changed_id:
        return send_bytes(to_xlsx, "data.xlsx")


@app.callback(Output('download_budg_png', 'data'),
              [Input('export_budg_png', 'n_clicks'),
               Input('budg_graph', 'figure')],
              prevent_initial_call=True)
def generate_budg_png(n_clicks, figure):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'export_budg_png' in changed_id:
        return send_bytes(lambda x: write_image(figure, x, format='png'), "figure.{}".format('png'))





struct_dates = get_struct_dates(server.session)
struct_indicators_names = get_struct_indicators_names(server.session)

struct = html.Div([dcc.Store(id='struct_session', storage_type='session'),
                html.H4('Структура'),
                html.Div([html.H5('Уровень бюджета'),
                             dcc.RadioItems(
                                 [{'label': 'консолидированный', 'value': 'consolidated'},
                                  {'label': 'областной', 'value': 'region'},
                                  ],
                                 value='consolidated',
                                 id='struct_level',
                                 inline=True
                             )]),
                html.Div([html.H5('Состояние'),
                             dcc.RadioItems(
                                 [{'label': 'утверждено', 'value': '_plan'},
                                  {'label': 'исполнено', 'value': '_fact'},
                                  ],
                                 value='_plan',
                                 id='struct_state',
                                 inline=True
                             )]),



                html.H5('На дату: '),
                dcc.Dropdown(id='struct_date_dropdown', options=struct_dates,
                                value=date(2015, 2, 1)),
                html.H5('Показатель: '),
                dcc.Dropdown(id='struct_indicators_dropdown', options=struct_indicators_names,
                                value=1),

                html.Div([dcc.Graph(id='struct_graph')]),
                   html.Div([
                       html.Div(
                           [dbc.Button('Выгрузить данные', id='export_struct_xls', n_clicks=0, color="info", className="mr-1"),
                            dcc.Download(id="download_struct_xls")],
                           style={'display': 'inline-block'}
                       ),
                       html.Div(
                           [dbc.Button('Выгрузить диаграмму', id='export_struct_png', n_clicks=0, color="secondary", className="mr-1"),
                            dcc.Download(id="download_struct_png")],
                           style={'display': 'inline-block'})
                   ])
                ])

@app.callback(Output('struct_graph', 'figure'),
              [Input('struct_level', 'value'),
               Input('struct_state', 'value'),
               Input('struct_date_dropdown', 'value'),
               Input('struct_indicators_dropdown', 'value')
               ])
def update_struct(level, state, date, indicator):
    if (level is not None) and \
            (state is not None) and \
            (date is not None) and \
            (indicator is not None):
        data_statement = get_struct_data(server.session, level, state, date, indicator)

        struct_data_df = pd.read_sql(sql=data_statement.statement, con = server.session.connection())

        struct_data_df = prepare_struct_dataframe(struct_data_df)

        fig = go.Figure(data=[go.Pie(labels=struct_data_df['Показатель'],
                                     values=struct_data_df['Значение, тыс.рублей'], hole=.3,
                                     )])

        server.session.close()
        return fig




@app.callback(Output('struct_session', 'data'),
              [Input('struct_level', 'value'),
               Input('struct_state', 'value'),
               Input('struct_date_dropdown', 'value'),
               Input('struct_indicators_dropdown', 'value')
               ])
def update_struct(level, state, date, indicator):
    if (level is not None) and \
            (state is not None) and \
            (date is not None) and \
            (indicator is not None):
        data_statement = get_struct_data(server.session, level, state, date, indicator)

        struct_data_df = pd.read_sql(sql=data_statement.statement, con=server.session.connection())
        struct_data_df = prepare_struct_dataframe(struct_data_df)
        server.session.close()
        return struct_data_df.to_dict()

@app.callback(Output('download_struct_xls', 'data'),
              [Input('export_struct_xls', 'n_clicks'),
               Input('struct_session', 'data')],
              prevent_initial_call=True)
def generate_struct_xlsx(n_clicks, struct_data):
    def to_xlsx(bytes_io):
        df = pd.DataFrame(struct_data)
        xslx_writer = pd.ExcelWriter(bytes_io, engine="xlsxwriter")
        df.to_excel(xslx_writer, index=False, sheet_name="sheet1")
        xslx_writer.save()
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'export_struct_xls' in changed_id:
        return send_bytes(to_xlsx, "data.xlsx")


@app.callback(Output('download_struct_png', 'data'),
              [Input('export_struct_png', 'n_clicks'),
               Input('struct_graph', 'figure')],
              prevent_initial_call=True)
def generate_struct_png(n_clicks, figure):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'export_struct_png' in changed_id:
        return send_bytes(lambda x: write_image(figure, x, format='png'), "figure.{}".format('png'))


success = html.Div(
    [dcc.Location(id='url_login_success', refresh=True),
     header, html.Div([budget, struct],style={'display': 'inline-block'}),
     html.Div([cities, debt],style={'display': 'inline-block'})]) #end div

app.layout= html.Div([
            html.Div(id='page-content', className='content')
            ,  dcc.Location(id='url', refresh=False)])

@login_manager.user_loader
def load_user(user_id):
    return server.session.query(User).filter_by(id=user_id).first()

@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return login
    elif pathname == '/success':
        if current_user.is_authenticated:
            return success
        else:
            return failed
    else:
        return '404'

@app.callback(
    Output('url_login', 'pathname')
    , [Input('login-button', 'n_clicks')]
    , [State('uname-box', 'value'), State('pwd-box', 'value')])
def successful(n_clicks, input1, input2):
    user = server.session.query(User).filter_by(login=input1).first()
    if user:
        if  (user.password == input2):
            login_user(user)
            return '/success'
        else:
            pass
    else:
        pass

@app.callback(
    Output('output-state', 'children')
    , [Input('login-button', 'n_clicks')]
    , [State('uname-box', 'value'), State('pwd-box', 'value')])
def update_output(n_clicks, input1, input2):
    if n_clicks > 0:
        user = server.session.query(User).filter_by(login=input1).first()
        if user:
            if (user.password == input2):
                return ''
            else:
                return 'Неправильный логин или пароль'
        else:
            return 'Неправильный логин или пароль'
    else:
        return ''

@app.callback(Output('url_login_success', 'pathname'), [Input('back-button', 'n_clicks')])
def logout_dashboard(n_clicks):
    if n_clicks > 0:
        return '/'

@app.callback(Output('url_login_df', 'pathname'), [Input('back-button', 'n_clicks')])
def logout_dashboard(n_clicks):
    if n_clicks > 0:
        return '/'

@app.callback(Output('url_logout', 'pathname'), [Input('back-button', 'n_clicks')])
def logout_dashboard(n_clicks):
    if n_clicks > 0:
        return '/'

if __name__ == '__main__':
    app.run_server(debug=True)