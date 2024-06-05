from hikoky.scrapers.urls import add_latest_chapters, add_chapter_link, add_link_manga
from hikoky.scrapers.PyProbe.PyParse import pyparse

from bs4 import BeautifulSoup
import re

def home_3asq(soup):
    
    manga_data_list = process_boxes(soup)
    next_page_url = extract_next_page_url(soup)
    
    return manga_data_list, next_page_url

def process_boxes(soup):
    manga_items = soup.find_all('div', class_='page-item-detail manga')
    results = []
    for manga_item in manga_items:
        
        manga_cover, manga_link, manga_name, translation_team = extract_manga_data(manga_item)
        manga_path = add_link_manga(manga_name, manga_link, source="3asq")
        chapters_info = process_chapters(manga_item, manga_name)
        
        results.append({
            "manga_name": manga_name,
            "manga_link": manga_path,
            "manga_cover": manga_cover,
            "translation_team": translation_team,
            "chapters_info": chapters_info
        })
    return results
    
def extract_manga_data(soup):
    manga_div = soup.find('div', class_='item-thumb hover-details c-image-hover')
    
    translation_team_tag = soup.find('span', class_='manga-title-badges')
    translation_team = translation_team_tag.text.strip() if translation_team_tag else None
    
    manga_name = manga_div.find('a')['title']
    manga_link = manga_div.find('a')['href']
    manga_cover = manga_div.find('img')['src']
    
    
    return manga_cover, manga_link, manga_name, translation_team


def process_chapters(soup, manga_name):
    chapters = soup.find_all('div', class_='chapter-item')
    
    if len(chapters) > 0:
        latest_chapter = chapters[0]
        latest_chapter_url = latest_chapter.find('a')['href']
        
        latest_chapter = latest_chapter.find('a').text.strip()
        latest_chapter_number = extract_chapter_number(latest_chapter)
        
        add_latest_chapters(manga_name, latest_chapter, latest_chapter_url, source="3asq")
        
    else:
        latest_chapter_number = None
        latest_chapter_url = None
    
    if len(chapters) > 1:
        penultimate_chapter = chapters[1]
        penultimate_chapter_url = penultimate_chapter.find('a')['href']
        
        penultimate_chapter = penultimate_chapter.find('a').text.strip()
        penultimate_chapter_number = extract_chapter_number(penultimate_chapter)
        
        add_latest_chapters(manga_name, penultimate_chapter, penultimate_chapter_url, source="3asq")
    else:
        penultimate_chapter_number = None
        penultimate_chapter_url = None
        
    
    return {
        "latest_chapter_number": latest_chapter_number,
        "penultimate_chapter_number": penultimate_chapter_number,
        "latest_chapter_url": latest_chapter_number,
        "penultimate_chapter_url": penultimate_chapter_number
    }
    
def extract_next_page_url(soup):
    
    div_tag = soup.find('div', class_='nav-previous float-left')
    a_tag = div_tag.find('a') if div_tag else None
    return a_tag['href'] if a_tag else None

def extract_chapter_number(text):
    match = re.match(r'^\D*(\d+)', text)
    if match:
        return match.group(1)
    else:
        return text

# ======================
def manga_3asq(soup):
    
    info_manga, manga_name = infomanga(soup)
    chapters = info_chapters(soup, manga_name)
    
    return info_manga, chapters, None
    
def infomanga(soup):
   
    manga_name = soup.find("div", class_="post-title").find("h1").text.strip()
    review_text = soup.find('div', class_='manga-excerpt')
    if review_text:
        review_text = review_text.p.get_text(strip=True)
    else:
        review_text = 'محد مهتم يكتب قصة'
    genres = [a.get_text(strip=True) for a in soup.find('div', class_='genres-content').find_all('a')]
    cover_manga = soup.find('div', class_='summary_image').find('img')['src']
    
    info_manga = {
        "manganame": manga_name,
        "cover_manga": cover_manga,
        "genres": genres,
        "review_text": review_text,
    }
        
    return info_manga, manga_name
    
    
def info_chapters(soup, manga_name):
    chapters = []
    for ul in soup.select('.listing-chapters_wrap'):
        for li in ul.find_all('li', class_='wp-manga-chapter'):
            a_tag = li.find('a')
            chapter_url = a_tag['href']
            chapter_title = a_tag.text.strip()
            add_chapter_link(manga_name, chapter_title, chapter_url, source="3asq")
            chapters.append({"number": chapter_title})
    return chapters
   
def chapter_3asq(soup , url):
    
    image_urls = []
    for img_tag in soup.select('.page-break img.wp-manga-chapter-img'):
        image_url = img_tag['src'].strip()
        image_urls.append(image_url)
        
    active_li = soup.find('li', class_='active')
    if active_li:
        chapter_title = active_li.text.strip()
        
    
    nav_links = soup.find('div', class_='nav-links')
    if nav_links:
        
        try:
            prev_link_tag = soup.find('a', class_="btn prev_page")
            prev_link = prev_link_tag['href']
            prev_chapter_path = get_path(prev_link)
        except (TypeError, KeyError):
            prev_chapter_path = None
        
        try:
            next_link_tag = soup.find('a', class_='btn next_page')
            next_link = next_link_tag['href']
            next_chapter_path = get_path(next_link)
        except (TypeError, KeyError):
            next_chapter_path = None

    return {
        "image_urls": image_urls,
        "title": chapter_title,
        "next_chapter_link": next_chapter_path,
        "prev_chapter_link": prev_chapter_path
    }
    
def get_path(url):
    if url:
        return url.split('/')[-2]
    else:
        return None 