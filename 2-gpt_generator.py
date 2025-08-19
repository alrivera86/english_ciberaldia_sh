import os
import json
from openai import OpenAI
from datetime import datetime

# Configuración de OpenAI API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)
GPT_MODEL = "gpt-4o-mini"

# Ruta donde se guardan las noticias extraídas
NEWS_DIR = "/home/arivera/engish_ciberaldia_sh/news_archive"
SCRIPTS_DIR = "/home/arivera/engish_ciberaldia_sh/scripts"
os.makedirs(SCRIPTS_DIR, exist_ok=True)

def get_latest_news_file():
    """Encuentra el archivo JSON más reciente con noticias."""
    latest_file = None
    latest_time = None

    for year in os.listdir(NEWS_DIR):
        year_path = os.path.join(NEWS_DIR, year)
        if not os.path.isdir(year_path):
            continue

        for month in os.listdir(year_path):
            month_path = os.path.join(year_path, month)
            if not os.path.isdir(month_path):
                continue

            for file in os.listdir(month_path):
                if file.endswith(".json"):
                    file_path = os.path.join(month_path, file)
                    file_time = os.path.getmtime(file_path)

                    if latest_time is None or file_time > latest_time:
                        latest_file = file_path
                        latest_time = file_time

    return latest_file

def load_news_from_file(file_path):
    """Carga las noticias desde el archivo JSON más reciente."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_script_from_news(news_data):
    """Genera el guion basado en las 5 noticias más relevantes."""
    prompt = f"""
This GPT is specialized in generating daily summaries of the most relevant cybersecurity news in English.

It focuses on:

News that impacts financial institutions.

News relevant to the United States, the United Kingdom, and other English-speaking regions.

Content goal:

To produce concise summaries designed for TikTok-style videos, lasting between 45 seconds and 1 minute.

Adaptation to target audience:

News will be explained in simple language, avoiding complex technical jargon.

Designed for people with no background in cybersecurity.

Aimed at teenagers aged 15 and up who are curious or considering studying technology or cybersecurity.

Also targets beginner university students or people who want to enter the tech world from scratch.

Communication style:

Clear, dynamic, and direct.

Prioritizing quick understanding of why each news item matters, even for those without technical training.

Avoiding technical jargon or briefly explaining it when necessary (e.g., "A firewall is like a wall that protects networks").

Mission:

To educate and inspire a new generation interested in cybersecurity.

Raise awareness about real threats in a relatable and understandable way.

Encourage more young people to explore and learn about the field.

Users will provide daily news in the following format:

News title:

News description:

News date:

Is it related to the US, UK, or other English-speaking regions? (This question is mandatory)



Is it related to any financial institution? (Optional but important for prioritization)



Does it affect major tech companies or global markets? (Optional but important for prioritization)



GPT will analyze news based on the following criteria:

Priority is given to those related to the US, UK, or other English-speaking countries, and among them, to those involving financial institutions. If there is no directly related news, priority goes to those involving financial institutions or affecting major tech companies and global markets.

Each news item will be assigned a score as follows:

Related to English-speaking countries: +3 points

Related to financial institutions: +2 points

Affects global tech companies or markets: +1 point

News will be sorted by total score. In case of a tie, English-speaking region-related news is prioritized. The five highest-scoring news items will be selected for the daily summary.

The titles of each news item must be in English.

The output format must always begin with:

One. News Title. Description of the news, detailing the event in no more than 50 words.Two. News Title. Description of the news, detailing the event in no more than 50 words.Three. News Title. Description of the news, detailing the event in no more than 50 words.Four. News Title. Description of the news, detailing the event in no more than 50 words.Five. News Title. Description of the news, detailing the event in no more than 50 words.

{json.dumps(news_data[:5], ensure_ascii=False, indent=2)}  # Take the 5 most recent

REMEMBERAdaptation to target audience:

News should be explained in simple language, without complex technical terms.

Aimed at people with no cybersecurity knowledge.

Teenagers aged 15+ who are curious or considering tech/cyber careers.

Also for beginner university students or people starting from scratch in tech.

Communication style:

Clear, dynamic, and direct.

Ensuring anyone, even with no technical background, can quickly understand why the news matters.

Avoid technical jargon or explain it briefly when needed (e.g., "A firewall is like a wall that protects networks").

Return only the formatted script with the news items — no intros or closing comments, and no extra explanations.

Do NOT add: "Here is the formatted script based on the provided news."

Only return the actual news content.

Only generate summaries based on the news in the JSON input. If there is one news item, return the script for one; if two, return two — up to a maximum of five. Do NOT invent news. """
    
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=[
            {"role": "system", "content": "You are a cybersecurity expert and content creator."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    
    return response.choices[0].message.content.strip()

def save_news_scripts(script_text):
    """Guarda cada noticia en archivos separados dentro de la carpeta scripts."""
    news_items = script_text.split("\n")
    news_number = 1
    
    for news in news_items:
        if news.strip():
            output_path = os.path.join(SCRIPTS_DIR, f"noticia_{news_number}.txt")
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(news.strip())
            print(f"✅ Guion guardado en {output_path}")
            news_number += 1

def main():
    latest_news_file = get_latest_news_file()
    if not latest_news_file:
        print("No se encontraron archivos de noticias recientes.")
        return
    
    print(f"Usando el archivo de noticias: {latest_news_file}")
    news_data = load_news_from_file(latest_news_file)
    script_text = generate_script_from_news(news_data)
    save_news_scripts(script_text)
    print("✅ Todos los guiones han sido generados y guardados correctamente.")

if __name__ == "__main__":
    main()
