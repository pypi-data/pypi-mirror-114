from . import aristoteDash
import dash, dash_core_components as dcc, dash_html_components as html, dash_bootstrap_components as dbc
import dorianUtils.dccExtendedD as dccExt
from multiprocessing import Process, Queue, current_process,Pool

dccE= dccExt.DccExtended()
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],title='aristote',
                                                        url_base_pathname = '/aristote/')
powerTab   = aristoteDash.PowerTab(app,)
energyTab  = aristoteDash.EnergyTab(app,)
titleHTML  = html.H1('Aristote V1.1')
tabsLayout = dccE.createTabs([powerTab,energyTab])
app.layout = html.Div([html.Div(titleHTML),html.Div(tabsLayout)])
app.run_server(port = 65002,debug=True,host='0.0.0.0',use_reloader=True)
