import time
import pyautogui
import vision
import subprocess
import sys
import os

############################################
# RUTAS DEL PROYECTO
############################################

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATES_PATH = os.path.join(BASE_DIR, "templates")
ENEMIES_PATH = os.path.join(BASE_DIR, "enemies")


############################################
# CONFIGURACION MOVIMIENTO
############################################

DISTANCIA = 250
PASOS = 5
TIEMPO_PASO = 0.05
ESPERA_CAMBIO = 4


############################################
# MOVERSE
############################################

def moverse(direccion, desviacion=0):

    img, gray, edges = vision.capturar_pantalla()

    flechas = {
        "derecha": vision.templates["flecha_derecha"],
        "izquierda": vision.templates["flecha_izquierda"],
        "arriba": vision.templates["flecha_arriba"],
        "abajo": vision.templates["flecha_abajo"]
    }

    # inverso para compensar el drag del mapa
    dx,dy = {
        "derecha":(-DISTANCIA,0),
        "izquierda":(DISTANCIA,0),
        "arriba":(0,DISTANCIA),
        "abajo":(0,-DISTANCIA)
    }[direccion]


    ############################################
    # POSICION INICIAL DEL MOUSE
    ############################################

    w,h = pyautogui.size()

    cx = w//2
    cy = h//2


    # aplicar desviación
    if direccion in ["derecha","izquierda"]:
        cy -= desviacion

    if direccion in ["arriba","abajo"]:
        cx += desviacion


    pyautogui.moveTo(cx,cy)


    ############################################
    # ARRASTRAR MOUSE
    ############################################

    pyautogui.mouseDown()

    paso_x = dx/PASOS
    paso_y = dy/PASOS

    flecha_detectada = False

    for i in range(PASOS):

        pyautogui.moveRel(paso_x,paso_y,duration=TIEMPO_PASO)

        img, gray, edges = vision.capturar_pantalla()

        res = vision.detectar_template(
            gray,
            flechas[direccion],
            0.8
        )

        if res:
            flecha_detectada = True


    pyautogui.mouseUp()


    ############################################
    # SI NO HAY FLECHA NO HAY MOVIMIENTO
    ############################################

    if not flecha_detectada:

        print("No se detectó flecha de movimiento")

        return False


    ############################################
    # ESPERAR CAMBIO DE MAPA
    ############################################

    time.sleep(ESPERA_CAMBIO)

    img2, gray2, edges2 = vision.capturar_pantalla()


    diff = abs(gray2.astype("int16") - gray.astype("int16")).mean()


    if diff < 5:

        print("No hubo cambio de mapa")

        return False


    print("Movimiento exitoso:", direccion)

    subprocess.run([
        sys.executable,
        os.path.join(BASE_DIR,"grupo.py")
    ])
    
    return True