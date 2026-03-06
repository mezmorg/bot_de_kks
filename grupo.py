import time
import pygetwindow as gw
import win32gui

import vision_grupo
import publi_grupo
import move_grupo


############################################
# NOMBRES DE VENTANAS
############################################

VENTANA_PRINCIPAL = "TouchEmu 2,2"
VENTANA_SECUNDARIA = "gato-6136f52c"


############################################
# ACTIVAR VENTANA (METODO ROBUSTO)
############################################

def activar_ventana(nombre):

    ventanas = gw.getWindowsWithTitle(nombre)

    if not ventanas:
        return False

    hwnd = ventanas[0]._hWnd

    win32gui.ShowWindow(hwnd, 5)
    win32gui.SetForegroundWindow(hwnd)

    return True


############################################
# DETECTAR DIRECCION SEGUIR
############################################

def detectar_seguir(gray):

    checks = {

        "arriba": vision_grupo.templates["seguir_arriba"],
        "abajo": vision_grupo.templates["seguir_abajo"],
        "derecha": vision_grupo.templates["seguir_derecha"],
        "izquierda": vision_grupo.templates["seguir_izquierda"]

    }

    for direccion, template in checks.items():

        res = vision_grupo.detectar_template(
            gray,
            template
        )

        if res:
            return direccion

    return None


############################################
# PROGRAMA PRINCIPAL
############################################

def main():

    ############################################
    # CAMBIAR A VENTANA SECUNDARIA
    ############################################

    if not activar_ventana(VENTANA_SECUNDARIA):
        return

    time.sleep(0.5)


    ############################################
    # EJECUTAR PUBLICIDAD / COMBATE / MUERTE
    ############################################

    publi_grupo.check()


    ############################################
    # CAPTURAR PANTALLA
    ############################################

    img, gray, edges = vision_grupo.capturar_pantalla()


    ############################################
    # BUSCAR DIRECCION DE SEGUIR
    ############################################

    direccion = detectar_seguir(gray)

    if direccion:

        move_grupo.moverse(direccion)


    ############################################
    # VOLVER A VENTANA PRINCIPAL
    ############################################

    time.sleep(0.3)

    activar_ventana(VENTANA_PRINCIPAL)



############################################
# EJECUCION
############################################

if __name__ == "__main__":

    main()