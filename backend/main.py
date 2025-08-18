import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse, HTMLResponse  # ✅ Agregamos StreamingResponse
import subprocess
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permite GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Permite todos los encabezados HTTP
)

OUTPUT_DIR = "/home/arivera/ciberaldia_sh/output"
WORK_DIR = "/home/arivera/ciberaldia_sh/"
VIDEO_EXTENSIONS = [".mp4"]
POST_FILE = "post_del_dia.txt"

def list_files(directory, extensions):
    return [f for f in os.listdir(directory) if any(f.endswith(ext) for ext in extensions)]

@app.get("/")
def read_root():
    return {"message": "API para gestionar generación de videos y posts"}

@app.post("/run")
def run_script():
    def generate_output():
        process = subprocess.Popen(["python3", os.path.join(WORK_DIR, "main.py")], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in process.stdout:
            yield line  # Envía la salida en tiempo real
        for line in process.stderr:
            yield line  # Captura errores también

    return StreamingResponse(generate_output(), media_type="text/plain")

@app.get("/videos")
def list_videos():
    videos = list_files(OUTPUT_DIR, VIDEO_EXTENSIONS)
    return {"videos": videos}

@app.get("/videos/{video_name}")
def get_video(video_name: str):
    video_path = os.path.join(OUTPUT_DIR, video_name)
    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video no encontrado")
    return FileResponse(video_path)

@app.get("/post")
def get_post():
    post_path = os.path.join(OUTPUT_DIR, POST_FILE)
    if not os.path.exists(post_path):
        raise HTTPException(status_code=404, detail="Post no encontrado")
    return FileResponse(post_path)

@app.get("/history")
def get_history():
    return {"message": "Historial de ejecuciones no implementado aún"}

@app.get("/download/{video_name}")
def download_video(video_name: str):
    video_path = os.path.join(OUTPUT_DIR, video_name)
    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video no encontrado")
    
    return FileResponse(video_path, media_type="video/mp4", filename=video_name)

from fastapi.responses import HTMLResponse

@app.get("/latest", response_class=HTMLResponse)
def get_latest():
    # Obtener la lista de videos en el directorio
    videos = list_files(OUTPUT_DIR, VIDEO_EXTENSIONS)
    if not videos:
        raise HTTPException(status_code=404, detail="No se encontraron videos")

    # Construir la ruta completa y encontrar el más reciente por fecha de modificación
    videos_full_paths = [os.path.join(OUTPUT_DIR, v) for v in videos]
    latest_video_path = max(videos_full_paths, key=os.path.getmtime)
    latest_video_name = os.path.basename(latest_video_path)

    # Leer el contenido del post
    post_path = os.path.join(OUTPUT_DIR, POST_FILE)
    if not os.path.exists(post_path):
        raise HTTPException(status_code=404, detail="Post no encontrado")

    with open(post_path, "r", encoding="utf-8") as f:
        post_content = f.read()

    # Ahora construimos el HTML manualmente
    html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Último Video y Post del Día</title>
    <style>
        .container {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 40px;
            margin-bottom: 40px;
        }}
        .video-container, .image-container {{
            flex: 1;
        }}
        .video-container video {{
            width: 50%;
            height: auto;
            border-radius: 10px;
        }}
        .image-container img {{
            width: 50%;
            height: auto;
            border-radius: 10px;
        }}
    </style>
</head>
<body style="font-family: Arial, sans-serif; margin: 40px;">
    <h1>Último Video</h1>

    <div class="container">
        <div class="video-container">
            <video controls>
                <source src="/videos/{latest_video_name}" type="video/mp4">
                Tu navegador no soporta el elemento de video.
            </video>
        </div>
        <div class="image-container">
            <img src="/videos/captura_segundo_4_INTRO.png" alt="Captura del video">
        </div>
    </div>

    <a href="/download/{latest_video_name}" download>
        <button style="padding: 10px 20px; font-size: 16px;">Descargar Video</button>
    </a>

    <hr style="margin: 40px 0;">

    <h2>Post del Día</h2>

    <div style="position: relative; margin-bottom: 10px;">
        <button onclick="copyPostText()" style="padding: 8px 16px; font-size: 14px;">📋 Copiar Post</button>
    </div>

    <textarea id="postContent" style="width:100%; height:300px; background: #f5f5f5; padding: 20px; border-radius: 10px; font-size: 16px;">{post_content}</textarea>

    <script>
    function copyPostText() {{
        var textArea = document.getElementById('postContent');
        textArea.select();
        document.execCommand('copy');
        alert('¡Texto del post copiado!');
    }}
    </script>
</body>
</html>
"""

    return HTMLResponse(content=html)
