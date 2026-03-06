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

templates = {

    "rango":cv2.imread(os.path.join(TEMPLATES_PATH,"rango.png"),0),
    "cruz":cv2.imread(os.path.join(TEMPLATES_PATH,"cruz.png"),0),
    "zona":cv2.imread(os.path.join(TEMPLATES_PATH,"zona.png"),0),
    "publi":cv2.imread(os.path.join(TEMPLATES_PATH,"publi.png"),0),
    "atacar":cv2.imread(os.path.join(TEMPLATES_PATH,"atacar.png"),0),

    "combate":cv2.imread(os.path.join(TEMPLATES_PATH,"combate.png"),0),
    "listo":cv2.imread(os.path.join(TEMPLATES_PATH,"listo.png"),0),
    "pasar":cv2.imread(os.path.join(TEMPLATES_PATH,"pasar_turno.png"),0),
    "salir_combate":cv2.imread(os.path.join(TEMPLATES_PATH,"salir_combate.png"),0),

    "muerto":cv2.imread(os.path.join(TEMPLATES_PATH,"muerto.png"),0),
    "fenix":cv2.imread(os.path.join(TEMPLATES_PATH,"fenix.png"),0),
    "set":cv2.imread(os.path.join(TEMPLATES_PATH,"set.png"),0),
    "llanura":cv2.imread(os.path.join(TEMPLATES_PATH,"llanura.png"),0),
    "21":cv2.imread(os.path.join(TEMPLATES_PATH,"21.png"),0),
    "56":cv2.imread(os.path.join(TEMPLATES_PATH,"56.png"),0),

    "flecha_derecha":cv2.imread(os.path.join(TEMPLATES_PATH,"flecha_derecha.png"),0),
    "flecha_izquierda":cv2.imread(os.path.join(TEMPLATES_PATH,"flecha_izquierda.png"),0),
    "flecha_arriba":cv2.imread(os.path.join(TEMPLATES_PATH,"flecha_arriba.png"),0),
    "flecha_abajo":cv2.imread(os.path.join(TEMPLATES_PATH,"flecha_abajo.png"),0),

}


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