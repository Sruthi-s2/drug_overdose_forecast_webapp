from flask import Blueprint, jsonify
from services.overdose_service import retrieve_records

predict_routes = Blueprint('predict_routes', __name__)

@predict_routes.route('/api/predict', methods=['GET'])
def get_overdose_predictions():
    data = retrieve_records()
    return jsonify(data)
