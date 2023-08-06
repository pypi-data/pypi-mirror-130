import dash
from dash import dcc
from dash import html
import numpy as np
from dash.dependencies import Output, Input
from datetime import date
import krakenex
from pykrakenapi import KrakenAPI
from practica_kraken.kraken import Kraken

api = krakenex.API()
k = KrakenAPI(api)

df_assets_info = Kraken.get_asset_info(k)
time_frame = ['1 min', '5 min', '30 min', '1 hora', '4 horas', '24 horas']

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Análisis de Cryptomonedas"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🪙", className="header-emoji"),
                html.H1(
                    children="Análisis de Cryptomonedas",
                    className="header-title"
                ),
                html.P(
                    children="Analizar el comportamiento de un par de cryptomonedas desde Kraken"
                             " mediante el cálculo de su vwap para un tiempo determinado."
                             " Este cálculo del vwap se hará intradía.",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Moneda A", className="menu-title"),
                        dcc.Dropdown(
                            id="filtro-asset1",
                            options=[
                                {"label": asset1, "value": asset1}
                                for asset1 in np.sort(df_assets_info.altname.unique())
                            ],
                            value='XBT',
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Moneda B", className="menu-title"),
                        dcc.Dropdown(
                            id="filtro-asset2",
                            options=[
                                {"label": asset2, "value": asset2}
                                for asset2 in np.sort(df_assets_info.altname.unique())
                            ],
                            value='USDT',
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Fecha", className="menu-title"),
                        dcc.DatePickerSingle(
                            id="seleccion-fecha",
                            min_date_allowed=date(2021, 11, 10),
                            max_date_allowed=date(2021, 12, 10),
                            date=date(2021, 12, 3)
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Intervalo", className="menu-title"),
                        dcc.Dropdown(
                            id="seleccion-intervalo",
                            options=[
                                {"label": frame, "value": frame}
                                for frame in time_frame
                            ],
                            value='5 min',
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Hora Inicio - Fin",
                            className="menu-title"
                        ),
                        dcc.RangeSlider(
                            id='seleccion-hora',
                            min=0,
                            max=24,
                            step=0.5,
                            marks={
                                    0: '0 horas',
                                    8: '8 horas',
                                    16: '16 horas',
                                    24: '24 horas'
                                },
                            value=[8, 9],
                            tooltip={
                                "placement": "bottom",
                                "always_visible": True},
                            className="range-slider"
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="grafica-comun", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)


@app.callback(
    Output("grafica-comun", "figure"),
    [
        Input("filtro-asset1", "value"),
        Input("filtro-asset2", "value"),
        Input("seleccion-fecha", "date"),
        Input("seleccion-intervalo", "value"),
        Input("seleccion-hora", "value"),
    ],
)
def update_charts(asset1, asset2, date, frame, value):
    pair = Kraken.set_pair(k, asset1, asset2)
    unix_from_date, unix_to_date = Kraken.set_dates(k, date, value)
    df_trades = Kraken.get_recent_dates(k, pair, unix_from_date, unix_to_date)
    df_vwap = Kraken.get_df_vwap(df_trades, frame)
    common_chart_figure = {
        "data": [
            {
                "x": df_trades["time"].apply(lambda x: k.unixtime_to_datetime(x)),
                "y": df_trades["price"],
                "type": "lines",
                "name": "price",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            }, {
                "x": df_vwap['dtime'],
                "y": df_vwap["vwap"],
                "type": "lines",
                "name": "vwap",
                "marker": {'color': '#FF851B'}
            },
        ],
        "layout": {
            "title": {
                "text": "Cotizaciones para el par " + asset1 + '/' + asset2,
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    return common_chart_figure


if __name__ == "__main__":
    app.run_server(debug=True)
