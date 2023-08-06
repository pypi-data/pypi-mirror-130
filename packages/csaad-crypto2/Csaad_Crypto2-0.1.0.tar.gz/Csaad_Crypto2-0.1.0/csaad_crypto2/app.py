import dash
from dash.dependencies import Output, Input
from dash import dcc, html
import pandas as pd
import numpy as np
import krakenex as knx
from datetime import date, datetime

# initializing krakenex API
k = knx.API()


class App:
    # App class initializer
    # argument1 title = title of page
    # argument2 stylesheet = external stylesheets of page
    def __init__(self, title, stylesheet):
        self.app = dash.Dash(__name__, external_stylesheets=stylesheet)
        self.app.title = title
        self.setPairs()  # getting all tradeable pairs from kraken
        self.setIntervals()  # setting usable intervals
        self.setLayout()  # setting layout of app page
        # callback for update chart
        self.app.callback(Output("price-chart", "figure"),
                          [
                              Input("crypto-filter", "value"),
                              Input("time-intervals", "value"),
                              Input("date-selection", "date")
                          ]
                          )(self.update_chart)

    # app runner
    def run(self, debug=True):
        self.app.run_server(debug=debug)

    # getting all tradable pairs from kraken and setting
    def setPairs(self):
        try:
            assetPairsRes = k.query_public("AssetPairs")
            assetPairs = assetPairsRes["result"].values()
            res = [(x['altname'], x['wsname']) for x in assetPairs]
            self.pairs = res
        except:
            print("Error while setting pairs")

    # setting all usable interval for API
    def setIntervals(self):
        self.intervals = [(1, "1 Minute"),
                          (5, "5 Minute"),
                          (15, "15 Minute"),
                          (30, "30 Minute"),
                          (60, "1 hour"),
                          (240, "4 hours"),
                          (1440, "1 day"),
                          (10080, "7 days"),
                          (21600, "15 days")]

    # setting API page layout using dash
    def setLayout(self):
        self.app.layout = html.Div(
            children=[
                html.Div(
                    children=[
                        html.P(children="📈", className="header-emoji"),
                        html.H1(children="Cryptocurrency Price", className="header-title"),
                        html.P(children=["Graph of the prices of cryptocurrency", html.Br(),
                                         "", html.A("", href="https://www.kraken.com/", target="_blank")],
                               className="header-description")
                    ], className="header"
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.Div(children="Cryptomoney", className="menu-title"),
                                dcc.Dropdown(
                                    id="crypto-filter",
                                    options=[
                                        {"label": y, "value": x} for x, y in self.pairs
                                    ],
                                    value="ETH/USDC",
                                    clearable=False,
                                    className="dropdown"
                                )
                            ]
                        ),
                        html.Div(
                            children=[
                                html.Div(children="Interval", className="menu-title"),
                                dcc.Dropdown(
                                    id="time-intervals",
                                    options=[
                                        {"label": y, "value": x} for x, y in self.intervals
                                    ],
                                    value="60",
                                    clearable=False,
                                    className="dropdown"
                                )
                            ]
                        ),
                        html.Div(
                            children=[
                                html.Div(children="Date", className="menu-title"),
                                dcc.DatePickerSingle(
                                    id="date-selection",
                                    min_date_allowed=date(2021, 1, 1),
                                    max_date_allowed=date.today(),
                                    initial_visible_month=date.today(),
                                    date=date.today()
                                )
                            ]
                        )
                    ],
                    className="menu"
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=dcc.Graph(id="price-chart", config={"displayModeBar": False}),
                            className="card"
                        )
                    ],
                    className="wrapper"
                )
            ]
        )

    # chart updater for changes in page
    # argument 1 pair = tradable pair like "1INCHEUR"
    # argument 2 interval= interval of chart
    # argument 3 since= since date of chart
    def update_chart(self, pair, interval, since):
        try:
            selectedDate = int(datetime.strptime(since, "%Y-%m-%d").timestamp())
            data = self.getCurrencyInformation(pair, interval, selectedDate)
            columns = ["Time", "Open", "High", "Low", "Close", "VWAP", "Volume", "Count"]

            chart = {}

            df = pd.DataFrame(data=data, columns=columns)
            df["Date"] = pd.to_datetime(df.Time, unit="s")

            df["Open"] = df["Open"].apply(pd.to_numeric)
            df["High"] = df["High"].apply(pd.to_numeric)
            df["Low"] = df["Low"].apply(pd.to_numeric)
            df["Close"] = df["Close"].apply(pd.to_numeric)
            df["Volume"] = df["Volume"].apply(pd.to_numeric)

            df["VWAP"] = np.cumsum(df.Volume * ((df.High + df.Low + df.Close) / 3)) / np.cumsum(df.Volume)

            chart = {
                "data": [
                    {
                        "x": df["Date"],
                        "y": df["Low"],
                        "type": "lines",
                        "name": "Low",
                        "hovertemplate": "$%{y:.2f}<extra></extra>",
                    },
                    {
                        "x": df["Date"],
                        "y": df["High"],
                        "type": "lines",
                        "name": "High",
                        "hovertemplate": "$%{y:.2f}<extra></extra>",
                    },
                    {
                        "x": df["Date"],
                        "y": df["VWAP"],
                        "type": "lines",
                        "name": "VWAP",
                        "line": {
                            "dash": 'dot',
                            "with": 6
                        },
                        "hovertemplate": "$%{y:.2f}<extra></extra>",
                    }
                ],
                "layout": {
                    "title": {
                        "text": "Evolution of Cryptocurrency Prices",
                        "x": 0.05,
                        "xanchor": "left",
                    },
                    "xaxis": {"fixedrange": True},
                    "yaxis": {"tickprefix": "$", "fixedrange": True},
                    "colorway": ["#ff0000", "#10a700", "#000000"],
                }
            }

            return chart
        except:
            print("Error while updating chart")

    # getting currency information from kraken API
    # argument 1 pair = tradable pair like "1INCHEUR"
    # argument 2 interval= interval of data
    # argument 3 since= since date of data
    def getCurrencyInformation(self, pair, interval, since):
        try:
            data = k.query_public("OHLC", {"pair": pair,
                                           "interval": interval,
                                           "since": since})
            data = data["result"]
            return data[list(data.keys())[0]]
        except:
            print("Error while getting currency information")


if __name__ == "__main__":
    stylesheet = [{
        "href": "https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet"
    }]
    title = "Page Title"
    app = App(title, stylesheet)
    app.run()
