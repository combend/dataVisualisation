import requests, csv, datetime


def collect_data():
    file = "time_series_covid19_confirmed_global.csv"
    routeURL = "http://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/" + file
    print(routeURL)
    response = requests.get(routeURL)
    if response.status_code != 200:
        print("Couldn't get data")  # todo: Handle non OK response
    else:
        cases = {}
        data = csv.reader(response.text.strip().split('\n'))
        dates = [datetime.datetime.strptime(date, '%m/%d/%y') for date in next(data)[4:]]
        global_cases = 0
        for row in data:
            country = row[1]
            case_history = [int(case) for case in row[4:] if case]
            global_cases += case_history[-1]
            new_state = {row[0]: {'lat': row[2], 'long': row[3], 'case_history': case_history}}
            if country in cases:
                cases[country].update(new_state)
            else:
                cases[country] = new_state
    return dates, cases, global_cases


def country_cases():
    dates, cases, global_cases = collect_data()
    country_total_cases = {}
    for country in cases:
        total = 0
        for state in cases[country]:
            total += cases[country][state]['case_history'][-1]
        country_total_cases[country] = total
    return country_total_cases, global_cases


def state_cases():
    dates, cases, global_cases = collect_data()
    state_total_cases = {}
    for country in cases:
        if len(cases[country]) > 1:
            for state in cases[country]:
                state_total_cases[state] = cases[country][state]
        else:
            state_total_cases[country] = cases[country]['']
    return state_total_cases
