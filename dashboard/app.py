import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go


def run():

    print("Python Initiated")

    data_folder = "./Data/"
    # data_folder = "./app/dashboard/Data/"
    
    state_level = pd.read_csv(data_folder+"state_level.csv")

    years = [{'label':y,'value':y} for y in state_level['year'].unique()]
    states = [{'label':s.title(),'value':s} for s in state_level['state'].unique()]

    colors = dict(background='#f1f6f9', text1='#14274e', text2='#394867', border='#9ba4b4')

    # external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    # app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app = dash.Dash(__name__)

    year_selector = dcc.Dropdown(
            id='year_selection',
            options=years,
            value=2019,
            clearable=False
        )

    state_selector = dcc.Dropdown(
            id='state_selection',
            options=states,
            value='UTTAR PRADESH',
            clearable=False
        )
    app.layout = html.Div([
        year_selector,
        
        html.Div(children=[
                html.Div(dcc.Graph(id = 'ec'), style={'display':'inline-block'}),
                html.Div(dcc.Graph(id = 'pc'), style={'display':'inline-block'}),
                html.Div(dcc.Graph(id = 'popular'), style={'display':'inline-block'})],
            style ={'display':'inline-block', 'background-color':colors['background'], 
                    'margin-left':'auto','margin-right':'auto'}

        ), 
        state_selector,
        html.Div(children=[
                html.Div(dcc.Graph(id = 'state_constituency'), style={'display':'inline-block'}),
                html.Div(dcc.Graph(id = 'state_vote'), style={'display':'inline-block'})],
            style ={'display':'inline-block', 'background-color':colors['background'], 
                    'margin-left':'auto','margin-right':'auto',
                    }

        )
    ], style={'background-color':colors['background'],
                'max-width':'800px','borderStyle':'solid', 'borderRadius':'15px',
                'borderWidth':'2px', 'borderColor':colors['border'],'padding':'10px'})

    @app.callback(
        [dash.dependencies.Output('ec', 'figure'),
        dash.dependencies.Output('popular', 'figure'),
        dash.dependencies.Output('pc', 'figure')],
        dash.dependencies.Output('state_vote', 'figure'),
        dash.dependencies.Output('state_constituency', 'figure'),
        [dash.dependencies.Input('year_selection', 'value'),
        dash.dependencies.Input('state_selection', 'value')])
    def update_year_plots(year, state):
        year_plots = generate_year_plots(year, data_folder)
        state_plots = generate_state_plots(year, state, data_folder)
        return year_plots['ec'], year_plots['popular'], year_plots['pc'], \
            state_plots['state_vote'], state_plots['state_constituency']   
    
    app.run_server(host='0.0.0.0', port=8080)
    # app.run_server(debug=True, port=8080)

