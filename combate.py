import time
import pyautogui
import ctypes

import vision


############################################
# CURSOR WINDOWS
############################################

class CURSORINFO(ctypes.Structure):

    _fields_ = [
        ("cbSize", ctypes.c_uint),
        ("flags", ctypes.c_uint),
        ("hCursor", ctypes.c_void_p),
        ("ptScreenPos", ctypes.c_long * 2)
    ]


def get_cursor_handle():

    ci = CURSORINFO()

    ci.cbSize = ctypes.sizeof(ci)

    ctypes.windll.user32.GetCursorInfo(ctypes.byref(ci))

    return ci.hCursor


############################################
# PASAR TURNO INTELIGENTE
############################################

def pasar_turno_inteligente(x,y,w,h):

    bx = x + w//2
    by = y + h//2

    pyautogui.moveTo(bx,by)

    time.sleep(0.2)

    cursor_base = get_cursor_handle()

    time.sleep(0.1)

    cursor_actual = get_cursor_handle()

    if cursor_actual != cursor_base:

        pyautogui.click()

        sw,sh = pyautogui.size()

        pyautogui.moveTo(sw//2,sh//2)

        time.sleep(0.1)

        pyautogui.moveTo(bx,by)


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

            time.sleep(0.4)


        ############################################
        # PASAR TURNO
        ############################################

        pasar = vision.detectar_template(
            gray,
            vision.templates["pasar"]
        )

        if pasar:

            x,y = pasar[0]
            h,w = pasar[1]

            pasar_turno_inteligente(x,y,w,h)


        time.sleep(0.25)


############################################
# EJECUCION
############################################

if __name__ == "__main__":

    combate()