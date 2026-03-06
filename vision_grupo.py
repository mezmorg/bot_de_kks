import os
import cv2
import mss
import numpy as np


############################################
# CONFIGURACION
############################################

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATES_DIR = os.path.join(BASE_DIR, "templates_2")

THRESHOLD = 0.85


############################################
# CAPTURA MSS GLOBAL (más rápido)
############################################

sct = mss.mss()
monitor = sct.monitors[1]


############################################
# CARGAR TEMPLATES
############################################

templates = {}


def cargar_templates():

    for archivo in os.listdir(TEMPLATES_DIR):

        if archivo.endswith(".png"):

            nombre = os.path.splitext(archivo)[0]

            ruta = os.path.join(TEMPLATES_DIR, archivo)

            img = cv2.imread(ruta, 0)

            templates[nombre] = img


cargar_templates()


############################################
# CAPTURAR PANTALLA
############################################

def capturar_pantalla():

    screenshot = sct.grab(monitor)

    img = np.array(screenshot)[:, :, :3]

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 50, 150)

    return img, gray, edges


############################################
# DETECTAR TEMPLATE
############################################

def detectar_template(gray, template, threshold=THRESHOLD):

    result = cv2.matchTemplate(
        gray,
        template,
        cv2.TM_CCOEFF_NORMED
    )

    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:

        return max_loc, template.shape

    return None