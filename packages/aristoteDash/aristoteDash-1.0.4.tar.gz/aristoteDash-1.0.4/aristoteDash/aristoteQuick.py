from aristoteDash import aristote,aristoteDash
import importlib
import dash, dash_core_components as dcc, dash_html_components as html, dash_bootstrap_components as dbc
import dorianUtils.dccExtendedD as dccExt
from multiprocessing import Process, Queue, current_process,Pool

# importlib.reload(dccExt)
# importlib.reload(aristote)
# importlib.reload(aristoteDash)


# cfg=aristote.ConfigAristote()
# import time
# start=time.time()
# timeRange=['2019-03-25 09:00','2019-04-12 23:00']
# import plotly.express as px
# df= cfg.energy_PV_timeSeries(timeRange,freqCalc='1200s',period='1d',longitude=10,latitude=0.5)
# df= cfg.PV_timeSeries(timeRange,freqCalc='1200s',longitude=10,latitude=0.5)
# fig= cfg.plot_energy_timeSeries(timeRange,freqCalc='3600s',period='1d')
# fig.show()
# for k in [1,2,4,6,12,24,48]:
#     fig= cfg.plot_energy_timeSeries(timeRange,freqCalc='1200s',period=str(k)+'h')
#     fig.show()
# cfg.utils.printCTime(start)

dccE= dccExt.DccExtended()
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],title='aristote',
                                                        url_base_pathname = '/aristote/')
powerTab=aristoteDash.PowerTab(app,)
energyTab=aristoteDash.EnergyTab(app,)
titleHTML=html.H1('Aristote V1.1')
tabsLayout= dccE.createTabs([powerTab,energyTab])
app.layout = html.Div([html.Div(titleHTML),html.Div(tabsLayout)])
app.run_server(port = 65002,debug=True,host='0.0.0.0',use_reloader=True)
