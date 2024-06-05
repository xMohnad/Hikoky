from flask import Blueprint, render_template, flash, redirect, url_for
from config import source_handlers
from hikoky.blueprints.utils import get_handler_and_check_errors, chapter_handler

chapter = Blueprint('chapter', __name__)

app_name = "Hikoky"  

@chapter.route('/<source>/<manga_path>/<chapter_num>')
@chapter.route('/<source>/<manga_path>/<chapter_num>/')
def display_manga(source, manga_path, chapter_num):
    handler, error_response = get_handler_and_check_errors(source)
    if error_response:
        return error_response
    
    return chapter_handler(handler, manga_path, chapter_num, source, app_name)
