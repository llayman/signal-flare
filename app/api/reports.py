import dateutil.parser
from flask import jsonify, request

from app import db
from app.api import bp
from app.models import Report
from app.api.errors import bad_request


@bp.route('/reports', methods=['POST'])
def create_report():
    data = request.get_json() or {}

    if 'guid' not in data or 'latitude' not in data or 'longitude' not in data:
        return bad_request('must include guid, latitude, and longitude fields')

    report = Report()
    report.from_dict(data)
    db.session.add(report)
    db.session.commit()
    response = jsonify(report.to_dict())
    response.status_code = 201
    return response


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
