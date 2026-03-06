import time
import random
import pytesseract
import pyautogui
import threading
import os
import traceback

import vision
import publi
import move


RANGO_MINIMO = 50
RANGO_MAXIMO = 300


############################################
# ZONA EXCLUSION
############################################

ultima_zona_click = None


def dentro_zona(x, y):

    global ultima_zona_click

    if ultima_zona_click is None:
        return False

    zx, zy, r = ultima_zona_click

    if abs(x - zx) <= r and abs(y - zy) <= r:
        return True

    return False


def actualizar_zona(x, y):

    global ultima_zona_click

    ultima_zona_click = (x, y, 50)


############################################
# LEER RANGO
############################################

def leer_rango(gray):

    res = vision.detectar_template(
        gray,
        vision.templates["rango"],
        0.7
    )

    if not res:
        return None

    x,y = res[0]
    h,w = res[1]

    roi = gray[y-5:y+h+3,x+w:x+w+35]

    text = pytesseract.image_to_string(
        roi,
        config="--psm 7 digits"
    )

    numeros = "".join(filter(str.isdigit,text))

    if numeros == "":
        return None

    valor = int(numeros)

    if valor < RANGO_MINIMO:
        return None

    return valor


############################################
# ATACAR
############################################

def intentar_atacar(gray):

    res = vision.detectar_template(
        gray,
        vision.templates["atacar"]
    )

    if not res:
        return False

    x,y = res[0]
    h,w = res[1]

    print("Atacando grupo")

    pyautogui.click(x+w//2,y+h//2)

    for _ in range(8):
        time.sleep(0.5)
        publi.check()

    return True


############################################
# CERRAR MENU
############################################

def cerrar_menu(gray):

    cruz = vision.detectar_template(
        gray,
        vision.templates["cruz"],
        0.7
    )

    if cruz:

        x,y = cruz[0]
        h,w = cruz[1]

        pyautogui.click(
            x+int(w*0.75),
            y+int(h*0.25)
        )


############################################
# CAMBIAR SALA
############################################

def cambiar_sala():

    direcciones = [
        "arriba",
        "abajo",
        "izquierda",
        "derecha"
    ]

    random.shuffle(direcciones)

    for d in direcciones:
        
        publi.check()

        if move.moverse(d):

            img,gray,edges = vision.capturar_pantalla()

            publi.check()

            zona = vision.detectar_template(
                gray,
                vision.templates["zona"]
            )

            if zona:
                return True

    return False


############################################
# BOT PRINCIPAL
############################################

def bot():

    while True:

        publi.check()

        img,gray,edges = vision.capturar_pantalla()

        enemigos = vision.detectar_enemigos(edges)

        if len(enemigos) == 0:

            cambiar_sala()

            continue


        # guardar cantidad inicial de intentos
        intentos = len(enemigos)

        print("Intentos en esta sala:", intentos)


        for intento in range(intentos):

            publi.check()

            img,gray,edges = vision.capturar_pantalla()

            enemigos = vision.detectar_enemigos(edges)

            if len(enemigos) == 0:
                continue


            enemigos = sorted(enemigos, key=lambda e: e[1])


            indice = intento % len(enemigos)

            x,y,w,h = enemigos[indice]

            cx = x + w//2
            cy = y + h//2


            if dentro_zona(cx,cy):

                print("Descartado por zona muerta")

                continue


            print("Intento", intento+1, "enemigo indice", indice+1)


            pyautogui.click(cx,cy)

            actualizar_zona(cx,cy)

            time.sleep(1)


            img,gray,edges = vision.capturar_pantalla()

            publi.check()

            rango = leer_rango(gray)


            if rango and RANGO_MINIMO < rango < RANGO_MAXIMO:

                if intentar_atacar(gray):
                    break


            cerrar_menu(gray)

            time.sleep(0.6)


        cambiar_sala()


############################################
# THREAD SEGURO
############################################

def safe_bot():

    try:

        bot()

    except Exception:

        traceback.print_exc()

        os._exit(1)


thread = threading.Thread(
    target=safe_bot,
    daemon=True
)

thread.start()

thread.join()