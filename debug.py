import threading
import time
import win32gui
import win32con
import win32api

rects = []
overlay_thread = None
running = False
hwnd = None


############################################
# WINDOW PROC
############################################

def wndProc(hwnd,msg,wparam,lparam):

    if msg == win32con.WM_PAINT:

        hdc, ps = win32gui.BeginPaint(hwnd)

        # limpiar pantalla del overlay
        brush = win32gui.CreateSolidBrush(win32api.RGB(0,0,0))
        win32gui.FillRect(hdc, ps[2], brush)
        win32gui.DeleteObject(brush)

        pen = win32gui.CreatePen(
            win32con.PS_SOLID,
            2,
            win32api.RGB(0,255,0)
        )

        brush = win32gui.GetStockObject(win32con.NULL_BRUSH)

        win32gui.SelectObject(hdc,pen)
        win32gui.SelectObject(hdc,brush)

        for x,y,w,h in rects:

            win32gui.Rectangle(
                hdc,
                x,
                y,
                x+w,
                y+h
            )

        win32gui.EndPaint(hwnd,ps)

        return 0

    return win32gui.DefWindowProc(hwnd,msg,wparam,lparam)


############################################
# OVERLAY LOOP
############################################

def overlay_loop():

    global hwnd,running

    hInstance = win32api.GetModuleHandle()

    className = "DebugOverlay"

    wndClass = win32gui.WNDCLASS()
    wndClass.lpfnWndProc = wndProc
    wndClass.lpszClassName = className
    wndClass.hInstance = hInstance

    try:
        win32gui.RegisterClass(wndClass)
    except:
        pass

    width = win32api.GetSystemMetrics(0)
    height = win32api.GetSystemMetrics(1)

    exStyle = (
        win32con.WS_EX_LAYERED |
        win32con.WS_EX_TRANSPARENT |
        win32con.WS_EX_TOPMOST
    )

    hwnd = win32gui.CreateWindowEx(
        exStyle,
        className,
        None,
        win32con.WS_POPUP,
        0,
        0,
        width,
        height,
        None,
        None,
        hInstance,
        None
    )

    win32gui.SetLayeredWindowAttributes(
        hwnd,
        win32api.RGB(0,0,0),
        0,
        win32con.LWA_COLORKEY
    )

    win32gui.ShowWindow(hwnd,win32con.SW_SHOW)

    while running:

        win32gui.PumpWaitingMessages()

        win32gui.InvalidateRect(hwnd,None,True)
        win32gui.UpdateWindow(hwnd)

        time.sleep(0.01)


############################################
# START THREAD
############################################

def start():

    global overlay_thread,running

    if overlay_thread and overlay_thread.is_alive():
        return

    running = True

    overlay_thread = threading.Thread(
        target=overlay_loop,
        daemon=True
    )

    overlay_thread.start()


############################################
# API
############################################

def add(x,y,h,w):

    start()

    rects.append((x,y,w,h))


def clean():

    rects.clear()

    if hwnd:
        win32gui.InvalidateRect(hwnd,None,True)
        win32gui.UpdateWindow(hwnd)


def stop():

    global running

    running = False

    rects.clear()

    if hwnd:
        try:
            win32gui.DestroyWindow(hwnd)
        except:
            pass