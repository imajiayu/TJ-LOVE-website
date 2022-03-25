from flask import render_template
from . import main

#404路由
@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('main/404.html'), 404


