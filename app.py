import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import pandas as pd
import datetime
from datetime import date
import os


app = dash.Dash(__name__,external_stylesheets=[dbc.themes.VAPOR],meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ])
app.title = "Wrist Wearable's Data Monitor"

server = app.server

hr_data = os.path.join(os.path.dirname(os.path.abspath(__file__)),'data/HR-data-2021-12-08 20_37_23.csv')
notes_data = os.path.join(os.path.dirname(os.path.abspath(__file__)),'data/notes.csv')

df = pd.read_csv(notes_data)

df1 = pd.read_csv(hr_data)

df1.dropna(inplace=True)

df1['Date'] = pd.to_datetime(df1['Time']).dt.date
df1['Time'] = pd.to_datetime(df1['Time']).dt.time

moods_list = []

for i in range(len(df)):
    if df['mood'][i] == 'happy':
        moods_list.append("😃")
    elif df['mood'][i] == 'content':
        moods_list.append("🙂")
    elif df['mood'][i] == 'neutral':
        moods_list.append("😐")
    elif df['mood'][i] == 'sad':
        moods_list.append("☹️")
    elif df['mood'][i] == 'angry':
        moods_list.append("😡")
    elif df['mood'][i] == 'bored':
        moods_list.append("😒")
    elif df['mood'][i] == 'tired':
        moods_list.append("😫")
    elif df['mood'][i] == 'grateful':
        moods_list.append("😇")
    elif df['mood'][i] == 'stressed':
        moods_list.append("😓")
    elif df['mood'][i] == 'motivated':
        moods_list.append("🧐")
    elif df['mood'][i] == 'relieved':
        moods_list.append("😌")
    elif df['mood'][i] == 'focused':
        moods_list.append("🤔")
    elif df['mood'][i] == 'irritated':
        moods_list.append("😩")
    elif df['mood'][i] == 'relaxed':
        moods_list.append("😎")
    elif df['mood'][i] == 'hopeful':
        moods_list.append("😏")
    elif df['mood'][i] == 'anxious':
        moods_list.append("😰")
    elif df['mood'][i] == 'frustrated':
        moods_list.append("😖")
    elif df['mood'][i] == 'inspired':
        moods_list.append("🤩")
    elif df['mood'][i] == 'guilt':
        moods_list.append("🤥")
    elif df['mood'][i] == 'ashamed':
        moods_list.append("😬")
    elif df['mood'][i] == 'depressed':
        moods_list.append("😥")
    elif df['mood'][i] == 'indifferent':
        moods_list.append("😕")
    else:
        moods_list.append(" ")

df['emojis'] = moods_list



app.layout = dbc.Container(
                          [
                          html.H1(['Wrist Wearable's Data Monitor'],style={'text-align':'center'}),
                          html.Hr(),
                          
                          dbc.Row(
                                 [
                                 dbc.Col(
                                         [
                                             dbc.Row(html.H3(['Hourly Activity'],style={'text-align':'center'})),
                                             dbc.Row(id='card-content',style={'overflow':'scroll','overflow-x':'hidden','height':'800px'})
                                         ],style={'margin-bottom':'50px'},align='center',md=2
                                     ),
                                 
                                 dbc.Col(
                                        [
                                        dbc.Row(
                                               [
                                               dcc.DatePickerSingle(
                                               id='my-date-picker-single',
                                               min_date_allowed=date(2021, 9, 2),
                                               max_date_allowed=date(2021, 9, 19),
                                               initial_visible_month=date(2021, 9, 1),
                                               date=date(2021, 9, 10)
                                           ),
                                           html.Div(id='output-container-date-picker-single')
                                               ]
                                        ),
                                        dbc.Row(id='graph')
                                        
                                        ],align='center',md=10
                                 )
                                 ]
                          )

                          ],fluid=True
)


@app.callback(
    [Output('output-container-date-picker-single', 'children'),Output('graph','children'),Output('card-content','children')],
    [Input('my-date-picker-single', 'date')]
)

def update_output(date_value):

    df1['Date'] = df1['Date'].astype('str')
    df1['Time'] = df1['Time'].astype('str')

    df_filtered = df[df['full_date'] == date_value]
    df1_filtered = df1[df1['Date'] == date_value]


    df_filtered['full_date'] = pd.to_datetime(df_filtered['full_date'] + ' ' + df_filtered['time'])
    df_filtered['full_date'] = pd.to_datetime(df_filtered['full_date'])
    df_filtered.sort_values('full_date',inplace=True)
    df_filtered.reset_index(inplace=True,drop=True)


    df1_filtered['Date'] = pd.to_datetime(df1_filtered['Date'] + ' ' + df1_filtered['Time'])
    df1_filtered['Date'] = pd.to_datetime(df1_filtered['Date'])
    df1_filtered.sort_values('Date',inplace=True)
    df1_filtered.reset_index(drop=True,inplace=True)



    string_prefix = 'You have selected: '
    if date_value is not None:
        print(date_value)
        date_object = date.fromisoformat(date_value)
        date_string = date_object.strftime('%B %d, %Y')

        fig = go.Figure()

        fig.add_trace(go.Scatter(x=df1_filtered['Date'], y=df1_filtered['Empatica.mean'],
                            mode='lines'))

        fig.update_layout(title_text='Heart Rate',title_font_size=24,font_color='#ffffff',paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",margin=dict(l=0,r=0))

        fig.update_xaxes(showline=True, linewidth=1, linecolor='rgba(255,255,255,0.5)',showgrid=False,zeroline=False)
        fig.update_yaxes(showline=True, linewidth=1, linecolor='rgba(255,255,255,0.5)',showgrid=False,zeroline=False)


        for i in range(len(df_filtered)):

            fig.add_vline(x=datetime.datetime.strptime(str(df_filtered['full_date'][i]), "%Y-%m-%d %H:%M:%S").timestamp() * 1000, line_width=1, line_dash="dash", line_color="#32fbe2",annotation_text=df_filtered['emojis'][i],annotation_position='top',annotation_font_size=32)


        card_content = []

        for i in range(len(df_filtered)):
            card_content.append(dbc.Row(
                    [
                    dbc.Col(dbc.Card(children=[
                                               dbc.CardHeader(children=[df_filtered['time'][i]]),
                                               dbc.CardBody(
                                                   [
                                                       html.P(children=[df_filtered['note'][i]],
                                                             className="card-text",
                                                       ),
                                                   ]
                                               )
                                               ],style={'margin':'10px 0px 10px 10px'},color="primary", inverse=True
                                    )
                            )


                    ]
            ))

        return [string_prefix + date_string,dcc.Graph(figure=fig),card_content]




if __name__ == "__main__":
    app.run_server(debug=False)
