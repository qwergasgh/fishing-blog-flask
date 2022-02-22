from flask import Blueprint, render_template
from app import app

blueprint_app = Blueprint('blueprint_app', 
                          __name__,
                          template_folder='templates', 
                          static_folder='static')

@blueprint_app.route('/')
def home(): 
    return render_template('homepage.html')
