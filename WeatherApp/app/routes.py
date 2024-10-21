from flask import Blueprint, jsonify, request
from WeatherApp.app.processing import calculate_daily_summary
from WeatherApp.app.alerting import check_alert_thresholds

main_bp = Blueprint('main', __name__)

@main_bp.route('/weather/summary/<city>', methods=['GET'])
def get_daily_summary(city):
    summary = calculate_daily_summary(city)
    if summary:
        return jsonify(summary)
    return jsonify({"message": "No data found"}), 404

@main_bp.route('/alerts/<city>', methods=['GET'])
def get_alerts(city):
    summary = calculate_daily_summary(city)
    if summary and check_alert_thresholds(summary):
        return jsonify({'alerts': [f"Temperature in {city} exceeded threshold!"]})
    return jsonify({'alerts': []})

@main_bp.route('/set_threshold', methods=['POST'])
def set_threshold():
    data = request.get_json()
    threshold = data.get('threshold', 35)
    app.config['TEMP_THRESHOLD'] = threshold
    return jsonify({'message': f'Threshold set to {threshold}°C'}), 200
