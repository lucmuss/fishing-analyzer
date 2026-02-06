from dash import Input, Output, dcc, html

from fishing_analyzer import config
from fishing_analyzer.apps import add, distributions, environment, histograms, mainpage, statistics
from fishing_analyzer.mainapp import app

main_footer: html.Div = html.Div(
    className="container",
    children=[
        html.Footer(
            children=[
                html.P(
                    className="",
                    children=(
                        "This website was created by Lucas Mussmaecher in 2018 "
                        "- Email: lucas.mussmaecher@gmail.com"
                    ),
                ),
            ]
        )
    ],
)

main_navigation_bar: html.Div = html.Div(
    className="container mt-2",
    children=[
        html.Div(
            className="row mt-4",
            children=[
                html.Ul(
                    className="nav bg-light",
                    children=[
                        html.Li(
                            className="nav-item",
                            children=dcc.Link(
                                "Month Statistics", className="nav-link", href="/apps/statistics"
                            ),
                        ),
                        html.Li(
                            className="nav-item",
                            children=dcc.Link(
                                "Environmental Data", className="nav-link", href="/apps/environment"
                            ),
                        ),
                        html.Li(
                            className="nav-item",
                            children=dcc.Link(
                                "Histograms", className="nav-link", href="/apps/histograms"
                            ),
                        ),
                        html.Li(
                            className="nav-item",
                            children=dcc.Link(
                                "Distributions", className="nav-link", href="/apps/distributions"
                            ),
                        ),
                        html.Li(
                            className="nav-item",
                            children=dcc.Link(
                                "Add Data", className="nav-link", href="/apps/addfish"
                            ),
                        ),
                        html.Li(
                            className="nav-item",
                            children=dcc.Link("Description", className="nav-link", href="/"),
                        ),
                    ],
                )
            ],
        ),
    ],
)

layout: html.Div = html.Div(
    [
        main_navigation_bar,
        dcc.Location(id="url", refresh=False),
        html.Div(className="container clearfix mt-4 mb-4", id="page_content"),
        main_footer,
    ]
)

app.layout = layout

PAGE_MAP = {
    "/apps/environment": environment.layout,
    "/apps/statistics": statistics.layout,
    "/apps/histograms": histograms.layout,
    "/apps/distributions": distributions.layout,
    "/apps/addfish": add.layout,
}


@app.callback(Output("page_content", "children"), [Input("url", "pathname")])
def display_page(pathname: str) -> html.Div:
    return PAGE_MAP.get(pathname, mainpage.layout)


def main() -> None:
    if config.RUN_AS_PRODUCTION:
        app.run_server(host="0.0.0.0", port=8085)
    else:
        app.run_server(debug=True, port=8085)


if __name__ == "__main__":
    main()
