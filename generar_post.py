import os
import datetime
import locale
from config import DAYS_OFFSET  # ✅ Importar la configuración

# Configurar el locale en español
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

# Calcular la fecha correcta según DAYS_OFFSET
fecha_correcta = datetime.datetime.today() - datetime.timedelta(days=DAYS_OFFSET)

fecha_formateada = fecha_correcta.strftime("%d_%m_%Y")  # Formato: DD_MM_AAAA





# Directorio donde se guardan los guiones de noticias
SCRIPTS_DIR = "/home/arivera/ciberaldia_sh/scripts"
OUTPUT_DIR = "/home/arivera/ciberaldia_sh/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Emojis de encabezado
HEADER = "🛡️ ¿Qué pasó hoy en Ciberseguridad? 🔐"
# Formatear la fecha en español
DATE = f"📅 Fecha: {fecha_correcta.strftime('%d de %B de %Y')}\n"

# DATE = f"📅 Fecha: {datetime.datetime.today().strftime('%d de %B de %Y')}\n"

INTRO = "🔎 ¡Mantente informado con las noticias más importantes del mundo digital! 👇\n"

# Lista de emojis para cada noticia
NEWS_ICONS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]

# Cargar las noticias
news_posts = []
for i in range(1, 6):  # Leer hasta 5 noticias
    script_path = os.path.join(SCRIPTS_DIR, f"noticia_{i}.txt")
    if os.path.exists(script_path):
        with open(script_path, "r", encoding="utf-8") as file:
            content = file.read().strip()
            news_posts.append(f"{NEWS_ICONS[i-1]} {content}")

# Si no hay noticias, mostrar un mensaje
if not news_posts:
    print("❌ No se encontraron noticias para generar el post.")
    exit()

# Crear el post
POST_CONTENT = f"{HEADER}\n{DATE}\n{INTRO}\n" + "\n\n".join(news_posts) + "\n\n✨ Mantente alerta y protege tu información. Síguenos para más actualizaciones diarias sobre ciberseguridad.\n\n🔔 #Ciberseguridad #SeguridadDigital #NoticiasTech #ProtegeTuInfo #Hackers #Tecnología #NoticiasDeHoy #SeguridadInformática\n\n📲 ¿Cuál de estas noticias te impactó más? ¡Déjalo en los comentarios! ⬇️"

# Guardar en archivo
post_file_path = os.path.join(OUTPUT_DIR, "post_del_dia.txt")
post_file_with_date = os.path.join(OUTPUT_DIR, f"post_del_dia_{fecha_formateada}.txt")

with open(post_file_path, "w", encoding="utf-8") as file:
    file.write(POST_CONTENT)

with open(post_file_with_date, "w", encoding="utf-8") as file:
    file.write(POST_CONTENT)

# Mostrar por pantalla
print("\n✅ **Post generado correctamente** ✅\n")
print(POST_CONTENT)
print(f"\n📂 El post ha sido guardado en: {post_file_path}")
print(f"📂 También se ha guardado en: {post_file_with_date}")

