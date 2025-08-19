import os
import json
import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from config import DAYS_OFFSET  # Importamos el valor desde config.py


# Directorio de almacenamiento
BASE_DIR = "/home/arivera/engish_ciberaldia_sh/news_archive"
os.makedirs(BASE_DIR, exist_ok=True)

# Lista de fuentes RSS
RSS_SOURCES = [
    {"name": "The Hacker News", "url": "https://feeds.feedburner.com/TheHackersNews"},
    {"name": "Bleeping Computer", "url": "https://www.bleepingcomputer.com/feed/"},
    {"name": "Dark Reading", "url": "https://www.darkreading.com/rss.xml"},
    {"name": "We Live Security", "url": "https://www.welivesecurity.com/en/rss/feed/"},
    {"name": "Krebs on Security", "url": "https://krebsonsecurity.com/feed/"},
    {"name": "SecurityWeek", "url": "https://feeds.feedburner.com/securityweek"},
    {"name": "Daily Dark Web", "url": "https://dailydarkweb.net/feed/"},
    {"name": "El Espectador", "url": "https://www.elespectador.com/rss/tecnologia/"},
    {"name": "CyberNews", "url": "https://cybernews.com/feed/"},
    {"name": "CyberCultural", "url": "https://cybercultural.com/feed/"},
    {"name": "APNIC Blog", "url": "https://blog.apnic.net/feed/"},
    {"name": "Reuters", "url": "https://www.reutersagency.com/feed/"}
]

def extract_published_date(entry):
    """Extrae la fecha de publicación de una entrada RSS."""
    if hasattr(entry, 'published_parsed'):
        return datetime(*entry.published_parsed[:6]).strftime('%Y-%m-%d')
    elif hasattr(entry, 'updated_parsed'):
        return datetime(*entry.updated_parsed[:6]).strftime('%Y-%m-%d')
    else:
        return datetime.today().strftime('%Y-%m-%d')

def extract_full_article(link, source):
    """Extrae el contenido completo de un artículo basado en su fuente."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        response = requests.get(link, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Error fetching article: {e}"
    
    soup = BeautifulSoup(response.content, 'html.parser')
    print(f"Extracting from {source} - {link}")
    
    selectors = {
        "The Hacker News": 'div.articlebody.clear',
        "Bleeping Computer": 'div.articleBody',
        "Dark Reading": 'div.content',
        "We Live Security": 'div.single-post-content',
        "Krebs on Security": 'div.post-content',
        "SecurityWeek": 'div.content',
        "Daily Dark Web": 'div.entry-content'
    }
    
    article = soup.select_one(selectors.get(source, ''))
    
    if article:
        return article.get_text(separator='\n', strip=True)
    else:
        paragraphs = soup.find_all('p')
        full_article = "\n".join([para.get_text() for para in paragraphs])
        return full_article if full_article else "Full article not available."

def extract_news_from_rss(source):
    """Extrae noticias de una fuente RSS específica."""
    feed = feedparser.parse(source["url"])
    news_list = []
    today = (datetime.today() - timedelta(days=DAYS_OFFSET)).strftime('%Y-%m-%d')  

    for entry in feed.entries:
        try:
            published_date = extract_published_date(entry)
            if published_date == today:
                summary = entry.summary if 'summary' in entry else 'No summary available'
                full_article = extract_full_article(entry.link, source["name"])  
                
                news_list.append({
                    'Title': entry.title,
                    'Link': entry.link,
                    'Summary': summary,
                    'Date': published_date,
                    'Content': full_article
                })
        except Exception as e:
            print(f"Error processing entry from {source['name']}: {e}")
    return news_list

def save_news_to_file(news_list):
    """Guarda las noticias en un archivo JSON organizado por fecha."""
    now = datetime.now()
    year, month, day, hour_minute = now.strftime('%Y %m %d %H%M').split()
    
    year_dir = os.path.join(BASE_DIR, year)
    month_dir = os.path.join(year_dir, month)
    os.makedirs(month_dir, exist_ok=True)
    
    filename = f'news_{year}_{month}_{day}_{hour_minute}.json'
    filepath = os.path.join(month_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(news_list, file, ensure_ascii=False, indent=4)
    
    print(f"✅ Noticias guardadas en {filepath}")

def main():
    """Ejecuta el flujo completo de extracción, scraping y almacenamiento de noticias."""
    all_news = []
    
    for source in RSS_SOURCES:
        print(f"🔍 Extrayendo noticias de {source['name']}")
        news_list = extract_news_from_rss(source)
        all_news.extend(news_list)
    
    if all_news:
        save_news_to_file(all_news)
        print("✅ Extracción y almacenamiento de noticias completados.")
    else:
        print("⚠️ No se encontraron noticias relevantes para el día de hoy.")

if __name__ == "__main__":
    main()
