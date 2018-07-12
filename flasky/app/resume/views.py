from flask import render_template
from . import resume


@resume.route('/resume/')
def resume():
    return render_template('resume.html')
