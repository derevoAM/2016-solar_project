# coding: utf-8
# license: GPLv3

from solar_objects import Star, Planet


def read_space_objects_data_from_file(input_filename):
    """Cчитывает данные о космических объектах из файла, создаёт сами объекты
    и вызывает создание их графических образов

    Параметры:

    **input_filename** — имя входного файла
    """

    objects = []
    with open(input_filename) as input_file:
        for line in input_file:
            if len(line.strip()) == 0 or line[0] == '#':
                continue  # пустые строки и строки-комментарии пропускаем
            object_type = line.split()[0].lower()
            if object_type == "star":
                star = Star()
                parse_star_parameters(line, star)
                objects.append(star)
            elif object_type == "planet":
                planet = Planet()
                parse_planet_parameters(line, planet)
                objects.append(planet)
            else:
                print("Unknown space object")

    return objects


def parse_star_parameters(line, star):
    """Считывает данные о звезде из строки.
    Входная строка должна иметь слеюущий формат:
    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Здесь (x, y) — координаты зведы, (Vx, Vy) — скорость.
    Пример строки:
    Star 10 red 1000 1 2 3 4

    Параметры:

    **line** — строка с описание звезды.
    **star** — объект звезды.
    """
    star.m = float(line.split()[3])
    star.x = float(line.split()[4])
    star.y = float(line.split()[5])
    star.Vx = float(line.split()[6])
    star.Vy = float(line.split()[7])
    star.R = float(line.split()[1])
    star.color = line.split()[2]


def parse_planet_parameters(line, planet):
    """Считывает данные о планете из строки.
    Предполагается такая строка:
    Входная строка должна иметь слеюущий формат:
    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Здесь (x, y) — координаты планеты, (Vx, Vy) — скорость.
    Пример строки:
    Planet 10 red 1000 1 2 3 4

    Параметры:

    **line** — строка с описание планеты.
    **planet** — объект планеты.
    """
    planet.m = float(line.split()[3])
    planet.x = float(line.split()[4])
    planet.y = float(line.split()[5])
    planet.Vx = float(line.split()[6])
    planet.Vy = float(line.split()[7])
    planet.R = float(line.split()[1])
    planet.color = line.split()[2]


def write_space_objects_data_to_file(output_filename, space_objects):
    """Сохраняет данные о космических объектах в файл.
    Строки должны иметь следующий формат:
    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>
    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Параметры:

    **output_filename** — имя входного файла
    **space_objects** — список объектов планет и звёзд
    """
    with open(output_filename, 'w') as out_file:
        for obj in space_objects:
            out_file.writelines(
                ("{} {} {} {} {} {} {} {} \n".format(obj.type, obj.R, obj.color, obj.m, obj.x, obj.y, obj.Vx,
                                                     obj.Vy)).title())


def write_statistics(obj):
    """
    Функция, записывающая в файл значения координаты и скорости спутника
    :param obj: объект класса Globals
    """
    line = ""
    body = obj.space_objects[1]
    line += str(obj.displayed_time.get()) + " " + str(body.x) + " " + str(body.y) + " " + str(
        body.Vx) + " " + str(body.Vy) + "\n"
    if obj.flag == 0:
        with open("stats.txt", 'w') as out_file:
            out_file.write(line)
        obj.flag = 1
    else:
        with open("stats.txt", 'a') as out_file:
            out_file.write(line)
    return obj


if __name__ == "__main__":
    print("This module is not for direct call!")
