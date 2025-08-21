import os
from moviepy.editor import VideoFileClip

# Directorios
VIDEOS_DIR = "/home/arivera/english_ciberaldia_sh/videos"
OUTPUT_DIR = "/home/arivera/english_ciberaldia_sh/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_closing_video():
    """Genera el video de cierre final."""
    
    # Cargar el video de cierre
    closing_video = VideoFileClip(os.path.join(VIDEOS_DIR, "Base_FIN_CON_VOZ_cyberdailyworld.mp4"))
    
    # Definir la ruta de salida
    output_path = os.path.join(OUTPUT_DIR, "closing_video.mp4")

    # Exportar el video final
    closing_video.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac")
    
    print(f"✅ Video de cierre generado en {output_path}")

if __name__ == "__main__":
    create_closing_video()
