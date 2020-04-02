from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

import dataProcessing, countryInfo
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import DatetimeTickFormatter


from math import pi
import pandas as pd
from bokeh.palettes import Turbo256
from bokeh.transform import cumsum

app = Flask(__name__)
app.secret_key = "super secret"
bootstrap = Bootstrap(app)


@app.route('/updateStates', methods=['GET', 'POST'])
def updateStates():
    if request.method == 'POST':
        return index(request.form.getlist('states'))


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index(chosen_states=[]):
    dates, cases, global_cases = dataProcessing.collect_data()
    plot = figure(plot_height=600, sizing_mode='stretch_width',
                  title="COVID-19 - Confirmed cases",
                  x_axis_label="Date", x_axis_type='datetime',
                  y_axis_label="Cases",
                  toolbar_location="above")
    for state in countryInfo.aus_states:
        if state in chosen_states:
            plot.line(dates, cases['Australia'][state]['case_history'], legend_label=state,
                      line_color=countryInfo.aus_states[state])
    plot.xaxis.formatter = DatetimeTickFormatter(days="%d/%m/%y")
    script, div = components(plot)
    states = countryInfo.aus_states.keys()
    return render_template('index.html', buttons=states, script=script, div=div)

@app.route('/globalCases')
def global_cases_summary():
    x, global_cases = dataProcessing.country_cases()

    data = pd.Series(x).reset_index(name='value').rename(columns={'index': 'country'})
    data['angle'] = data['value'] / data['value'].sum() * 2 * pi
    data['color'] = Turbo256[:len(x)]

    p = figure(plot_height=800, sizing_mode='scale_height', aspect_ratio = 2,
               title="Global confirmed cases", toolbar_location=None,
               tools="hover", tooltips="@country: @value", x_range=(-0.5, 1.0))

    p.wedge(x=0, y=1, radius=0.3,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend_field='country', source=data)

    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None
    script, div = components(p)
    return render_template('globalCases.html', script=script, div=div, global_cases = global_cases)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/heatMap')
def heatMap():
    dates, cases, global_cases = dataProcessing.collect_data()
    state_cases_info = dataProcessing.state_cases()
    print(state_cases_info)
    return render_template('heatMap.html', cases_info = state_cases_info)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


if __name__ == '__main__':
    app.run()
