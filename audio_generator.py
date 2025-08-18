import os
import requests
from datetime import datetime

# Obtener API Key de ElevenLabs desde variable de entorno
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"  # Puedes cambiar la voz si quieres

# Carpeta donde se guardarán los audios
AUDIO_DIR = "/home/arivera/ciberaldia_sh/audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

def get_script_files():
    """Obtiene la lista de archivos de guion en la carpeta scripts."""
    scripts_dir = "/home/arivera/ciberaldia_sh/scripts"
    return sorted([os.path.join(scripts_dir, f) for f in os.listdir(scripts_dir) if f.startswith("noticia_") and f.endswith(".txt")])

def read_script(file_path):
    """Lee el contenido del archivo de guion."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def generate_audio(script_text, output_filename):
    """Convierte el guion en audio usando ElevenLabs API."""
    url = "https://api.elevenlabs.io/v1/text-to-speech/" + ELEVENLABS_VOICE_ID

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": script_text,
        "model_id": "eleven_multilingual_v2",  # Usa el modelo multilingüe
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 1.0  # Ajusta la entonación para español
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        audio_path = os.path.join(AUDIO_DIR, output_filename)
        with open(audio_path, "wb") as f:
            f.write(response.content)
        print(f"✅ Audio guardado en {audio_path}")
        return audio_path
    else:
        print(f"❌ Error generando audio para {output_filename}: {response.text}")
        return None

def main():
    """Genera un archivo de audio para cada noticia en la carpeta scripts."""
    script_files = get_script_files()
    
    if not script_files:
        print("❌ No se encontraron archivos de guion recientes en la carpeta scripts.")
        return
    
    for script_file in script_files:
        script_text = read_script(script_file)
        news_number = os.path.basename(script_file).replace("noticia_", "").replace(".txt", "")
        audio_filename = f"noticia_{news_number}.mp3"
        generate_audio(script_text, audio_filename)
    
    print("✅ Todos los audios han sido generados correctamente.")

if __name__ == "__main__":
    main()
