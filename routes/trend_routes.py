from flask import Blueprint, render_template, session, request, redirect, url_for, jsonify
from services.overdose_service import get_filter_options
from services.db_service import db

trend_routes = Blueprint('trend_routes', __name__)

@trend_routes.route('/trends')
def show_trends():
    if 'user_id' not in session:
        return redirect(url_for('auth_routes.login_page'))

    filters = get_filter_options()
    return render_template('trends.html',
        indicators=filters['indicators'],
        years=filters['years'],
        months=filters['months'],
        states=filters['states']
    )

@trend_routes.route('/api/trend_charts')
def api_trend_charts():
    indicator = request.args.get('indicator')
    states = request.args.get('states', '').split(',')
    years = request.args.get('years', '').split(',')
    months = request.args.get('months', '').split(',')

    query = {}
    if indicator and indicator != "ALL":
        query["indicator"] = indicator
    if states and states != ['']:
        query["state.name"] = {"$in": states}
    if years and years != ['']:
        query["year"] = {"$in": list(map(int, years))}
    if months and months != ['']:
        query["month"] = {"$in": months}

    records = list(db["overdose_deaths"].find(query))

    # Grouping dicts
    total_by_year = {}
    by_state = {}
    by_drug = {}

    for r in records:
        year = r.get("year")
        state = r.get("state", {}).get("name")
        drug = r.get("indicator")
        deaths = r.get("no_of_deaths", 0)

        if year is not None:
            total_by_year[year] = total_by_year.get(year, 0) + deaths
        if state:
            by_state[state] = by_state.get(state, 0) + deaths
        if drug:
            by_drug[drug] = by_drug.get(drug, 0) + deaths

    
    sorted_years = sorted(total_by_year)
    chart1 = {
        "years": sorted_years,
        "values": [total_by_year[y] for y in sorted_years]
    }

    
    SCALE_UNIT = 100000
    bar_labels = list(by_state.keys())
    bar_raw = list(by_state.values())

    chart2 = [
        {"state": bar_labels[i], "values": [round(bar_raw[i] / SCALE_UNIT, 2)]}
        for i in range(len(bar_labels))
    ]

    
    total_deaths = sum(by_drug.values())
    chart3 = {
        "labels": list(by_drug.keys()),
        "values": [round((v / total_deaths) * 100, 2) if total_deaths else 0 for v in by_drug.values()]
    }

    return jsonify({
        "totalByYear": chart1,
        "byStateOverTime": chart2,
        "percentByDrug": chart3
    })
