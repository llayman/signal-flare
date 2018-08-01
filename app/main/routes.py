from flask import render_template, jsonify

from app.main import bp
from app.models import Report
from app import db


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])

def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]

    reports = Report.query.all()
    items = [item.to_dict() for item in reports]
    # data = {
    #     'items': [item.to_dict() for item in reports],
    #     '_meta': {
    #         'total_items': len(reports)
    #     }
    # }

    return render_template('index.html', title='Home', user=user, posts=posts, reports=items)


