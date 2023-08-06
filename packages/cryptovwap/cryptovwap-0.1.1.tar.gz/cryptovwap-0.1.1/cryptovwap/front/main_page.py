from .head import *
from .menu import *

from ..back.helpers import *
from ..back import Kraken, Bitvavo
import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input, State

from datetime import timedelta as td

import pandas as pd


external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
    {
        "href": "https://cdnjs.cloudflare.com/ajax"
                "/libs/font-awesome/6.0.0-beta3/css/all.min.css",
        "rel": "stylesheet",
    },
    {
        "href": "https://cdn.jsdelivr.net/npm/"
                "bootstrap@5.1.3/dist/css/bootstrap.min.css",
        "rel": "stylesheet",
    }
]

app = dash.Dash("cryptovwap", external_stylesheets=external_stylesheets)
app.title = "Crypto VWAP"
server = app.server
k = Bitvavo()

app.layout = html.Div(
    children=[
        head,
        menu(k),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="grafica-precio", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        dcc.Store(id='hdata-value'),
        dcc.Store(id='queries-value')
    ]
)


def generate_interval(fecha):
    start = dt_str_datetime(fecha)
    startp1 = start + td(days=1)
    end = startp1 if startp1 < dt.today() else dt.today()
    return dt_datetime_unix(start), dt_datetime_unix(end)


def hist_data(df, symbol, fecha):
    return df[(df["time"].between(fecha, fecha + 24*3600)) & (df["symbol"] == symbol)].sort_values(["time"])


@app.callback(
    Output("grafica-precio", "figure"),
    Output('hdata-value', 'data'),
    Output('queries-value', 'data'),
    [
        State("filtro-exchange", "value"),
        Input("filtro-crypto", "value"),
        Input('filtro-date', "date"),
        Input('filtro-vwap', "value"),
        State('hdata-value', 'data'),
        State('queries-value', 'data')

    ],
)
def update_charts(exchange, symbol, fecha, fvwap, hdata, queries):
    hdata = None if hdata is None else pd.read_json(hdata, orient='split')
    queries = [] if queries is None else queries

    if exchange == "Bitvavo":
        x = Bitvavo()
    if exchange == "Kraken":
        x = Kraken()

    start, end = generate_interval(fecha)

    if ([symbol, fecha]) in queries:
        print("Ya tenemos data")
        data = hist_data(hdata, symbol, start)
        vwap = x.vwap(data, fvwap)
    else:
        data = x.get_data(symbol, start, end)
        vwap = x.vwap(data, fvwap)
        hdata = pd.concat([data, hdata])
        queries.append([symbol, fecha])

    price_chart_figure = {
        "data": [
            {
                "x": data["time"].apply(dt_unix_datetime).apply(str),
                "y": data["price"],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
                'name': symbol
            },
            {
                "x": vwap["time"].apply(dt_unix_datetime).apply(str),
                "y": vwap["vwap"],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
                'name': "VWAP"
            },
        ],
        "layout": {
            "title": {
                "text": "Average Price of Avocados",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897", "#CCCCCC"],
        },
    }

    return price_chart_figure, hdata.to_json(date_format='iso', orient='split'), queries




@app.callback(
    Output("filtro-crypto", "options"),
    Output("filtro-crypto", "value"),
    [
        Input("filtro-exchange", "value"),

    ],
)
def update_charts(exchange):
    if exchange == "Bitvavo":
        x = Bitvavo()
    if exchange == "Kraken":
        x = Kraken()
    return [{"label": x, "value": x} for x in x.get_asset_pairs_symbols()], x.default_trade