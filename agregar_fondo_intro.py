import os
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
from moviepy.video.fx.all import resize

# Directorios
VIDEO_DIR = "/home/arivera/ciberaldia_sh/videos"
OUTPUT_DIR = "/home/arivera/ciberaldia_sh/output"
IMAGES_DIR = "/home/arivera/ciberaldia_sh/images"
VIDEO_INPUT_PATH = os.path.join(VIDEO_DIR, "Base_INTRO_CON_VOZ_CiberAldia.mp4")
VIDEO_OUTPUT_PATH = os.path.join(OUTPUT_DIR, "intro_video_CON_FONDO.mp4")

# Cargar video principal
video_clip = VideoFileClip(VIDEO_INPUT_PATH)

# Obtener imágenes de fondo
image_files = sorted([os.path.join(IMAGES_DIR, f) for f in os.listdir(IMAGES_DIR) if f.endswith((".png", ".jpg", ".jpeg"))])

if not image_files:
    print("❌ No se encontraron imágenes para el fondo.")
    exit()

# Crear un clip de imagen para cada imagen y hacer que duren el tiempo del video
background_clips = []
num_images = len(image_files)
duration_per_image = video_clip.duration / num_images  # Distribuir imágenes a lo largo del video

for i, img_path in enumerate(image_files):
    image_clip = ImageClip(img_path).set_duration(duration_per_image).resize(video_clip.size)
    background_clips.append(image_clip)

# Concatenar las imágenes para que cubran toda la duración del video
background_video = CompositeVideoClip(background_clips).set_duration(video_clip.duration)

# Superponer el video principal sobre el fondo
final_video = CompositeVideoClip([background_video, video_clip.set_position("center")])

# Exportar el video final
final_video.write_videofile(VIDEO_OUTPUT_PATH, fps=30, codec="libx264", audio_codec="aac")

print(f"✅ Video de introducción generado en {VIDEO_OUTPUT_PATH}")

