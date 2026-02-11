import pandas as pd
import smtplib
import os
import unicodedata
from datetime import datetime
from email.message import EmailMessage

# Variables de entorno (se configuran en GitHub Secrets)
EMAIL_USER = os.environ["EMAIL_USER"]
EMAIL_PASS = os.environ["EMAIL_PASS"]

# Función para limpiar nombres y apellidos (quita tildes y minúsculas)
def limpiar(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFKD', texto)
    texto = texto.encode('ASCII', 'ignore').decode('utf-8')
    return texto

# Leer Excel
df = pd.read_excel("cumpleaños.xlsx")

# Fecha de hoy (solo mes y día)
hoy = datetime.today().strftime("%m-%d")

for index, row in df.iterrows():
    try:
        fecha = pd.to_datetime(row["fecha"]).strftime("%m-%d")
        if fecha == hoy:
            nombre = str(row["nombre"]).strip()
            apellido = str(row["apellido"]).strip()
            destinatario = str(row["email"]).strip()

            nombre_completo = f"{nombre} {apellido}"

            # Crear el correo
            msg = EmailMessage()
            msg["Subject"] = f"🎉 ¡Feliz cumpleaños {nombre}!"
            msg["From"] = EMAIL_USER
            msg["To"] = destinatario

            msg.set_content(f"""
Hola {nombre},

La comunidad te desea un muy feliz cumpleaños 🎂🎉

¡Que tengas un excelente día!

Saludos.
""")

            # Buscar la imagen PNG o JPG en la misma carpeta
            imagen_base = f"{limpiar(apellido)}_{limpiar(nombre)}"
            imagen_path = None
            subtype = None

            if os.path.exists(imagen_base + ".jpg"):
                imagen_path = imagen_base + ".jpg"
                subtype = "jpeg"
            elif os.path.exists(imagen_base + ".png"):
                imagen_path = imagen_base + ".png"
                subtype = "png"

            if imagen_path:
                with open(imagen_path, "rb") as f:
                    msg.add_attachment(
                        f.read(),
                        maintype="image",
                        subtype=subtype,
                        filename=os.path.basename(imagen_path)
                    )
            else:
                print(f"No se encontró imagen para {nombre_completo}")

            # Enviar correo usando Gmail
            with smtplib.SMTP_SSL("smtp.gmail.com", 465_

