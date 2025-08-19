import os
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.fx.all import fadein, fadeout
from config import DAYS_OFFSET  # ✅ Importar la configuración
import datetime
import shutil



# Calcular la fecha correcta según DAYS_OFFSET
fecha_correcta = datetime.datetime.today() - datetime.timedelta(days=DAYS_OFFSET)
fecha_formateada = fecha_correcta.strftime("%d_%m_%Y")  # Formato: DD_MM_AAAA


# Directorio donde se guardan los videos generados
OUTPUT_DIR = "/home/arivera/english_ciberaldia_sh/output"

def merge_videos():
    """Une los videos de introducción, noticias y cierre en un solo archivo final con transiciones suaves."""
    
    # Definir la ruta de cada video
    intro_path = os.path.join(OUTPUT_DIR, "intro_video.mp4")
    closing_path = os.path.join(OUTPUT_DIR, "closing_video.mp4")

    # Verificar que los archivos existen
    if not os.path.exists(intro_path) or not os.path.exists(closing_path):
        print("❌ No se encontraron los videos de introducción o cierre.")
        return

    # Cargar los videos de noticias
    news_videos = []
    for i in range(1, 6):
        news_path = os.path.join(OUTPUT_DIR, f"noticia_{i}.mp4")
        if os.path.exists(news_path):
            clip = VideoFileClip(news_path).fadein(0.5).fadeout(0.5)  # Aplicar transiciones suaves
            news_videos.append(clip)
        else:
            print(f"⚠️ No se encontró el video {news_path}, se omitirá.")

    # Cargar los videos de introducción y cierre
    intro_video = VideoFileClip(intro_path).fadein(0.5).fadeout(0.5)
    closing_video = VideoFileClip(closing_path).fadein(0.5)

    # Unir todos los clips en un solo video con transiciones suaves
    final_clip = concatenate_videoclips([intro_video] + news_videos + [closing_video], method="compose")

    # Definir la ruta de salida
    final_output_path = os.path.join(OUTPUT_DIR, "final_video.mp4")
    final_output_path_with_date = os.path.join(OUTPUT_DIR, f"final_video_{fecha_formateada}.mp4")


    # Exportar el video final
    final_clip.write_videofile(final_output_path, fps=30, codec="libx264", audio_codec="aac")

        # Copiar el archivo en lugar de renderizarlo de nuevo
    shutil.copy(final_output_path, final_output_path_with_date)


    print(f"✅ Video final generado en {final_output_path}")
    print(f"✅ También guardado en {final_output_path_with_date}")


if __name__ == "__main__":
    merge_videos()
