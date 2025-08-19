import os
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
from datetime import datetime, timedelta
from config import DAYS_OFFSET  # Importamos el valor desde config.py
import time  # <-- Importa time para hacer una pausa




# Directorios de los archivos generados
VIDEOS_DIR = "/home/arivera/english_ciberaldia_sh/videos"
OUTPUT_DIR = "/home/arivera/english_ciberaldia_sh/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_intro():
    """Crea el video de introducción con la fecha dinámica."""
    
    # Cargar video de introducción
    intro_video = VideoFileClip(os.path.join(VIDEOS_DIR, "Base_INTRO_CON_VOZ_CiberAldia.mp4"))
    
    # Generar fecha dinámica en español
    import locale
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    # Hora como se mostraba inicialmente
    #today_date = datetime.now().strftime("%d de %B de %Y")
    # Hora restando los dias necesarios
    today_date = (datetime.today() - timedelta(days=DAYS_OFFSET)).strftime("%d de %B de %Y")
    
    
    
    
    #today = (datetime.today() - timedelta(days=0)).strftime('%Y-%m-%d')  

    # Crear el texto de la fecha con efecto de entrada y salida
    date_text = TextClip(today_date, fontsize=80, color="white", font="Arial-Bold")
    date_text = date_text.set_position(("center", 1100)).set_duration(intro_video.duration)
    date_text = fadein(date_text, 2).fx(fadeout, 0)  # Efecto de entrada y salida
    
    # Combinar el video con la fecha
    intro_with_text = CompositeVideoClip([intro_video, date_text])

    # 📸 Guardar captura del segundo 4 directamente desde intro_with_text
    screenshot_path = os.path.join(OUTPUT_DIR, "captura_segundo_4_INTRO.png")
    intro_with_text.save_frame(screenshot_path, t=3)
    
    # Guardar el video de introducción
    output_path = os.path.join(OUTPUT_DIR, "intro_video.mp4")
    intro_with_text.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac")

    # ⚡ Cerrar el video anterior
    intro_video.close()
    intro_with_text.close()



    print(f"✅ Video de introducción generado en {output_path}")
    print(f"✅ Captura del segundo 4 guardada en {screenshot_path}")


if __name__ == "__main__":
    create_intro()
