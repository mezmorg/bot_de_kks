import os
import cv2
import numpy as np
import mss
import glob


############################################
# RUTAS DEL PROYECTO
############################################

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATES_PATH = os.path.join(BASE_DIR, "templates")
ENEMIES_PATH = os.path.join(BASE_DIR, "enemies")


############################################
# TEMPLATE MATCH
############################################

def detectar_template(gray, template, threshold=0.8):

    if template is None:
        return None

    result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    _,max_val,_,max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        return max_loc, template.shape

    return None


############################################
# NMS
############################################

def nms(rects, overlapThresh=0.3):

    if len(rects) == 0:
        return []

    boxes = np.array(rects)

    x1 = boxes[:,0]
    y1 = boxes[:,1]
    x2 = boxes[:,0] + boxes[:,2]
    y2 = boxes[:,1] + boxes[:,3]

    areas = (x2-x1+1)*(y2-y1+1)
    idxs = np.argsort(y2)

    pick = []

    while len(idxs) > 0:

        last = idxs[-1]
        pick.append(last)

        xx1 = np.maximum(x1[last], x1[idxs[:-1]])
        yy1 = np.maximum(y1[last], y1[idxs[:-1]])
        xx2 = np.minimum(x2[last], x2[idxs[:-1]])
        yy2 = np.minimum(y2[last], y2[idxs[:-1]])

        w = np.maximum(0, xx2-xx1+1)
        h = np.maximum(0, yy2-yy1+1)

        overlap = (w*h)/areas[idxs[:-1]]

        idxs = np.delete(
            idxs,
            np.concatenate(([len(idxs)-1],
            np.where(overlap > overlapThresh)[0]))
        )

    return boxes[pick].astype("int")


############################################
# DETECTAR ENEMIGOS
############################################

enemy_templates = []

for file in glob.glob(os.path.join(ENEMIES_PATH, "*.png")):

    img = cv2.imread(file,0)

    edges = cv2.Canny(img,50,150)

    h,w = edges.shape

    enemy_templates.append({"image":edges,"w":w,"h":h})


def detectar_enemigos(edges_screen):

    rects = []

    for t in enemy_templates:

        result = cv2.matchTemplate(edges_screen,t["image"],cv2.TM_CCOEFF_NORMED)

        locations = np.where(result >= 0.35)

        for pt in zip(*locations[::-1]):

            rects.append((pt[0],pt[1],t["w"],t["h"]))

    rects = nms(rects)

    rects = sorted(rects,key=lambda r:(r[1],r[0]))

    return list(rects)


############################################
# CARGAR TEMPLATES
############################################

templates = {}
def cargar_templates():

    for archivo in os.listdir(TEMPLATES_PATH):

        if archivo.endswith(".png"):

            nombre = os.path.splitext(archivo)[0]

            ruta = os.path.join(TEMPLATES_PATH, archivo)

            img = cv2.imread(ruta, 0)

            templates[nombre] = img


cargar_templates()


############################################
# CAPTURA DE PANTALLA
############################################

def capturar_pantalla():

    with mss.mss() as sct:

        monitor = sct.monitors[1]

        screenshot = sct.grab(monitor)

        img = np.array(screenshot)[:,:,:3]

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(gray,50,150)

        return img, gray, edges

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