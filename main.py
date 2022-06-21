
# zaimportowanie potrzebnych bibliotek
import queue
import threading
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import shape_detector
from PIL import ImageGrab

# zmienne globalne
_VARS = {'window': False,
         'fig_agg': False,
         'pltFig': False}


# rysowanie figury
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


# nanoszenie figury na rysunek
def drawChart():
    _VARS['pltFig'], ax = plt.subplots()
    # circle1 = plt.Circle((0.5, 0.5), 0.3)
    text_kwargs = dict(ha='center', va='center', fontsize=24, color='b')
    plt.text(0.5, 0.5, 'Naciśnij -Go- aby rozpocząć', **text_kwargs)
    plt.axis('off')
    _VARS['fig_agg'] = draw_figure(
        _VARS['window']['figCanvas'].TKCanvas, _VARS['pltFig'])


# odświeżanie rysunku
def updateChart():
    _VARS['fig_agg'].get_tk_widget().forget()
    shape = shape_detector.detect()
    plt.clf()
    if shape == 1:
        circle1 = plt.scatter(0.5, 0.5, marker="o", s=50000)
        plt.gcf().gca().add_artist(circle1)
    elif shape == 3:
        triangle1 = plt.scatter(0.5, 0.5, marker="^", s=50000)
        plt.gcf().gca().add_artist(triangle1)
    elif shape == 4:
        square1 = plt.scatter(0.5, 0.5, marker="s", s=50000)
        plt.gcf().gca().add_artist(square1)
    else:
        text_kwargs = dict(ha='center', va='center', fontsize=24, color='b')
        plt.text(0.5, 0.5, 'Nie rozpoznano figury', **text_kwargs)
    plt.axis('off')
    _VARS['fig_agg'] = draw_figure(
        _VARS['window']['figCanvas'].TKCanvas, _VARS['pltFig'])


# metoda obsługująca wątek w tle
def long_function_wrapper(work_id, gui_queue):
    updateChart()
    gui_queue.put('{} ::: done'.format(work_id))
    return


# główna metoda interfejsu graficzengo
def the_gui():
    gui_queue = queue.Queue()

    # zaprojektowanie okna głównego
    sg.theme('DarkGrey3')
    layout = [[sg.Text('Rozpoznawane figury: koło, trójkąt, kwadrat')],
              [sg.Canvas(key='figCanvas')],
              [sg.Button('Go'), sg.Button('Save'), sg.Button('Exit')], ]

    _VARS['window'] = sg.Window('Detektor figur',
                                layout,
                                ttk_theme="vista",
                                finalize=True,
                                resizable=True,
                                location=(500, 175),
                                element_justification="center")

    drawChart()     # rysowanie figury

    # obsługa przycisków gui
    work_id = 0
    while True:
        event, values = _VARS['window'].Read(timeout=100)       # Oczekiwanie na eventy

        if event is None or event == 'Exit':                    # Wyjście z programu
            break

        if event == 'Save':                                     # Zapisanie figury do jpg
            sg.popup('Figura została pomyslnie zapisana!')
            ImageGrab.grab(bbox=(
        _VARS['fig_agg'].get_tk_widget().winfo_rootx(),
        _VARS['fig_agg'].get_tk_widget().winfo_rooty(),
        _VARS['fig_agg'].get_tk_widget().winfo_rootx() + _VARS['fig_agg'].get_tk_widget().winfo_width(),
        _VARS['fig_agg'].get_tk_widget().winfo_rooty() + _VARS['fig_agg'].get_tk_widget().winfo_height())).save("shape.jpg")

        if event == 'Go':                                       # Rozpoczęcie wykrywania w osobnym wątku
            thread_id = threading.Thread(target=long_function_wrapper, args=(work_id, gui_queue,), daemon=True)
            thread_id.start()

            work_id = work_id + 1 if work_id < 19 else 0

        try:
            message = gui_queue.get_nowait()
        except queue.Empty:
            message = None

        if message is not None:
            work_id -= 1
            if not work_id:
                sg.PopupAnimated(None)

        if work_id:                                             # Wyświetlanie animacji oczekiwania
            sg.PopupAnimated(sg.DEFAULT_BASE64_LOADING_GIF, background_color='white', relative_location=(100, 0),
                             time_between_frames=100)

    _VARS['window'].Close()


# inicjalizacja gui
if __name__ == '__main__':
    the_gui()
    print('Exiting Program')