def generate_year_plots(year, data_folder):
    ec = pd.read_csv(data_folder+"ec.csv")
    pc = pd.read_csv(data_folder+'pc.csv')
    pop = pd.read_csv(data_folder+'popular.csv')

    small_margin = dict(l=10,r=10,t=10,b=5)
    big_margin = dict(l=30,r=30,t=30,b=30)

    ec_year = ec[ec['year']==year].sort_values(by='pc',ascending=False)
    pc_year = pc[pc['year']==year].sort_values(by='pc',ascending=False)
    pop_year = pop[pop['year']==year].sort_values(by='votes',ascending=False)


    colors = {'BJP': 'F97D09', 'INC': '138808','BJD': '01A31C','BSP': "22409A",'CPM': 'DE0000','DMK': 'FF0000',
              'IND': 'FFE6EE','JD(U)': '228B22','Others': 'FFFFFF', 'RJD': '008000', 'SP': '006D02', 'TDP': 'FFFF00',
              'YSRCP': '0266B4','ADMK':'F20636','AITC':'009900'}

    ec_color = []
    for party in list(ec_year['party']):
        ec_color.append(colors[party])
    pop_color = []
    for party in list(pop_year['party']):
        pop_color.append(colors[party])
    pc_color = []
    for party in list(pc_year['party']):
        pc_color.append(colors[party])



    popular_data = go.Pie(labels=list(pop_year['party']), values=list(pop_year['votes']), 
                         name="Popular",sort=True,direction='clockwise',marker_colors=pop_color, 
                          hole = .3, textinfo='label+percent')

    pc_data = go.Pie(labels=list(pc_year['party']), values=list(pc_year['pc']), 
                         name="PC",sort=True,direction='clockwise',marker_colors=pc_color, 
                          hole = .3, textinfo='label+percent')

    ec_data = go.Pie(labels=list(ec_year['party']), values=list(ec_year['pc']), 
                         name="EC",sort=True,direction='clockwise',marker_colors=ec_color, 
                          hole = .3, textinfo='label+percent')

    popular_fig = go.Figure(data=popular_data)

    popular_fig.update_layout(title={
            'text': "Popular Vote",
            'y':0.1,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'bottom'},
            showlegend=False,
            margin=small_margin,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)')

    pc_fig = go.Figure(data=pc_data)

    pc_fig.update_layout(title={
            'text': "Constituencies",
            'y':0.1,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'bottom'},
            showlegend=False,
            margin=small_margin,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)')

    ec_fig = go.Figure(data=ec_data)

    ec_fig.update_layout(title={
            'text': "Electoral College",
            'y':0.1,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'bottom'},
            showlegend=False,
            margin=small_margin,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)')

    popular_fig.layout.width = 250
    pc_fig.layout.width = 250
    ec_fig.layout.width = 250

    popular_fig.layout.height = 420
    pc_fig.layout.height = 420
    ec_fig.layout.height = 420

    return {'popular':popular_fig, 'pc':pc_fig,'ec':ec_fig}

def generate_state_plots(year, state, data_folder):
    state_level = pd.read_csv(data_folder+"state_level.csv")
    colors = {'BJP': 'F97D09', 'INC': '138808','BJD': '01A31C','BSP': "22409A",'CPM': 'DE0000','DMK': 'FF0000',
          'IND': 'FFE6EE','JD(U)': '228B22','Others': 'FFFFFF', 'RJD': '008000', 'SP': '006D02', 'TDP': 'FFFF00',
          'YSRCP': '0266B4','ADMK':'F20636','AITC':'009900'}
    
    small_margin = dict(l=10,r=10,t=10,b=5)
    big_margin = dict(l=30,r=30,t=30,b=30)

    state_slice = state_level[(state_level['year']==year)& (state_level['state']==state)]

    state_color = []
    for party in list(state_slice['party']):
        state_color.append(colors[party])

    state_votes_data = go.Pie(labels=list(state_slice['party']), values=list(state_slice['votes']), 
                         name="Votes",sort=True,direction='clockwise',marker_colors=state_color,
                             hole = .3, textinfo='label+percent')

    state_constituency_data = go.Pie(labels=list(state_slice['party']), values=list(state_slice['pc_won']), 
                         name="Constituencies",sort=True,direction='clockwise',marker_colors=state_color,
                             hole = .3, textinfo='label+percent')

    state_votes_fig = go.Figure(data=state_votes_data)

    state_votes_fig.update_layout(title={
            'text': "{} Votes".format(state.title()),
            'y':0.1,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'bottom'},
            showlegend=False,
            margin=small_margin,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)')

    state_constituency_fig = go.Figure(data=state_constituency_data)

    state_constituency_fig.update_layout(title={
            'text': "{} Constituencies".format(state.title()),
            'y':0.1,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'bottom'},
            showlegend=False,
            margin=small_margin,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)')

    state_votes_fig.layout.width = 250
    state_constituency_fig.layout.width = 250

    state_votes_fig.layout.height = 420
    state_constituency_fig.layout.height = 420

    return {'state_vote':state_votes_fig, 'state_constituency':state_constituency_fig}


if __name__ == '__main__':
    run()

