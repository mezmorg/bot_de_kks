import time
import pyautogui
import subprocess
import sys
import os

import vision


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

############################################
# MODO COMBATE
############################################

def combate():

    print("Modo combate")

    while True:

        img, gray, edges = vision.capturar_pantalla()


        ############################################
        # SALIR COMBATE
        ############################################

        salir = vision.detectar_template(
            gray,
            vision.templates["salir_combate"]
        )

        if salir:

            print("Combate terminado")

            time.sleep(1)

            return


        ############################################
        # BOTON LISTO
        ############################################

        listo = vision.detectar_template(
            gray,
            vision.templates["listo"]
        )

        if listo:

            x,y = listo[0]
            h,w = listo[1]

            pyautogui.click(x+w//2,y+h//2)

            time.sleep(0.5)
            listo = vision.detectar_template(
                gray,
                vision.templates["listo"]
            )
            if listo:
                subprocess.run([
                    sys.executable,
                    os.path.join(BASE_DIR,"grupo.py")
                ])


        ############################################
        # PASAR TURNO
        ############################################

        grupo = vision.detectar_template(
            gray,
            vision.templates["turno_grupo"]
        )
        if grupo:
            subprocess.run([
                sys.executable,
                os.path.join(BASE_DIR,"grupo.py")
            ])

        turno = vision.detectar_template(
            gray,
            vision.templates["turno_mio"]
        )

        if turno:

            pasar = vision.detectar_template(
                gray,
                vision.templates["pasar_turno"]
            )

            if pasar:
                x,y = pasar[0]
                h,w = pasar[1]

                pyautogui.click(x+w//2,y+h//2)
                time.sleep(1)
                pyautogui.click(x+w//2,y+h//2)
                
        time.sleep(0.25)


############################################
# EJECUCION
############################################

if __name__ == "__main__":

    combate()