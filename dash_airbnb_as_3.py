import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
import plotly.graph_objs as go
import pandas as pd


# Getting Data
df = pd.read_excel('airbnb_elzonte.xlsx')
df.drop('Unnamed: 0', axis=1, inplace = True)
print(df[['Precio', 'beds']].head())
print(df.shape)



precio_beds = go.Scatter(y = list(df['Precio']), x=list(df['beds']), mode='markers', marker=dict(color="rgba(19,47,99, 0.5)", size=20))

dist_precios = go.Histogram(x=df['Precio'], marker=dict(color='rgb(19,47,99)'))
dist_guests = go.Histogram(x=df['guests'], marker=dict(color='rgb(19,47,99)'))
dist_wifi = go.Histogram(x=df['wifi'], marker=dict(color='rgb(19,47,99)'))
dist_ac = go.Histogram(x=df['air_conditioning'], marker=dict(color='rgb(19,47,99)'))

avg_precio = round(df["Precio"].mean(),2)
avg_ratings = round(df["rating"].mean(),2)
avg_beds = round(df["beds"].mean())
avg_baths = round(df["baths"].mean())


app = dash.Dash(__name__) #allows access to assets folder in wd
server = app.server
# App Layout
app.layout = html.Div([
    html.Div([
        html.H2(["Situacion Actual - El Zonte/La Libertad"], className = "header_text_main"),
        html.Img(src="/assets/logo_as.png")
    ], className = "banner"),
    html.Div([
        html.P(["Podemos elegir entre: Precio, guests, rating, bedrooms, beds, baths, reviews"], className= "general_text_main")
    ]),
    html.Div([
        dcc.Input(id="graph-input", value="beds", type="text"),
        html.Button(id="submit-button", n_clicks = 0, children="Submit")
        ]),

    html.Div([ # Graphs row 1, triggers a callback, thats why it doesn't have a the layout here
        html.Div([ # Graph 1, row 1
            dcc.Graph(
                id = "main_graph",
            )
        ], className="two_columns_75"),


        html.Div([ # Cards Area, make a 2x2 grid

            html.Div([ #first row (cards)
                html.Div([
                    html.Div([
                        html.Div([html.H3(["Precio Promedio"], className="header_text")]),
                        html.Div([html.P(["$" + str(avg_precio)], className="data_text")])
                    ], className = "two_columns"), #first column, first row
                    html.Div([
                        html.Div([html.H3(["Rating Promedio"], className="header_text")]),
                        html.Div([html.P([avg_ratings], className="data_text")])
                    ], className = "two_columns")       
                ], className="row"),            
            ], className ="row"),

            html.Div([ #Second row (cards)
                html.Div([
                    html.Div([
                        html.Div([html.H3(["Camas Promedio"], className="header_text")]),
                        html.Div([html.P([avg_beds], className="data_text")])
                    ], className = "two_columns"), #first column, first row
                    html.Div([
                        html.Div([html.H3(["Baños Promedio"], className="header_text")]),
                        html.Div([html.P([avg_baths], className="data_text")])
                    ], className = "two_columns")       
                ], className="row"),            
            ], className ="row")

        ], className="two_columns_25")
    ], className = "row"), #End of first  general row

    html.Div([ # Graphs, row 2
        html.Div([ # Graph 1, row 2
            dcc.Graph(
                id = "graph_precios",
                figure = {
                    "data": [dist_precios],
                    "layout": {
                        "title": "Distribucion Precios"
                    }
                }
            )
        ], className="two_columns_25"),
        html.Div([ # Graph 2, row 2
            dcc.Graph(
                id = "graph_ratings",
                figure = {
                    "data": [dist_guests],
                    "layout": {
                        "title": "Distribucion de Guests"
                    }
                }
            )
        ], className="two_columns_25"),

        html.Div([ # Graph 3, row 2
            dcc.Graph(
                id = "graph_wifi",
                figure = {
                    "data": [dist_wifi],
                    "layout": {
                        "title": "Distribucion Wifi"
                    }
                }
            )
        ], className="two_columns_25"),

        html.Div([ # Graph 4, row 2
            dcc.Graph(
                id = "graph_ac",
                figure = {
                    "data": [dist_ac],
                    "layout": {
                        "title": "Distribucion AC"
                    }
                }
            )
        ], className="two_columns_25")
    ], className="row")
])
#app.css.append_css({
#    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
#})

@app.callback(dash.dependencies.Output("main_graph", "figure"),
                [dash.dependencies.Input("submit-button", "n_clicks")],
                [dash.dependencies.State("graph-input", "value")])

def update_fig(n_clicks,input_value):

    data = []
    precio_beds = go.Scatter(y = list(df['Precio']), x=list(df[input_value]), mode='markers', marker=dict(color="rgb(19,47,99)", size=10))
    data.append(precio_beds)

    layout = {
        "title": str(input_value) + " contra Precios",
    }
    return {
        "data": data,
        "layout": layout
    }

# Executing server
if __name__ == '__main__':
    app.run_server(debug=True)