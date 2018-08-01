from app import create_app, db
from app.models import Report, Type, Severity

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Report': Report, 'Type': Type, 'Severity': Severity}
