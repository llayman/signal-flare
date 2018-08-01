import dateutil.parser
from flask import jsonify, request

from app.api import bp
from app.models import Report


@bp.route('/reports', methods=['POST'])
def create_report():
    pass

@bp.route('/reports', methods=['GET'])
def get_reports():
    data = request.get_json() or {}
    query = Report.query

    if 'start_time' in data:
        query = query.filter(Report.timestamp >= dateutil.parser.parse(data['start_time']))
    if 'end_time' in data:
        query = query.filter(Report.timestamp <= dateutil.parser.parse(data['end_time']))

    resources = query.all()
    data = {
        'items': [item.to_dict() for item in resources],
        '_meta': {
            'total_items': len(resources)
        }
    }
    return jsonify(data)
