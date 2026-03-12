import time
import pyautogui
import subprocess
import sys
import os

import vision


############################################
# RUTA BASE
############################################

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


############################################
# DETECCION PUBLICIDAD / MUERTE / COMBATE
############################################

def check():

    img, gray, edges = vision.capturar_pantalla()


    ############################################
    # COMPROBAR COMBATE (PRIORIDAD MAXIMA)
    ############################################

    combate = vision.detectar_template(
        gray,
        vision.templates["combate"]
    )

    if combate:

        print("Combate detectado")

        subprocess.run([
            sys.executable,
            os.path.join(BASE_DIR,"grupo.py")
        ])

        subprocess.run([
            sys.executable,
            os.path.join(BASE_DIR,"combate.py")
        ])

        # Al salir del combate revisar inmediatamente
        img, gray, edges = vision.capturar_pantalla()


    ############################################
    # COMPROBAR PUBLICIDAD
    ############################################

    publi = vision.detectar_template(
        gray,
        vision.templates["publi"]
    )

    if publi:

        # comprobar si está muerto
        muerto = vision.detectar_template(
            gray,
            vision.templates["muerto"]
        )

        if muerto:

            print("Personaje muerto detectado")

            subprocess.run([
                sys.executable,
                os.path.join(BASE_DIR,"grupo.py")
            ])

            subprocess.run([
                sys.executable,
                os.path.join(BASE_DIR,"muerte.py")
            ])

            return "MUERTO"


        print("Publicidad detectada")

        cerrar = vision.detectar_template(
            gray,
            vision.templates["cerrar"]
        )
        
        if cerrar:
            x,y = cerrar[0]
            h,w = cerrar[1]

            pyautogui.click(x+w//2,y+h//2)

        return "PUBLI"


    ############################################
    # COMPROBAR MUERTE DIRECTA
    ############################################

    muerto = vision.detectar_template(
        gray,
        vision.templates["muerto"]
    )

    if muerto:

        print("Personaje muerto detectado")

        subprocess.run([
            sys.executable,
            os.path.join(BASE_DIR,"grupo.py")
        ])

        subprocess.run([
            sys.executable,
            os.path.join(BASE_DIR,"muerte.py")
        ])

        return "MUERTO"


    return None