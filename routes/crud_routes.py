# routes/crud_routes.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from services.overdose_service import fetch_records, get_filter_options

crud_routes = Blueprint('crud_routes', __name__)

@crud_routes.route('/api/records', methods=['GET'])
def get_records():
    year = request.args.get('year')
    month = request.args.get('month')
    state = request.args.get('state')
    indicator = request.args.get('indicator')
    try:
        limit = int(request.args.get('limit', 8))
    except ValueError:
        limit = 8  

    filters = {
        "year": int(year) if year else None,
        "month": month,
        "state": state,
        "indicator": indicator,
        "limit": limit
    }
    records = fetch_records(filters)
    return jsonify(records)


@crud_routes.route('/api/filter-options', methods=['GET'])
def filter_options():
    options = get_filter_options()
    return jsonify(options)

