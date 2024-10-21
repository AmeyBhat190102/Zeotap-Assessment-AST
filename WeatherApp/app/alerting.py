from flask import current_app

def check_alert_thresholds(summary):
    threshold = current_app.config.get('TEMP_THRESHOLD', 35)
    return summary['max_temp'] > threshold
