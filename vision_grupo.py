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

def capturar_region(x,y,h,w):

    with mss.mss() as sct:

        region = {
            "top": y,
            "left": x,
            "width": w,
            "height": h
        }

        screenshot = sct.grab(region)

        img = np.array(screenshot)[:,:,:3]

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        return img,gray
    
def comparar_region(img1,img2,threshold=25):

    import cv2
    import numpy as np

    diff = cv2.absdiff(img1,img2)

    gray = cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)

    _,mask = cv2.threshold(gray,threshold,255,cv2.THRESH_BINARY)

    cambios = cv2.countNonZero(mask)

    return cambios