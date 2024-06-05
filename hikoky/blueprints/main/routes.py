from flask import Blueprint, render_template, request, flash, jsonify, url_for, redirect
from config import source_handlers
from hikoky.blueprints.utils import get_handler_and_check_errors, home_handler

main = Blueprint('main', __name__)

app_name = "Hikoky"  

@main.route('/')
def sources():
    return render_template('sources.html', app_name=app_name)

@main.route('/<source>')
@main.route('/<source>/')
def home(source):
    handler, error_response = get_handler_and_check_errors(source)
    if error_response:
        return error_response
        
    return home_handler(request.args.get('next_page_url'), handler, app_name, source)

@main.route('/search/<source>/')
@main.route('/search/<source>')
def search(source):
    return "<h1>قريبا</h1>"
