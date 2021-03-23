from flask import Blueprint, render_template
import os

blueprint_default = Blueprint('blueprint_default', __name__)

@blueprint_default.route('/', methods=('GET', 'POST'))
def index():
    context = {
        'example': 'teste value.'
    }
    return render_template("index.html", context=context)
