markdown
# 🛡️ CiberAlDía - Generador de Noticias en Video 📹  

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)  
📢 **Automatización de noticias de ciberseguridad en formato de video para redes sociales**.  
Extrae noticias de fuentes confiables, las procesa con IA y genera videos con imágenes y narración.  

## 🏗️ **Estructura del Proyecto**

 ```📂 ciberaldia_sh
 ├── 📂 audio/                 # Audios generados con TTS
 ├── 📂 images/                # Imágenes generadas para las noticias
 ├── 📂 news_archive/          # Archivos JSON con las noticias extraídas
 ├── 📂 output/                # Videos generados listos para publicar
 ├── 📂 scripts/               # Guiones de las noticias generados por GPT
 ├── 📜 config.py              # Configuración global del proyecto
 ├── 📜 extractor.py           # Extrae noticias desde fuentes RSS
 ├── 📜 scraper.py             # Extrae contenido completo de las noticias
 ├── 📜 storage.py             # Guarda las noticias extraídas
 ├── 📜 gpt_generator.py       # Genera el guion de las noticias usando GPT-4
 ├── 📜 audio_generator.py     # Convierte el guion en audio usando TTS
 ├── 📜 image_generator.py     # Genera imágenes para cada noticia
 ├── 📜 video_intro_creator.py # Crea el video de introducción
 ├── 📜 video_news_creator.py  # Crea los videos de cada noticia
 ├── 📜 video_closing_creator.py # Genera el video de cierre
 ├── 📜 final_video_creator.py # Une todos los videos y agrega transiciones
 ├── 📜 main.py                # Ejecuta todo el flujo de trabajo
 ├── 📜 requirements.txt       # Dependencias del proyecto
 ├── 📜 README.md              # Este archivo ✨
 ├── 📜 .credential            # Archivo con variables de entorno
 ```

---

## 🚀 **Instalación**
### 1️⃣ **Clonar el Repositorio**
```bash
git clone https://github.com/alrivera86/ciberaldia_sh.git
cd ciberaldia_sh
 ```

### 2️⃣ **Crear un Entorno Virtual (Opcional, pero recomendado)**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
 ```


### 3️⃣ **Instalar Dependencias**

```bash
pip install feedparser requests beautifulsoup4 openai 'moviepy==1.0.3' python-dotenv
 ```

---

## ⚙️ **Configuración**
### 1️⃣ **Variables de Entorno (`.credential`)**
Crea un archivo **`.credential`** en la raíz del proyecto con las siguientes claves:
```ini
export OPENAI_API_KEY="tu-api-key-de-openai"
export INSTAGRAM_ACCESS_TOKEN="tu-token-de-instagram"
export ELEVENLABS_API_KEY="tu-api-key-de-elevenlabs"
 ```
Para cargar las variables automáticamente:
 ```bash
source .credential
 ```

---

## 🏃 **Ejecución**
### **Ejecutar Todo el Flujo de Trabajo**
```bash
python3 main.py
 ```
Esto ejecutará **la extracción, generación de contenido, creación de videos y publicación**.

---

## 🔧 **Solución de Problemas**
### 🖼️ **Error con `moviepy` - Falta `ImageMagick`**
Si tienes problemas con `moviepy`, instala **ImageMagick** en **CentOS** con:
```bash
sudo yum install ImageMagick
```

En **Ubuntu/Debian**:
```bash
sudo apt install imagemagick
```

En **macOS**:
```bash
brew install imagemagick
```

Si sigue fallando, verifica que la variable de entorno `IMAGEMAGICK_BINARY` está configurada:
```bash
export IMAGEMAGICK_BINARY=$(which convert)
```

### 🔥 **Error de Memoria al Procesar Videos**
Si MoviePy se detiene abruptamente, intenta reducir la calidad del video:
```python
news_clip.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac", bitrate="500k")
```

---

## 🤝 **Contribuciones**
1. **Clona y crea una rama nueva**:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
2. **Haz tus cambios y súbelos**:
   ```bash
   git add .
   git commit -m "Añadir nueva funcionalidad"
   git push origin feature/nueva-funcionalidad
   ```
3. **Crea un Pull Request en GitHub**.

---

## 📜 **Licencia**
Este proyecto está bajo la licencia **MIT**.

---

💡 **¿Te gustó el proyecto?** ¡Dale una ⭐ en GitHub y síguenos en redes sociales! 🚀

---

🔹 **CiberAlDía** - Noticias de Ciberseguridad en Formato de Video 🔹  
📲 Instagram | 🎥 YouTube | 🐦 Twitter | 🌐 [Sitio Web](https://ciberaldia.com)  

```

---

### ✅ **Instrucciones Finales**
1. **Guarda este contenido en `README.md`**
2. **Sube el archivo al repositorio** con:
   ```bash
   git add README.md
   git commit -m "Añadir README.md actualizado"
   git push origin main
   ```
3. **Verifica en GitHub** que el README aparece correctamente formateado.

---

🚀 **Ahora tienes un README profesional y completo para tu proyecto!** 🎯
