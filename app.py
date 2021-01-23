import dash
import dash_core_components as dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from textblob import TextBlob
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.io as plt_io
app = dash.Dash(__name__, title="🎬 Netflix Analytics 🎥", external_stylesheets=[dbc.themes.GRID])
server=app.server


#Creating template for Dark Theme
plt_io.templates["custom_dark"] = plt_io.templates["plotly_dark"]
plt_io.templates["custom_dark"]['layout']['paper_bgcolor'] = '#1e1e2e'
plt_io.templates["custom_dark"]['layout']['plot_bgcolor'] = '#1e1e2e'
plt_io.templates['custom_dark']['layout']['yaxis']['gridcolor'] = '#342c47'
plt_io.templates['custom_dark']['layout']['xaxis']['gridcolor'] = '#342c47'


#Loading Data
dff=pd.read_csv('./data/netflix_titles.csv')

#Pie chart to show the % of ratings
z = dff.groupby(['rating']).size().reset_index(name='counts')
pieChart = px.pie(z, values='counts', names='rating', title='Distribution of Content Ratings on Netflix 🍕🍿🥃😄▶️💻',color_discrete_sequence=px.colors.qualitative.Set3)
pieChart.layout.template = 'custom_dark'


#TOP 5 Directors
dff['director']=dff['director'].fillna('No Director Specified')
filtered_directors=pd.DataFrame()
filtered_directors=dff['director'].str.split(',',expand=True).stack()
filtered_directors=filtered_directors.to_frame()
filtered_directors.columns=['Director']
directors=filtered_directors.groupby(['Director']).size().reset_index(name='Total Content')
directors=directors[directors.Director !='No Director Specified']
directors=directors.sort_values(by=['Total Content'],ascending=False)
directorsTop5=directors.head()
directorsTop5=directorsTop5.sort_values(by=['Total Content'])
fig2=px.bar(directorsTop5,x='Total Content',y='Director',title='Top 5 Directors on Netflix 🎬 📝')
fig2.layout.template = 'custom_dark'


#TOP 5 Actors
dff['cast']=dff['cast'].fillna('No Cast Specified')
filtered_cast=pd.DataFrame()
filtered_cast=dff['cast'].str.split(',',expand=True).stack()
filtered_cast=filtered_cast.to_frame()
filtered_cast.columns=['Actor']
actors=filtered_cast.groupby(['Actor']).size().reset_index(name='Total Content')
actors=actors[actors.Actor !='No Cast Specified']
actors=actors.sort_values(by=['Total Content'],ascending=False)
actorsTop5=actors.head()
actorsTop5=actorsTop5.sort_values(by=['Total Content'])
fig3=px.bar(actorsTop5,x='Total Content',y='Actor', title='Top 5 Actors on Netflix 💃')
fig3.layout.template = 'custom_dark'



#Trend of MOVIES and TV Shows over the years.
df1=dff[['type','release_year']]
df1=df1.rename(columns={"release_year": "Release Year"})
df2=df1.groupby(['Release Year','type']).size().reset_index(name='Total Content')
df2=df2[df2['Release Year']>=2010]
fig4 = px.line(df2, x="Release Year", y="Total Content", color='type',title='Trend of content produced over the years on Netflix 🍕🍿🥃😄▶️💻')
fig4.layout.template = 'custom_dark'

#Sentiment of movie/tv show description
dfx=dff[['release_year','description']]
dfx=dfx.rename(columns={'release_year':'Release Year'})
for index,row in dfx.iterrows():
    z=row['description']
    testimonial=TextBlob(z)
    p=testimonial.sentiment.polarity
    if p==0:
        sent='Neutral 🔹'
    elif p>0:
        sent='Positive ✔️'
    else:
        sent='Negative ❌'
    dfx.loc[[index,2],'Sentiment']=sent


dfx=dfx.groupby(['Release Year','Sentiment']).size().reset_index(name='Total Content')

dfx=dfx[dfx['Release Year']>=2010]
fig5 = px.bar(dfx, x="Release Year", y="Total Content", color="Sentiment", title="Content Sentiment on Netflix 😃😑😥😡")
fig5.layout.template = 'custom_dark'


# #Movie Statistics Calculator
#
# #Finding the list of countries
dfc=dff[['country']]
dfc=dfc.dropna()
dfc1=dfc['country'].str.split(',',expand=True).stack()
dfc1=dfc1.str.strip()
dfc1=dfc1.drop_duplicates()
dfc1=dfc1[dfc1!=" "]
dfc1=dfc1.dropna()
dfc1=dfc1.drop([27])




