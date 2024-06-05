# hikoky/blueprints/utils.py
from flask import Blueprint, render_template, request, flash, jsonify, url_for, redirect
from config import source_handlers
from hikoky.scrapers.PyProbe.PyParse import pyparse
from hikoky.scrapers.urls import get_link_manga, get_chapter_link, load_chapter, save_chapter

def get_handler_and_check_errors(source):
    handler = source_handlers.get(source)
    if not handler:
        flash("المصدر غير متوفر", 'danger')
        return None, redirect(url_for('main.sources'))
    return handler, None
    
def home_handler(url, handler, app_name, source):
    url = request.args.get('next_page_url') or handler["url"]
    
    result = pyparse(url) 
    if isinstance(result, dict) and 'error' in result:
        flash(result['error'], 'danger')
        return render_template('home.html', app_name=app_name, current_source=source)
        
    results, next_page_url = handler["home_page"](result)
    
    if request.args.get('next_page_url'):
        return jsonify(results=results, next_page_url=next_page_url)

    return render_template('home.html', results=results, next_page_url=next_page_url, app_name=app_name, current_source=source)
    
def manga_handler(handler, source, manga_path, app_name, more=False, url=None):
    if more is False:
        url = get_link_manga(manga_path, source=source) 

    result = pyparse(url) 
    if isinstance(result, dict) and 'error' in result:
        flash(result['error'], 'danger')
        return render_template('manga.html', info_manga=None, app_name=app_name, current_source=source)
    
    info_manga, chapters, next_page_link = handler["manga_page"](result)
    if more:
        return jsonify(chapters=chapters, next_page_link=next_page_link)
    else:
        return render_template('manga.html', info_manga=info_manga, chapters=chapters, next_page_link=next_page_link, app_name=app_name, current_source=source)


def chapter_handler(handler, manga_path, chapter_num, source, app_name):
    url = get_chapter_link(manga_path, chapter_num, source=source)
    
    result = load_chapter(url, source=source)
    if result:
        return render_template('chapter.html', manga_info=result, app_name=app_name, current_source=source)
    else:
        result = pyparse(url) 
        if isinstance(result, dict) and 'error' in result:
            flash(result['error'], 'danger')
            return render_template('chapter.html')
        result = handler["chapter_page"](result, url)
            
    save_chapter(result, url, source=source)
    return render_template('chapter.html', manga_info=result, app_name=app_name, current_source=source)
