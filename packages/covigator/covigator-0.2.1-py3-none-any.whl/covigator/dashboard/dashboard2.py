import dash
import dash_core_components as dcc
import dash_html_components as html
import covigator.configuration
from covigator.configuration import Configuration
from covigator.dashboard.tabs.footer import get_footer
from covigator.dashboard.tabs.overview import get_tab_overview
from covigator.dashboard.tabs.samples import get_tab_samples, set_callbacks_samples_tab
from covigator.dashboard.tabs.variants import get_tab_variants, set_callbacks_variants_tab
from covigator.database.database import session_scope, get_database
from logzero import logger
from covigator.database.queries import Queries


# loads configuration, connects and sets up the database
config = Configuration()
covigator.configuration.initialise_logs(config.logfile_dash)
database = get_database(config=config, initialize=True, verbose=True)


def get_tabs(queries: Queries):
    tab_overview = get_tab_overview(queries=queries)
    tab_samples = get_tab_samples(queries=queries)
    tab_variants = get_tab_variants(queries=queries)
    # assemble tabs in dcc.Tabs object
    # style={'margin': '0 0 0 0', 'padding-top': '2px'})
    return dcc.Tabs(
        children=[tab_overview, tab_samples, tab_variants],
        style={'height': '44px'}
    )


def serve_layout():
    logger.info("Serving layout")
    #with session_scope(database=database) as session:
    #    queries = Queries(session=session)
    footer = get_footer()
    tabs = get_tabs(queries)
    set_callbacks_variants_tab(app=app, queries=queries)
    set_callbacks_samples_tab(app=app, queries=queries)
    # , style={'margin-top': '0px', 'padding-top': '0px'})
    return html.Div(
        children=[tabs, footer]
    )


# creates the Dash application
logger.info("Create the application")
app = dash.Dash(
    name=__name__,
    title="CoVigator",
    meta_tags=[
        # A description of the app, used by e.g.
        # search engines when displaying search results.
        {
            'name': 'description',
            'content': 'CoVigator - monitoring Sars-Cov-2 mutations'
        },
        # A tag that tells Internet Explorer (IE)
        # to use the latest renderer version available
        # to that browser (e.g. Edge)
        {
            'http-equiv': 'X-UA-Compatible',
            'content': 'IE=edge'
        },
        # A tag that tells the browser not to scale
        # desktop widths to fit mobile screens.
        # Sets the width of the viewport (browser)
        # to the width of the device, and the zoom level
        # (initial scale) to 1.
        #
        # Necessary for "true" mobile support.
        {
          'name': 'viewport',
          'content': 'width=device-width, initial-scale=1.0'
        }
    ]
)
# Warning pass the layout as a function, do not call it otherwise the application will serve a static dataset
session = database.get_database_session()
queries = Queries(session=session)
app.layout = serve_layout


if __name__ == '__main__':
    app.run_server(debug=True, host=config.dash_host, port=config.dash_port)
