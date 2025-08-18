import os
import re
from moviepy.editor import VideoFileClip, TextClip, ImageClip, CompositeVideoClip, AudioFileClip, ColorClip, concatenate_videoclips
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
from moviepy.audio.AudioClip import CompositeAudioClip

# Directorios de los archivos generados
VIDEOS_DIR = "/home/arivera/ciberaldia_sh/videos"
OUTPUT_DIR = "/home/arivera/ciberaldia_sh/output"
SCRIPTS_DIR = "/home/arivera/ciberaldia_sh/scripts"
IMAGES_DIR = "/home/arivera/ciberaldia_sh/images"
AUDIO_DIR = "/home/arivera/ciberaldia_sh/audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_title_and_description(script_path):
    """Extrae el título y la descripción de la noticia desde el archivo de script."""
    with open(script_path, "r", encoding="utf-8") as file:
        content = file.read()
    
    match = re.search(r"\*\*(.*?)\*\*(.*)", content, re.DOTALL)
    if match:
        title = match.group(1).strip()
        description = match.group(2).strip()
    else:
        title = "Título no disponible"
        description = "Descripción no disponible"
    
    return title, description

def create_news_video(news_number):
    """Crea un video para una noticia específica con el formato visual requerido."""
    
    script_path = os.path.join(SCRIPTS_DIR, f"noticia_{news_number}.txt")
    image_path = os.path.join(IMAGES_DIR, f"noticia_{news_number}.png")
    audio_path = os.path.join(AUDIO_DIR, f"noticia_{news_number}.mp3")
    background_audio_path = os.path.join(AUDIO_DIR, "Missing_Persons_Jeremy_Blake.mp3")
    
    if not os.path.exists(script_path) or not os.path.exists(image_path) or not os.path.exists(audio_path):
        print(f"❌ No se encontraron archivos para la noticia {news_number}. Verifica los directorios.")
        return
    
    title, description = extract_title_and_description(script_path)
    
    # Cargar imagen de fondo
    news_image = ImageClip(image_path).set_duration(10).set_fps(30)
    
    # Ajustar dimensiones de los cuadros de texto con opacidad
    title_bg_width = 500
    description_bg_width = 600
    box_height = 450
    margin = 30  # Aumentar margen interno para evitar cortes en los bordes
    vertical_offset = 500  # Subir los elementos más arriba
    horizontal_offset = 50  # Mover la descripción más a la izquierda
    right_margin = 150  # Mayor margen adicional en el lado derecho para evitar cortes
    opacity = 0.9  # Opacidad para los fondos
    
    # Crear fondo del título (azul) y alinear a la izquierda con opacidad
    title_bg = ColorClip(size=(title_bg_width, box_height), color=(30, 144, 255)).set_duration(news_image.duration).set_opacity(opacity)
    title_text = TextClip(title.upper(), fontsize=45, color="white", font="Arial-Bold", method="caption", size=(title_bg_width - margin, None)).set_duration(news_image.duration)
    title_bg = title_bg.set_position((10, news_image.h - 250 - vertical_offset))
    title_text = title_text.set_position((40, news_image.h - 230 - vertical_offset))
    
    # Crear fondo de descripción (negro) y moverlo con margen derecho adicional con opacidad
    description_bg = ColorClip(size=(description_bg_width + right_margin, box_height), color=(0, 0, 0)).set_duration(news_image.duration).set_opacity(opacity)
    description_text = TextClip(description, fontsize=35, color="white", font="Arial", method="caption", size=(description_bg_width - margin - right_margin, None)).set_duration(news_image.duration)
    description_bg = description_bg.set_position((title_bg_width + 50 - horizontal_offset, news_image.h - 250 - vertical_offset))
    description_text = description_text.set_position((title_bg_width + 120 - horizontal_offset, news_image.h - 230 - vertical_offset))
    
    # Cargar audio de la noticia y fondo musical
    news_audio = AudioFileClip(audio_path)
    background_audio = AudioFileClip(background_audio_path).set_duration(news_audio.duration + 2).volumex(0.1)
    
    # Ajustar la duración del video a la del audio de fondo para que dure 2 segundos más
    video_duration = news_audio.duration - 0.3
    news_image = news_image.set_duration(video_duration)
    title_bg = title_bg.set_duration(video_duration)
    title_text = title_text.set_duration(video_duration)
    description_bg = description_bg.set_duration(video_duration)
    description_text = description_text.set_duration(video_duration)

    # Combinar audio de fondo con el audio de la noticia
    final_audio = CompositeAudioClip([news_audio, background_audio])
    
    # Combinar video con elementos visuales y audio con transiciones suaves
    news_clip = CompositeVideoClip([news_image, title_bg, title_text, description_bg, description_text])
    news_clip = news_clip.set_audio(final_audio).set_duration(video_duration)
    news_clip = fadein(news_clip, 0.5).fx(fadeout, 0.5)  # Aplicar transiciones suaves
    
    # Exportar video
    output_path = os.path.join(OUTPUT_DIR, f"noticia_{news_number}.mp4")
    news_clip.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac")
    
    print(f"✅ Video de Noticia {news_number} generado en {output_path}")

if __name__ == "__main__":
    for i in range(1, 6):  # Generar videos para las 5 noticias con transiciones
        create_news_video(i)
