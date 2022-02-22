from flask import Blueprint



blueprint_user = Blueprint('blueprint_user', 
                           __name__,
                           template_folder='templates', 
                           static_folder='static')

from .views import *