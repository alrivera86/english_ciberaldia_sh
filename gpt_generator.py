import os
import json
from openai import OpenAI
from datetime import datetime

# Configuración de OpenAI API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)
GPT_MODEL = "gpt-4o-mini"

# Ruta donde se guardan las noticias extraídas
NEWS_DIR = "/home/arivera/ciberaldia_sh/news_archive"
SCRIPTS_DIR = "/home/arivera/ciberaldia_sh/scripts"
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
Este GPT se especializa en generar resúmenes diarios de las noticias más relevantes sobre ciberseguridad en español.
Se enfoca en:

Noticias que impacten a entidades financieras,

Noticias relevantes para Chile y empresas con conexiones a América Latina.

Objetivo del contenido:

Producir resúmenes concisos, diseñados para videos de TikTok, con una duración de entre 45 segundos y 1 minuto.

Adaptación al público objetivo:

Las noticias se explicarán en un lenguaje sencillo, sin tecnicismos complicados.

Están pensadas para personas que no tienen conocimientos de ciberseguridad,

Adolescentes de 15 años en adelante que son curiosos o están considerando estudiar carreras de tecnología o ciberseguridad.

También para estudiantes universitarios principiantes o personas que quieren incursionar en el mundo de la tecnología desde cero.

Estilo de comunicación:

Claro, dinámico, y directo.

Priorizando que cualquier persona, incluso sin formación técnica, entienda rápidamente por qué esa noticia importa.

Evitando jerga técnica o explicándola brevemente si es necesaria (como: "Un firewall es como una muralla que protege las redes").

Misión:

Educar e inspirar a una nueva generación de interesados en ciberseguridad.

Aumentar la conciencia sobre amenazas reales de una forma cercana y entendible.

Motivar a que más personas jóvenes se interesen en aprender más del área.
    Los usuarios proporcionarán noticias diarias en el siguiente formato:

    1. **Título de la noticia:**
    2. **Descripción de la noticia:**
    3. **Fecha de la noticia:**
    4. **¿Está relacionada con Chile?** (Esta pregunta es obligatoria)
    - [ ] Sí
    - [ ] No
    5. **¿Está relacionada con alguna entidad financiera?** (Opcional, pero importante para priorizar)
    - [ ] Sí
    - [ ] No
    6. **¿Afecta a empresas con conexiones a América Latina?** (Opcional, pero importante para priorizar)
    - [ ] Sí
    - [ ] No

    El GPT analizará las noticias según estos criterios para priorizar las relacionadas con Chile y, entre ellas, las que tengan que ver con entidades financieras. En ausencia de noticias relacionadas con Chile, se priorizarán las que estén relacionadas con entidades financieras o afecten a empresas con conexiones a América Latina.

    Para manejar las prioridades, se asignará una puntuación a cada noticia de la siguiente manera:
    - Relacionada con Chile: +3 puntos.
    - Relacionada con entidades financieras: +2 puntos.
    - Afecta a empresas con conexiones a América Latina: +1 punto.

    Las noticias se ordenarán según su puntuación total. En caso de empate, se priorizarán las noticias relacionadas con Chile. Las cinco noticias con la mayor puntuación serán seleccionadas para el resumen diario.
    Los titulos de cada noticia tiene que ser en Español
    
    El formato de salida siempre debe comenzar con:

    "Uno. **Título de la noticia.** Descripción de la noticia, detallando el evento en un máximo de 50 palabras.
    Dos. **Título de la noticia.** Descripción de la noticia, detallando el evento en un máximo de 50 palabras.
    Tres. **Título de la noticia.** Descripción de la noticia, detallando el evento en un máximo de 50 palabras.
    Cuatro. **Título de la noticia.** Descripción de la noticia, detallando el evento en un máximo de 50 palabras.
    Cinco. **Título de la noticia.** Descripción de la noticia, detallando el evento en un máximo de 50 palabras."

    {json.dumps(news_data[:5], ensure_ascii=False, indent=2)}  # Tomamos las 5 más recientes

RECUERDA
Adaptación al público objetivo:

Las noticias se explicarán en un lenguaje sencillo, sin tecnicismos complicados.

Están pensadas para personas que no tienen conocimientos de ciberseguridad,

Adolescentes de 15 años en adelante que son curiosos o están considerando estudiar carreras de tecnología o ciberseguridad.

También para estudiantes universitarios principiantes o personas que quieren incursionar en el mundo de la tecnología desde cero.

Estilo de comunicación:

Claro, dinámico, y directo.

Priorizando que cualquier persona, incluso sin formación técnica, entienda rápidamente por qué esa noticia importa.

Evitando jerga técnica o explicándola brevemente si es necesaria (como: "Un firewall es como una muralla que protege las redes").
    Devuelve solo el guion formateado sin intro ni cierre solo las notiicas, sin explicaciones adicionales.
    no agergues Aquí está el guión formateado basado en las noticias proporcionadas:    
    Solo va a dar las noticias que estan en el json no puede inventar noticias, si es una solo le das el guion de una si soni	 dos solo el guin de dos o si son tres guion de 3 o 4 igual o maximo 5, pero puedes inventar noticias"""
    
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=[
            {"role": "system", "content": "Eres un experto en ciberseguridad y generador de contenido."},
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
