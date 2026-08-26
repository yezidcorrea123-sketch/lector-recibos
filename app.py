import streamlit as st
import cv2
import numpy as np
import pytesseract
import csv
from datetime import datetime
import os

# Configurar el motor para tu computador o para internet
if os.name == 'nt':
    pytesseract.pytesseract.tesseract_cmd = r'c:\program files\tesseract-ocr\tesseract.exe'

st.title("Lector de recibos")
st.write("Enciende tu camara y toma una foto para guardar los datos.")

foto = st.camera_input("Tomar foto al recibo")

if foto is not None:
    bytes_datos = np.asarray(bytearray(foto.read()), dtype=np.uint8)
    imagen = cv2.imdecode(bytes_datos, 1)

    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    _, imagen_limpia = cv2.threshold(imagen_gris, 130, 255, cv2.THRESH_BINARY)

    texto = pytesseract.image_to_string(imagen_limpia)

    st.write("Este es el texto leido:")
    st.text(texto)

    if st.button("Guardar en base de datos"):
        with open("base_datos.csv", "a", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), texto])
        st.success("Los datos se guardaron correctamente en tu archivo")