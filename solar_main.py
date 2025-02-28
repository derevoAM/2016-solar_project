# coding: utf-8
# license: GPLv3

import tkinter
import tkinter.filedialog as file
import solar_vis as vis
import solar_model as mod
import solar_input as inp
import matplotlib.pyplot as plt
import numpy as np

perform_execution = False
"""Флаг цикличности выполнения расчёта"""

physical_time = 0
"""Физическое время от начала расчёта.
Тип: float"""

displayed_time = None
"""Отображаемое на экране время.
Тип: переменная tkinter"""

time_step = None
"""Шаг по времени при моделировании.
Тип: float"""

space_objects = []
"""Список космических объектов."""


class Globals:
    def __init__(self):
        self.perform_execution = False
        self.physical_time = 0
        self.displayed_time = None
        self.time_step = None
        self.space_objects = []
        self.time_speed = 0
        self.root = tkinter.Tk()
        self.frame = tkinter.Frame(self.root)
        self.space = tkinter.Canvas(self.root, width=vis.window_width, height=vis.window_height, bg="black")
        self.start_button = tkinter.Button(self.frame, text="Start", command=lambda: start_execution(self), width=6)
        self.flag = 0


def execution(obj):
    """Функция исполнения -- выполняется циклически, вызывая обработку всех небесных тел,
    а также обновляя их положение на экране.
    Цикличность выполнения зависит от значения глобальной переменной perform_execution.
    При perform_execution == True функция запрашивает вызов самой себя по таймеру через от 1 мс до 100 мс.
    """

    mod.recalculate_space_objects_positions(obj.space_objects, obj.time_step.get())

    for body in obj.space_objects:
        vis.update_object_position(obj.space, body)

    obj.physical_time += obj.time_step.get()

    obj.displayed_time.set("%.1f" % obj.physical_time + " seconds gone")
    obj = inp.write_statistics(obj)
    if obj.perform_execution:
        obj.space.after(101 - int(obj.time_speed.get()), lambda: execution(obj))


def start_execution(obj):
    """Обработчик события нажатия на кнопку Start.
    Запускает циклическое исполнение функции execution.
    """
    obj.perform_execution = True
    obj.start_button['text'] = "Pause"
    obj.start_button['command'] = lambda: stop_execution(obj)

    execution(obj)
    print('Started execution...')


def stop_execution(obj):
    """Обработчик события нажатия на кнопку Start.
    Останавливает циклическое исполнение функции execution.
    """
    obj.perform_execution = False
    obj.start_button['text'] = "Start"
    obj.start_button['command'] = lambda: start_execution(obj)
    print('Paused execution.')


def open_file_dialog(ob):
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    ob.perform_execution = False
    for obj in ob.space_objects:
        ob.space.delete(obj.image)  # удаление старых изображений планет
    in_filename = file.askopenfilename(filetypes=(("Text file", ".txt"),))
    ob.space_objects = inp.read_space_objects_data_from_file(in_filename)
    max_distance = max([max(abs(obj.x), abs(obj.y)) for obj in ob.space_objects])
    vis.scale_factor = vis.calculate_scale_factor(max_distance)

    for obj in ob.space_objects:
        if obj.type == 'star':
            vis.create_star_image(ob.space, obj)
        elif obj.type == 'planet':
            vis.create_planet_image(ob.space, obj)
        else:
            raise AssertionError()


def save_file_dialog(obj):
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    out_filename = file.asksaveasfilename(filetypes=(("Text file", ".txt"),))
    inp.write_space_objects_data_to_file(out_filename, obj.space_objects)


def read_statistics_from_file():
    """
    Функция, считывающая данные из файла stats.txt
    """
    file_open = open('stats.txt', 'r')
    time = np.array([])
    x = np.array([])
    y = np.array([])
    vx = np.array([])
    vy = np.array([])
    lines = file_open.readlines()

    for line in lines:
        array = [i for i in line.split()]
        time = np.append(time, float(array[0]))
        x = np.append(x, float(array[3]))
        y = np.append(y, float(array[4]))
        vx = np.append(vx, float(array[5]))
        vy = np.append(vy, float(array[6]))

    file_open.close()

    return time, x, y, vx, vy


def plotting():
    """
    Функция, строящая графики по считанным данным
    """
    time, x, y, vx, vy = read_statistics_from_file()
    plt.grid(True)
    fig_1, ax_1 = plt.subplots()
    ax_1.plot(time, np.sqrt(vx ** 2 + vy ** 2))
    ax_1.set_title("График зависимости модуля скорости спутника от времени")
    ax_1.set_xlabel("t, c")
    ax_1.set_ylabel("V, м/c")
    fig_1.savefig("V(t).png")

    fig_2, ax_2 = plt.subplots()
    ax_2.plot(time, np.sqrt(x ** 2 + y ** 2))
    ax_2.set_title("График зависимости расстояния спутника до звезды от времени")
    ax_2.set_xlabel("t, c")
    ax_2.set_ylabel("L, м")
    fig_2.savefig("L(t).png")

    fig_3, ax_3 = plt.subplots()
    ax_3.plot(np.sqrt(x ** 2 + y ** 2), np.sqrt(vx ** 2 + vy ** 2))
    ax_3.set_title("График зависимости модуля скорости спутника \n от расстояния до звезды")
    ax_3.set_xlabel("L, м")
    ax_3.set_ylabel("V, м/c")
    fig_3.savefig("V(L).png")

    plt.show()


def main():
    """Главная функция главного модуля.
    Создаёт объекты графического дизайна библиотеки tkinter: окно, холст, фрейм с кнопками, кнопки.
    """
    var = Globals()

    print('Modelling started!')

    var.space.pack(side=tkinter.TOP)
    var.frame.pack(side=tkinter.BOTTOM)
    var.start_button.pack(side=tkinter.LEFT)

    var.time_step = tkinter.DoubleVar()
    var.time_step.set(1000)
    time_step_entry = tkinter.Entry(var.frame, textvariable=var.time_step)
    time_step_entry.pack(side=tkinter.LEFT)

    var.time_speed = tkinter.DoubleVar()
    scale = tkinter.Scale(var.frame, variable=var.time_speed, orient=tkinter.HORIZONTAL)
    scale.pack(side=tkinter.LEFT)

    load_file_button = tkinter.Button(var.frame, text="Open file...", command=lambda: open_file_dialog(var))
    load_file_button.pack(side=tkinter.LEFT)
    save_file_button = tkinter.Button(var.frame, text="Save to file...", command=lambda: save_file_dialog(var))
    save_file_button.pack(side=tkinter.LEFT)

    var.displayed_time = tkinter.StringVar()
    var.displayed_time.set(str(var.physical_time) + " seconds gone")
    time_label = tkinter.Label(var.frame, textvariable=var.displayed_time, width=30)
    time_label.pack(side=tkinter.RIGHT)

    open_file_dialog(var)

    execution(var)

    var.root.mainloop()
    print('Modelling finished!')


if __name__ == "__main__":
    main()
    plotting()
