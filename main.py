import os
import subprocess
import requests  # Importa requests para hacer la llamada al webhook
import json
from dotenv import load_dotenv

# Definir el directorio base donde están los scripts
WORK_DIR = "/home/arivera/english_ciberaldia_sh/"

# Cargar variables de entorno desde el archivo .credential
dotenv_path = os.path.join(WORK_DIR, ".credential")
load_dotenv(dotenv_path)

# Webhook de Make
#MAKE_WEBHOOK_URL = "https://hook.us2.make.com/gevluv3ys4j3wvyybw5178oq2iz2hnae"
MAKE_WEBHOOK_URL = "https://automatizacion.ciberaldia.com/n8n/webhook/e72d3d88-2bfb-4506-bd08-43e522eb547b"

# Lista de scripts a ejecutar en orden
scripts = [
    "1-news_extractor.py",
    "2-gpt_generator.py",
    "3-audio_generator.py",
    "4-image_generator.py",
    "5-video_intro_creator.py",
    "6-video_news_creator.py",
    "7-video_closing_creator.py",
    "8-final_video_creator.py",
    "9-generar_post.py"
]

def run_script(script_name):
    """Ejecuta un script de Python ubicado en WORK_DIR y maneja posibles errores."""
    script_path = os.path.join(WORK_DIR, script_name)  # Ruta completa del script
    print(f"\n🚀 Ejecutando {script_path}...\n")

    result = subprocess.run(["python3", script_path], capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✅ {script_name} ejecutado correctamente.\n")
    else:
        print(f"❌ Error en {script_name}. Salida:\n{result.stderr}")
        exit(1)  # Detiene la ejecución si hay un error

if __name__ == "__main__":
    print("\n🔄 Iniciando el proceso completo...\n")

    for script in scripts:
        script_path = os.path.join(WORK_DIR, script)
        if os.path.exists(script_path):
            run_script(script)
        else:
            print(f"⚠️ Advertencia: {script_path} no encontrado, se omitirá.")

    print("\n🎬 ¡Proceso completado! El video final ha sido generado.\n")

    # 🔥 Disparar el webhook de Make cuando todo finalice
#    try:
#        payload = {
#            "message": "Video y post generados exitosamente",
#            "video_url": "http://82.25.74.175:8000/videos/final_video.mp4",
#            "post_url": "http://82.25.74.175:8000/post"
#        }
        #response = requests.post(MAKE_WEBHOOK_URL, data=json.dumps(payload), headers={"Content-Type": "application/json"})
        #response = requests.get(MAKE_WEBHOOK_URL, params=payload)
#
#        if response.status_code == 200:
#            print("✅ Webhook de Make ejecutado correctamente.")
#        else:
#            print(f"⚠️ Error al ejecutar el webhook: {response.status_code}, {response.text}")
#
#    except Exception as e:
#        print(f"❌ Error al llamar al webhook de Make: {str(e)}")
