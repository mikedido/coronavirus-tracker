from . import api
from . import views
from .api import version0
from .api import version1
from app import app

app.register_blueprint(version0)
app.register_blueprint(version1)