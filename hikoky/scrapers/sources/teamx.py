# hikoky/scrapers/Sources/teamx.py

from hikoky.scrapers.urls import add_latest_chapters, add_chapter_link, add_link_manga
from hikoky.scrapers.PyProbe.PyParse import pyparse
from bs4 import BeautifulSoup
import re
import logging

def home_teamx(soup):
    boxes = soup.find_all("div", class_="box")
    box_results = process_boxes(boxes)
    next_page_url = extract_next_page_url(soup)
    
    return box_results, next_page_url

def process_boxes(boxes):
    results = []
    for box in boxes:
        manga_name, manga_link, manga_cover = extract_manga_info(box)
        chapters_info = process_chapters(box, manga_link, manga_name)
        manga_path = add_link_manga(manga_name, manga_link, source="teamx")
        results.append({
            "manga_name": manga_name,
            "manga_link": manga_path,
            "manga_cover": manga_cover,
            "chapters_info": chapters_info
        })
    return results

def extract_manga_info(box):
    img_div = box.find("div", class_="imgu")
    manga_name = img_div.find("img")["alt"]
    manga_link = img_div.find("a")["href"]
    manga_cover = img_div.find("img")["src"]
    return manga_name, manga_link, manga_cover

def process_chapters(box, manga_link, manga_name):
    info_div = box.find("div", class_="info")
    chapter_list = info_div.find_all("a")
    
    latest_chapter_number = extract_chapter_number(chapter_list, 1)
    latest_chapter_url = f"{manga_link}/{latest_chapter_number}"
    add_latest_chapters(manga_name, latest_chapter_number, latest_chapter_url, source="teamx")
    
    penultimate_chapter_number = extract_chapter_number(chapter_list, 2)
    penultimate_chapter_url = f"{manga_link}/{penultimate_chapter_number}"
    add_latest_chapters(manga_name, penultimate_chapter_number, penultimate_chapter_url, source="teamx")
    
    return {
        "latest_chapter_number": latest_chapter_number,
        "penultimate_chapter_number": penultimate_chapter_number,
        "latest_chapter_url": latest_chapter_number,
        "penultimate_chapter_url": penultimate_chapter_number
    }

def extract_chapter_number(chapter_list, index):
    if len(chapter_list) > index:
        return chapter_list[index].text.strip().split()[-1]
    return None

def extract_next_page_url(soup):
    next_page = soup.find("a", rel="next")
    return next_page["href"] if next_page else None

# =========================
def manga_teamx(soup):
    
    soup = soup.find('div', class_="container")
    
    info_manga, manganame = infomanga(soup)
    chapters = info_chapters(soup, manganame)
    next_page_link = get_next_page_url(soup)
    return info_manga, chapters, next_page_link

def infomanga(soup):
    cover_manga = soup.find('img', class_="shadow-sm")['src']
    infobox = soup.find_all("div",  class_="whitebox")[1]
    manganame = infobox.find('div', class_="author-info-title").find("h1").text.strip()
    
    genres = infobox.find('div', class_="review-author-info")
    genres = [a.get_text(strip=True) for a in genres.find_all('a', class_='subtitle')]
    
    review_text = infobox.find('div', class_='review-content').p.get_text(strip=True)
    chapter_text = soup.find('a', class_='nav-link').text
    chapter_number = ''.join(filter(str.isdigit, chapter_text))
    
    info_manga = {
        "manganame": manganame,
        "cover_manga": cover_manga,
        "genres": genres,
        "review_text": review_text,
        "chapter_number": chapter_number
    }
        
    return info_manga, manganame

def info_chapters(soup, manga_name):
    chapter_urls = soup.find('div', class_="eplister").find('ul')
    chapters = []
    for chapter_item in chapter_urls.find_all('li'):
        all_info = chapter_item.find('a')
        chapter_url = all_info['href']
        
        num_chapter = all_info.find_all('div', class_="epl-num")[1]
        chapter_number = num_chapter.text.strip().split()[1]
        
        add_chapter_link(manga_name, chapter_number, chapter_url, source="teamx")
        chapters.append({"number": chapter_number})
    return chapters

def get_next_page_url(soup):
    next_link = soup.find('a', rel='next')
    if next_link and next_link.has_attr('href'):
        return next_link['href']
    return None

# ========================
def chapter_teamx(soup, url):
    
    reader_area = soup.find_all('div', class_="page-break")
    image_urls = [img.get("src") for div in reader_area for img in div.find_all("img") if img.get("src")]
    if not image_urls:
        logging.error("Images not found.")

    title_element = soup.find("h1", id="chapter-heading")
    title = title_element.text.strip() if title_element else "Title not found"
    chapter_number = get_num(url)
    full_title = f"{title} | الفصل {chapter_number}"

    next_chapter_link, prev_chapter_link = extract_chapter_links(soup)

    info_chapter = {
        "image_urls": image_urls,
        "title": full_title,
        "next_chapter_link": next_chapter_link,
        "prev_chapter_link": prev_chapter_link
    }
    
    return info_chapter

def get_num(url):
    match = re.search(r'(?<=\/)\d+(\.\d+)?', url)
    return match.group() if match else "Number not found"

def extract_chapter_links(soup):
    next_chapter_link = None
    prev_chapter_link = None

    container = soup.find('div', class_="container")
    if container:
        next_chapter_element = container.find('a', id='next-chapter')
        if next_chapter_element and next_chapter_element['href'] != "#":
            next_chapter_link = get_num(next_chapter_element['href'])
        else:
            logging.info("Next chapter link is not available")

        prev_chapter_element = container.find('a', id='prev-chapter')
        if prev_chapter_element and prev_chapter_element['href'] != "#":
            prev_chapter_link = get_num(prev_chapter_element['href'])
        else:
            logging.info("Previous chapter link is not available")
    
    return next_chapter_link, prev_chapter_link
