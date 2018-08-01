from app import db, create_app
from app.models import Report, Severity, Type

app = create_app()
app_context = app.app_context()
app_context.push()

s1 = Severity(name="high", description="you better call someboday!", weight=5)
s2 = Severity(name="low", description="not a big deal", weight=1)

t1 = Type(name="fire", description="something's burning!")
t2 = Type(name="flood", description="too much water!")

db.session.bulk_save_objects([s1, s2, t1, t2])
db.session.commit()

r1 = Report()
r1.from_dict(
    {'latitude': 34.226,
     'longitude': -77.925,
     'guid': 'askjdh12436123',
     'type': 'fire',
     'severity': 'high'})

r2 = Report()
r2.from_dict(
    {'latitude': 34.226,
     'longitude': -77.90,
     'guid': 'xyzhdgaffffffff',
     'type': 'flood',
     'severity': 'low'})

r3 = Report()
r3.from_dict(
    {'latitude': 34.24,
     'longitude': -77.94,
     'guid': 'xyzhdgaffffffff',
     'type': 'flood',
     'severity': 'high'})

r4 = Report()
r4.from_dict(
    {'latitude': 34.29,
     'longitude': -77.935,
     'guid': '4444444444444444',
     'type': 'fire',
     'severity': 'low'})

db.session.bulk_save_objects([r1, r2, r3, r4])
db.session.commit()
