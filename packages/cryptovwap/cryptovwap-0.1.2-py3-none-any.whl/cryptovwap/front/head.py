from dash import html

head = html.Div(
    children=[
        html.I(children="", className="header-title fab fa-btc", style={"display": "block"}),
        html.H1(
            children="Crypto VWAP", className="header-title"
        ),
        html.P(
            children="Analizar el comportamiento del precio del aguacate"
                     " y el numero de aguacates vendidos en US"
                     " entre 2015 y 2018",
            className="header-description",
        ),
    ],
    className="header",
)