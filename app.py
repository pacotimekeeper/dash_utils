from dash import Dash, dcc, html, Input, Output, State

from text_utils import join_lines, masked_pattern


app = Dash(__name__, suppress_callback_exceptions=True)

CONTENT_STYLE = {
    "maxWidth": 700,
    "margin": "2rem auto",
    "display": "flex",
    "flexDirection": "column",
    "gap": "0.5rem",
}


def home_layout():
    return html.Div(
        [
            html.H2("Welcome"),
            html.P("Pick a tool from the navigation bar to get started:"),
            html.Ul(
                [
                    html.Li(dcc.Link("Join Lines Tool", href="/join")),
                    html.Li(dcc.Link("Masked Pattern Tool", href="/pattern")),
                ]
            ),
        ],
        style=CONTENT_STYLE,
    )


def join_layout():
    return html.Div(
        [
            html.H2("Join Lines"),
            dcc.Textarea(
                id="multiline-input",
                style={"width": "100%", "height": 200},
                placeholder="Enter text with multiple lines...",
            ),
            html.Button("Join Lines", id="join-button", n_clicks=0),
            html.Div(id="result-label", style={"marginTop": "1rem", "fontWeight": "bold"}),
        ],
        style=CONTENT_STYLE,
    )


def pattern_layout():
    return html.Div(
        [
            html.H2("Masked Pattern"),
            dcc.Textarea(
                id="numbers-input",
                style={"width": "100%", "height": 200},
                placeholder="Enter equal-length strings, one per line...",
            ),
            html.Button("Build Pattern", id="pattern-button", n_clicks=0),
            html.Div(id="pattern-label", style={"marginTop": "1rem", "fontWeight": "bold"}),
        ],
        style=CONTENT_STYLE,
    )


app.layout = html.Div(
    [
        dcc.Location(id="url"),
        html.Header(
            [
                html.H1("Dash Utils", style={"margin": 0}),
                html.Nav(
                    [
                        dcc.Link("Home", href="/", style={"marginRight": "1rem"}),
                        dcc.Link("Join Lines", href="/join", style={"marginRight": "1rem"}),
                        dcc.Link("Masked Pattern", href="/pattern"),
                    ],
                    style={"marginTop": "0.5rem"},
                ),
            ],
            style={"textAlign": "center", "padding": "1rem 0"},
        ),
        html.Div(id="page-content"),
    ]
)


@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def render_page(pathname):
    if pathname == "/join":
        return join_layout()
    if pathname == "/pattern":
        return pattern_layout()
    return home_layout()


@app.callback(
    Output("result-label", "children"),
    Input("join-button", "n_clicks"),
    State("multiline-input", "value"),
    prevent_initial_call=True,
)
def update_result(_, input_value):
    text = input_value or ""
    return join_lines(text)


@app.callback(
    Output("pattern-label", "children"),
    Input("pattern-button", "n_clicks"),
    State("numbers-input", "value"),
    prevent_initial_call=True,
)
def update_pattern(_, numbers_value):
    values = [line.strip() for line in (numbers_value or "").splitlines() if line.strip()]
    if not values:
        return "Enter at least one string."

    lengths = {len(value) for value in values}
    if len(lengths) != 1:
        return "All strings must share the same length."

    try:
        return masked_pattern(values)
    except ValueError as exc:  # pragma: no cover - defensive, masked_pattern already checks empties
        return f"Error: {exc}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6023, debug=True)
    print("Server running on http://0.0.0.0:6023")