app.layout = html.Div(children=[
    html.Header(

        id='header',
        children=[

            html.Img(
                src='/assets/icons8-netflix-desktop-app-48.png',
                id='header-logo',
                alt='logo not loading'
            ),

            html.Div("🎬 Netflix Analytics 🎥", id='header-text')
        ]

    ),
    html.Div([
        dbc.Row([

            dbc.Col(
                html.Div([

                dcc.Graph(id='pie-chart-ratings',figure=pieChart)], id='firstGraphDiv'), width=6
            ),
            dbc.Col(
                html.Div([

                    dcc.Graph(id='cc',figure=fig4)], id='secondGraphDiv'), width=6

            )



        ],align='center'),

        dbc.Row([
            dbc.Col(
                html.Div([
                    dcc.Graph(id='aa', figure=fig2)], id='thirdGraphDiv'),width=6

            ),

            dbc.Col(
                html.Div([
                dcc.Graph(id='bb',figure=fig3)], id='forthGraphDiv'),width=6
            )
        ]),

        dbc.Row([
            dbc.Col(
                html.Div([
                    dcc.Graph(id='dd',figure=fig5),html.Br()])),
            dbc.Col([
                html.Br(),
                html.Br(),

                html.Label('Movie Statistics 🎥📈', id='calculator'),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Div([
                dcc.Dropdown(id='dropDown',options=[{'label':x, 'value': x} for x in dfc1], value='India'),
                    html.Br(),
                    html.Br(),
                    html.Table([
                        html.Tbody([
                            html.Tr([
                                html.Td("No. of Movies till date"),

                                html.Td([
                                    html.Div(
                                        id="val1"

                                    )

                                ])
                            ]),
                            html.Tr([
                                html.Td("No. of TV Shows till date"),

                                html.Td([
                                    html.Div(
                                        id="val2"

                                    )

                                ])
                            ]),
                            html.Tr([
                                html.Td("Top Actor"),

                                html.Td([
                                    html.Div(
                                        id="val3"


                                    )

                                ])
                            ]),
                            html.Tr([
                                html.Td("Top Director"),

                                html.Td([
                                    html.Div(
                                        id="val4"


                                    )

                                ])
                            ])

                        ])
                    ])
                ])
            ])
        ])

    ]),



])

@app.callback(
[Output('val1','children'),Output('val2','children'),Output('val3','children'),Output('val4','children')],
    Input('dropDown','value')

)
def updateTable(dropDown):
    # Number of content produced

    dfx = dff[['type', 'country']]
    dfMovie = dfx[dfx['type'] == 'Movie']
    dfTV = dfx[dfx['type'] == 'TV Show']
    dfM1 = dfMovie['country'].str.split(',', expand=True).stack()
    dfTV1 = dfTV['country'].str.split(',', expand=True).stack()
    dfM1 = dfM1.to_frame()
    dfTV1 = dfTV1.to_frame()
    dfM1.columns = ['country']
    dfTV1.columns = ['country']
    dfM2 = dfM1.groupby(['country']).size().reset_index(name='counts')
    dfTV2 = dfTV1.groupby(['country']).size().reset_index(name='counts')
    dfM2['country'] = dfM2['country'].str.strip()
    dfTV2['country'] = dfTV2['country'].str.strip()
    val11 = dfM2[dfM2['country'] == dropDown]
    val22 = dfTV2[dfTV2['country'] == dropDown]
    val11 = val11.reset_index()
    val22 = val22.reset_index()

    if val11.empty:
        val1 = 0
    else:
        val1 = val11.loc[0]['counts']

    if val22.empty:
        val2 = 0
    else:
        val2 = val22.loc[0]['counts']

    # Top Actor
    dfA = dff[['cast', 'country']]
    dfA = dfA.dropna()
    dfA1 = dfA[dfA['country'].str.contains(dropDown, case=False)]
    dfA2 = dfA1['cast'].str.split(',', expand=True).stack()
    dfA2 = dfA2.to_frame()
    dfA2.columns = ['Cast']
    dfA3 = dfA2.groupby(['Cast']).size().reset_index(name='counts')
    dfA3 = dfA3[dfA3['Cast'] != 'No Cast Specified']
    dfA3 = dfA3.sort_values(by='counts', ascending=False)
    if dfA3.empty:
        val3 = "Actor data from this country is not available"
    else:
        val3 = dfA3.iloc[0]['Cast']


    # Top Director
    dfD = dff[['director', 'country']]
    dfD = dfD.dropna()
    dfD1 = dfD[dfD['country'].str.contains(dropDown, case=False)]
    dfD2 = dfD1['director'].str.split(',', expand=True).stack()
    dfD2 = dfD2.to_frame()
    dfD2.columns = ['Director']
    dfD3 = dfD2.groupby(['Director']).size().reset_index(name='counts')
    dfD3 = dfD3[dfD3['Director'] != 'No Director Specified']
    dfD3 = dfD3.sort_values(by='counts', ascending=False)
    if dfD3.empty:
        val4 = "Director data from this country is not available"
    else:
        val4 = dfD3.iloc[0]['Director']
    return val1, val2, val3, val4

if __name__ == '__main__':

    app.run_server(debug=True)
