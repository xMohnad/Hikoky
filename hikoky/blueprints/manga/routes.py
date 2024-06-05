from flask import Blueprint, render_template, request, flash, redirect, url_for
from config import source_handlers
from hikoky.blueprints.utils import get_handler_and_check_errors
from hikoky.blueprints.utils import manga_handler

manga = Blueprint('manga', __name__)

app_name = "Hikoky"  

@manga.route('/<source>/<manga_path>')
@manga.route('/<source>/<manga_path>/')
def manga_home(source, manga_path):
    handler, error_response = get_handler_and_check_errors(source)
    if error_response:
        return error_response
        
    return manga_handler(handler, source, manga_path, app_name)

@manga.route('/load_more')
def load_more():
    source = request.args.get('source')
    handler, error_response = get_handler_and_check_errors(source)
    if error_response:
        return error_response
    
    url = request.args.get('nextPageUrl')
    return manga_handler(handler, source, None, None, more=True, url=url)
