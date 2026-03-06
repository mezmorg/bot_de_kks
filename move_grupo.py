import time
import pyautogui

import vision_grupo


############################################
# FUNCION MOVERSE
############################################

def moverse(direccion, desviacion=50):

    w, h = pyautogui.size()

    cx = w // 2
    cy = h // 2

    ############################################
    # DESVIACION
    ############################################

    if direccion in ["derecha", "izquierda"]:

        cy = cy - desviacion

    if direccion in ["arriba", "abajo"]:

        cx = cx + desviacion


    pyautogui.moveTo(cx, cy)

    pyautogui.mouseDown()


    ############################################
    # VECTOR MOVIMIENTO
    ############################################

    dx, dy = {

        "derecha": (250, 0),
        "izquierda": (-250, 0),
        "arriba": (0, -250),
        "abajo": (0, 250)

    }[direccion]


    ############################################
    # DESPLAZAMIENTO SUAVE
    ############################################

    for i in range(10):

        pyautogui.moveRel(dx / 10, dy / 10, duration=0.05)

    pyautogui.mouseUp()

    time.sleep(1)


    ############################################
    # COMPROBAR CAMBIO DE SALA
    ############################################

    img, gray, edges = vision_grupo.capturar_pantalla()


    flechas = {

        "derecha": vision_grupo.templates["flecha_derecha"],
        "izquierda": vision_grupo.templates["flecha_izquierda"],
        "arriba": vision_grupo.templates["flecha_arriba"],
        "abajo": vision_grupo.templates["flecha_abajo"]

    }


    flecha = vision_grupo.detectar_template(
        gray,
        flechas[direccion]
    )


    if flecha:

        time.sleep(1)

        return True


    return False