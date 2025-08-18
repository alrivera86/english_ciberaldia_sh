import os
import json
import requests
from openai import OpenAI
from datetime import datetime

# Configuración de la API de OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Carpeta donde se guardarán las imágenes
IMAGES_DIR = "/home/arivera/ciberaldia_sh/images"
os.makedirs(IMAGES_DIR, exist_ok=True)

def get_latest_news_file():
    """Encuentra el archivo JSON más reciente con noticias."""
    news_dir = "/home/arivera/ciberaldia_sh/news_archive"
    latest_file = None
    latest_time = None

    for year in os.listdir(news_dir):
        year_path = os.path.join(news_dir, year)
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

def generate_image(news_item, index):
    """Genera una imagen basada en la noticia usando DALL·E."""
    prompt = f"""Situation
		En el contexto actual de crecientes amenazas digitales, se requiere crear una representación visual impactante que capture la esencia de una noticia relacionada con ciberseguridad, comunicando de manera inmediata y efectiva los riesgos y desafíos tecnológicos.

		Task
		Generar una imagen hiperrealista que ilustre un concepto de ciberseguridad, transformando el título y resumen de la noticia en un elemento visual directo, llamativo y explicativo.
		
		Objective
		Comunicar visualmente la complejidad y los riesgos de las amenazas cibernéticas de manera que capte instantáneamente la atención del espectador y transmita el mensaje central de la noticia.
		
		Knowledge

		Utilizar técnicas de diseño que representen conceptos abstractos de seguridad digital
		Incorporar elementos simbólicos de riesgo tecnológico
		Mantener un alto nivel de detalle y realismo
		Evitar representaciones genéricas o clichés de ciberseguridad
		Instrucciones Específicas
		
		Crea una imagen hiperrealista con alta definición
		Usa una paleta de colores que sugiera tensión y alerta
		Incorpora elementos visuales que representen vulnerabilidad digital
		Asegura que la imagen sea inmediatamente comprensible sin necesidad de explicación adicional. Basado en: {news_item['Title']}. {news_item['Summary']}
		– Style: professional concept art, cinematic, inspired by sci-fi thrillers , size="1024x1792"
		"""
    response = client.images.generate(
        model="dall-e-3",  # DALL·E 3 para imágenes de mejor calidad
        prompt=prompt,
        #size="1024x1792",
        n=1
    )

    image_url = response.data[0].url  # Obtener URL de la imagen generada
    image_filename = f"noticia_{index}.png"
    image_path = os.path.join(IMAGES_DIR, image_filename)

    # Descargar la imagen
    img_data = requests.get(image_url).content
    with open(image_path, "wb") as f:
        f.write(img_data)

    print(f"✅ Imagen generada y guardada en {image_path}")

def main():
    """Flujo principal para generar imágenes desde las noticias más recientes."""
    latest_news_file = get_latest_news_file()

    if not latest_news_file:
        print("❌ No se encontraron archivos de noticias recientes.")
        return

    print(f"📄 Usando el archivo de noticias: {latest_news_file}")
    news_data = load_news_from_file(latest_news_file)

    for index, news_item in enumerate(news_data[:5], start=1):  # Generar solo 5 imágenes
        generate_image(news_item, index)

if __name__ == "__main__":
    main()
