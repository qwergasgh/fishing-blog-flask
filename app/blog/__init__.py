from flask import Blueprint

blueprint_blog = Blueprint('blueprint_blog',
                           __name__,
                           template_folder='templates',
                           static_folder='static')

from .views import *