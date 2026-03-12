import time
import pyautogui
import subprocess
import sys
import os

import vision_grupo


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


############################################
# FUNCION PRINCIPAL
############################################

def check():

    img, gray, edges = vision_grupo.capturar_pantalla()


    ############################################
    # 1. MUERTO
    ############################################

    muerto = vision_grupo.detectar_template(
        gray,
        vision_grupo.templates["muerto"]
    )

    if muerto:

        subprocess.Popen([
            sys.executable,
            os.path.join(BASE_DIR, "muerte_grupo.py")
        ])


    ############################################
    # 2. UNIRSE
    ############################################

    unirse = vision_grupo.detectar_template(
        gray,
        vision_grupo.templates["unirse"]
    )

    while unirse:

        x, y = unirse[0]
        h, w = unirse[1]

        pyautogui.click(x + w // 2, y + h // 2)

        time.sleep(0.3)

        img, gray, edges = vision_grupo.capturar_pantalla()

        unirse = vision_grupo.detectar_template(
            gray,
            vision_grupo.templates["unirse"]
        )


    ############################################
    # 3. PUBLICIDAD
    ############################################

    publi = vision_grupo.detectar_template(
        gray,
        vision_grupo.templates["publi"]
    )

    while publi:

        cerrar = vision_grupo.detectar_template(
            gray,
            vision_grupo.templates["cerrar"]
        )

        if cerrar:

            x, y = cerrar[0]
            h, w = cerrar[1]

            pyautogui.click(x + w // 2, y + h // 2)

            time.sleep(0.3)

        img, gray, edges = vision_grupo.capturar_pantalla()

        publi = vision_grupo.detectar_template(
            gray,
            vision_grupo.templates["publi"]
        )


    ############################################
    # 4. LISTO (DETENER FLUJO)
    ############################################

    listo = vision_grupo.detectar_template(
        gray,
        vision_grupo.templates["listo"]
    )

    if listo:

        while listo:

            x, y = listo[0]
            h, w = listo[1]

            pyautogui.click(x + w // 2, y + h // 2)

            time.sleep(0.3)

            img, gray, edges = vision_grupo.capturar_pantalla()

            listo = vision_grupo.detectar_template(
                gray,
                vision_grupo.templates["listo"]
            )

        return


    ############################################
    # 5. PASAR TURNO (DETENER FLUJO)
    ############################################

    turno = vision_grupo.detectar_template(
        gray,
        vision_grupo.templates["turno_mio"]
    )
    tiempo_inicio = time.time()
    if turno:
        tiempo_inicio = time.time()
        while True:
            
            pasar = vision_grupo.detectar_template(
                gray,
                vision_grupo.templates["pasar_turno"]
            )

            if pasar:

                x, y = pasar[0]
                h, w = pasar[1]

                bx = x + w // 2
                by = y + h // 2

                pyautogui.click(bx, by)
                time.sleep(0.1)
                return

            if time.time() - tiempo_inicio > 3:
                    return