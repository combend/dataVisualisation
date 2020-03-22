from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import requests, csv, datetime
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import DatetimeTickFormatter

app = Flask(__name__)
app.secret_key = "super secret"
bootstrap = Bootstrap(app)

@app.route('/')
@app.route('/index')
def index():
    file = "time_series_19-covid-Confirmed.csv"
    routeURL =  "http://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/" + file
    print(routeURL)
    response = requests.get(routeURL)
    if response.status_code != 200:
        print("Couldn't get data") #todo: Handle non OK response
    else:
        regionCases = {}
        data = csv.reader(response.text.strip().split('\n'))
        dates =  next(data)[4:]
        for row in data:
            if row[0]:
                regionCases[row[0]] = [int(x) for x in row[4:]]
        x = [datetime.datetime.strptime(date, '%m/%d/%y') for date in dates]
        plot = figure(plot_height=600, sizing_mode='stretch_width',
                      title="COVID-19 - Confirmed cases",
                      x_axis_label="Date", x_axis_type='datetime',
                      y_axis_label="Cases",
                      toolbar_location="above")
        plot.line(x, regionCases["New South Wales"], legend_label = "New South Wales", line_color="skyblue")
        plot.line(x, regionCases["Queensland"], legend_label="Queensland", line_color="maroon")
        plot.line(x, regionCases["Victoria"], legend_label="Victoria", line_color="silver")
        plot.line(x, regionCases["Australian Capital Territory"], legend_label="Australian Capital Territory", line_color="blue")
        plot.line(x, regionCases["Western Australia"], legend_label="Western Australia", line_color="yellow")
        plot.line(x, regionCases["Northern Territory"], legend_label="Northern Territory", line_color="black")
        plot.line(x, regionCases["Tasmania"], legend_label="Tasmania", line_color="green")
        plot.line(x, regionCases["South Australia"], legend_label="South Australia", line_color="red")
        plot.xaxis.formatter=DatetimeTickFormatter(days = "%d/%m/%y")
        script, div = components(plot)
        return render_template('index.html', script=script, div=div)

@app.route('/about')
def contact():
    return render_template('about.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


if __name__ == '__main__':
    app.run()
