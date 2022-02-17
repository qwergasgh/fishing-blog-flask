from config import BaseConfig
from flask import Flask



app = Flask(__name__)
app.config.from_object(BaseConfig)

from .views import blueprint_app
app.register_blueprint(blueprint_app)