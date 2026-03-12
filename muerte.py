import time
import pyautogui
import subprocess
import sys
import os

import vision
import move
import publi


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


############################################
# ESPERAR DESAPARICION DE MUERTE
############################################

def cerrar_mensaje_muerte():

    while True:

        img, gray, edges = vision.capturar_pantalla()

        muerto = vision.detectar_template(
            gray,
            vision.templates["muerto"]
        )

        if not muerto:
            return

        x,y = muerto[0]
        h,w = muerto[1]

        click_x = x + int(w * 0.25)
        click_y = y + int(h * 0.75)

        pyautogui.click(click_x,click_y)

        time.sleep(0.5)


############################################
# ACTIVAR FENIX
############################################

def activar_fenix():

    while True:
        
        while publi.check() is not None:
            time.sleep(1)

        img, gray, edges = vision.capturar_pantalla()

        fenix = vision.detectar_template(
            gray,
            vision.templates["fenix"]
        )

        if fenix:

            x,y = fenix[0]
            h,w = fenix[1]

            pyautogui.click(x+w//2,y+h//2)
            time.sleep(1)
            pyautogui.click(x+w//2,y+h//2)

            return

        time.sleep(0.5)


############################################
# EQUIPAR SET
############################################

def equipar_set():

    while True:

        img,gray,edges = vision.capturar_pantalla()

        set_icon = vision.detectar_template(
            gray,
            vision.templates["set"]
        )

        if not set_icon:
            return

        x,y = set_icon[0]
        h,w = set_icon[1]

        pyautogui.click(x+w//2,y+h//2)

        time.sleep(0.6)

        img,gray,edges = vision.capturar_pantalla()

        equipar = vision.detectar_template(
            gray,
            vision.templates["equipar"]
        )

        if equipar:
            break


    ############################################
    # CLICK EQUIPAR
    ############################################

    while True:

        img,gray,edges = vision.capturar_pantalla()

        equipar = vision.detectar_template(
            gray,
            vision.templates["equipar"]
        )

        if not equipar:
            return

        x,y = equipar[0]
        h,w = equipar[1]

        pyautogui.click(x+w//2,y+h//2)

        time.sleep(0.5)


############################################
# BUSCAR TEMPLATE AL CAMBIAR SALA
############################################

def buscar_template(template):

    img, gray, edges = vision.capturar_pantalla()

    res = vision.detectar_template(gray,template)

    return res


############################################
# MOVER HASTA ENCONTRAR
############################################

def mover_hasta(direccion, template, max_intentos, desvio=0):

    for i in range(max_intentos):

        if move.moverse(direccion,desvio):

            publi.check()

            if buscar_template(template):
                return True

    return False


############################################
# RUTA DE REGRESO
############################################

def ruta_regreso():

    print("Ruta regreso iniciada")

    # derecha -> llanura

    if not mover_hasta(
        "derecha",
        vision.templates["guia1"],
        20
    ):
        pass


    # abajo -> 21

    if not mover_hasta(
        "abajo",
        vision.templates["guia2"],
        40,-30
    ):
        pass


    # derecha -> 56

    if not mover_hasta(
        "derecha",
        vision.templates["guia3"],
        20,50
    ):
        pass


    # arriba -> zona

    if mover_hasta(
        "arriba",
        vision.templates["zona"],
        20
    ):
        print("Zona encontrada")
        return True


    print("Zona no encontrada")

    return False


############################################
# MODO MUERTE
############################################

def muerte():

    print("Modo muerte iniciado")

    cerrar_mensaje_muerte()

    activar_fenix()

    equipar_set()

    if ruta_regreso():
        return


    print("Activando retorno.py")

    subprocess.run([
        sys.executable,
        os.path.join(BASE_DIR,"retorno.py")
    ])


############################################
# EJECUCION
############################################

if __name__ == "__main__":

    muerte()