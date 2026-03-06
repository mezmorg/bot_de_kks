import time
import pyautogui

import vision_grupo
import publi_grupo


############################################
# CLICK CUADRANTE INFERIOR IZQUIERDO
############################################

def click_inferior_izquierda(x,y,w,h):

    px = x + int(w*0.25)
    py = y + int(h*0.75)

    pyautogui.click(px,py)


############################################
# ESPERAR QUE MUERTO DESAPAREZCA
############################################

def cerrar_muerte():

    while True:

        img,gray,edges = vision_grupo.capturar_pantalla()

        muerto = vision_grupo.detectar_template(
            gray,
            vision_grupo.templates["muerto"]
        )

        if not muerto:
            return

        x,y = muerto[0]
        h,w = muerto[1]

        click_inferior_izquierda(x,y,w,h)

        time.sleep(0.5)


############################################
# ACTIVAR FENIX
############################################

def activar_fenix():

    img,gray,edges = vision_grupo.capturar_pantalla()

    fenix = vision_grupo.detectar_template(
        gray,
        vision_grupo.templates["fenix"]
    )

    if fenix:

        x,y = fenix[0]
        h,w = fenix[1]

        pyautogui.click(x+w//2,y+h//2)

        time.sleep(2)

        pyautogui.click(x+w//2,y+h//2)

        time.sleep(1)


############################################
# EQUIPAR SET
############################################

def equipar_set():

    while True:

        img,gray,edges = vision_grupo.capturar_pantalla()

        set_icon = vision_grupo.detectar_template(
            gray,
            vision_grupo.templates["set"]
        )

        if not set_icon:
            return

        x,y = set_icon[0]
        h,w = set_icon[1]

        pyautogui.click(x+w//2,y+h//2)

        time.sleep(0.6)

        img,gray,edges = vision_grupo.capturar_pantalla()

        equipar = vision_grupo.detectar_template(
            gray,
            vision_grupo.templates["equipar"]
        )

        if equipar:
            break


    ############################################
    # CLICK EQUIPAR
    ############################################

    while True:

        img,gray,edges = vision_grupo.capturar_pantalla()

        equipar = vision_grupo.detectar_template(
            gray,
            vision_grupo.templates["equipar"]
        )

        if not equipar:
            return

        x,y = equipar[0]
        h,w = equipar[1]

        pyautogui.click(x+w//2,y+h//2)

        time.sleep(0.5)


############################################
# PROGRAMA PRINCIPAL
############################################

def main():

    ############################################
    # CERRAR MENSAJE DE MUERTE
    ############################################

    cerrar_muerte()


    ############################################
    # LIMPIAR PUBLICIDAD / MENSAJES
    ############################################

    publi_grupo.check()


    ############################################
    # ACTIVAR FENIX
    ############################################

    activar_fenix()


    ############################################
    # EQUIPAR SET
    ############################################

    equipar_set()


############################################
# EJECUCION
############################################

if __name__ == "__main__":

    main()