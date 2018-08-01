import enum
from datetime import datetime

from app import db


class Type(enum.Enum):
    flood = "FLOOD"
    fire = "FIRE"
    other = "OTHER"


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)
    latitude = db.Column(db.Float, index=True)
    longitude = db.Column(db.Float, index=True)
    guid = db.Column(db.String(32), index=True, nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'))
    severity_id = db.Column(db.Integer, db.ForeignKey('severity.id'))

    # address

    def __repr__(self):
        return '<Report guid:{}, timestamp:{}, lat:{}, lon:{}, type:{}, severity:{}>'.format(self.guid, self.timestamp,
                                                                                             self.latitude,
                                                                                             self.longitude, self.type,
                                                                                             self.severity)

    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat() + 'Z',
            'latitude': self.latitude,
            'longitude': self.longitude,
            'type:': self.type.to_dict(),
            'severity': self.severity.to_dict(),
            'guid': self.guid
        }

    def from_dict(self, data):
        for field in ['timestamp', 'latitude', 'longitude', 'guid']:
            if field in data:
                setattr(self, field, data[field])
        if 'type' in data:
            setattr(self, 'type', Type.query.filter_by(name=data['type']).first())
        if 'severity' in data:
            setattr(self, 'severity', Severity.query.filter_by(name=data['severity']).first())

    @staticmethod
    def to_collection_dict(query):
        resources = query.all()
        data = {
            'items': [item.to_dict() for item in resources],
            '_meta': {
                'total_items': len(resources)
            }
        }
        return data


class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    description = db.Column(db.String(1024))
    reports = db.relationship('Report', backref='type', lazy=True)

    def __repr__(self):
        return '<Type name:{}'.format(self.name)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }


class Severity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    description = db.Column(db.String(1024))
    weight = db.Column(db.SmallInteger, index=True, nullable=False)
    reports = db.relationship('Report', backref='severity', lazy=True)

    def __repr__(self):
        return '<Severity name:{}, weight:{}'.format(self.name, self.weight)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'weight': self.weight
        }
