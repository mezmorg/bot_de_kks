import time
import pyautogui
import vision_grupo
from datetime import datetime,timedelta


############################################
# CONFIGURACION MOVIMIENTO
############################################

DISTANCIA = 250
PASOS = 5
TIEMPO_PASO = 0.05
ESPERA_CAMBIO = 7


############################################
# MOVERSE
############################################

def moverse(direccion, desviacion=0):

    img, gray, edges = vision_grupo.capturar_pantalla()

    flechas = {
        "derecha": vision_grupo.templates["flecha_derecha"],
        "izquierda": vision_grupo.templates["flecha_izquierda"],
        "arriba": vision_grupo.templates["flecha_arriba"],
        "abajo": vision_grupo.templates["flecha_abajo"]
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

        img, gray, edges = vision_grupo.capturar_pantalla()

        res = vision_grupo.detectar_template(
            gray,
            flechas[direccion],
            0.8
        )

        if res:
            flecha_detectada = True


    ############################################
    # SI NO HAY FLECHA NO HAY MOVIMIENTO
    ############################################

    if flecha_detectada:
        pyautogui.mouseUp()
    else:

        print("No se detectó flecha de movimiento")
        pyautogui.moveTo(cx,cy)
        pyautogui.mouseUp()

        return False


    ############################################
    # ESPERAR CAMBIO DE MAPA
    ############################################

    timpo_anterior = datetime.now()
    while True:

        img2, gray2, edges2 = vision_grupo.capturar_pantalla()

        cambios = vision_grupo.comparar_region(img,img2)
        if cambios > 60000:

            print("Movimiento exitoso:", direccion)
            
            return True
        
        if datetime.now() - timpo_anterior > timedelta(seconds=ESPERA_CAMBIO):
            print("error en el movimiento por tiempo")
            return False
        time.sleep(0.1)