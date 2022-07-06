#!/usr/bin/python
#coding: utf-8

import os
import logging
import subprocess
import shelve

from datetime import datetime
from django.conf import settings
from core.models import Employee

logger = logging.getLogger(__name__)


def mm(points):
    """
    Convert postscript points to millimetres. 1 pt = 25.4/72 mm
    :param points: (float) points
    :return: (float) millimetres
    """
    return int(round(float(points)/72*25.4))


def pt(mm):
    """
    :param mm: (float)
    :return: points (float)
    """
    return int(float(mm)*72/25.4)


def humansize(nbytes):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    if nbytes == 0: return '0 B'
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])


def dict_to_multiline(dic):
    """
    Функция преобразует словарь в текстовый объект, где каждая строка вида key: value1 value.
    Используется, например, для вывода колоранотов в html
    :param dic(dic): словарь
    :return: text(str)
    """
    text = ''
    try:
        for k, v in dic.items():
            text += str(k)+': '
            for i in v:
                text += i + ' '
            text += "\n"
    except AttributeError:
        # исключение возникает, если файл не сигновский. dic в этом случае - пустая строка
        # возвращается также пустая строка
        pass
    return text



def error_text(status, e):
    if status:
        text = "OK"
    else:
        if e:
            text = e
        else:
            text = "Unknown error"
    return text


def reduce_image(infile, outfile, new_width):
    """
    Эта функция пропорционально уменьшает изображение до ширины width
    :param source: путь к исходному изображению
    :param target: путь к уменьшенному изображению
    :param width: до какой ширины уменьшать (в пикселах)
    :return:
    """
    from PIL import Image

    if infile != outfile:
        try:
            im = Image.open(infile)
            height, width = im.size
            new_height = int(new_width * height / width)
            im = im.resize((new_height, new_width), Image.ANTIALIAS)
            im.save(outfile)
        except IOError as e:
            logger.error("cannot create thumbnail for {} with exception: {}".format(infile, e))


def colorant_to_string(pdf_colors):
    """
    :param pdf_colors: Это словарь, ключ - номер страницы, значение - список из строк-названий красок
    :return: short_colors: строка, краткий список красок на первом пейдже
    """
    if not pdf_colors :
        return None

    cmyk = ['Cyan', 'Magenta', 'Yellow', 'Black']

    # colors == ['PANTONE_Reflex_Blue_C', 'Cyan', 'Magenta', 'PANTONE_246_C']
    colors = pdf_colors[1]

    #убираем из пантонов слово Pantone и знаки подчеркивания
    inks = []
    for separations in colors:
        parts = separations.split("_")
        if 'PANTONE' in parts:
            parts.remove('PANTONE')
        newcolor = ''.join(parts)
        inks.append(newcolor)

    # inks == ['ReflexBlueC', 'Cyan', 'Magenta', '246C']

    replaced_colors = ''
    #если краски - только CMYK
    if set(inks) == set(cmyk):
        # то возвращаем пустую строку - в название файла никакая инфа не добавится
        # logger.debug('only cmyk')
        short_colors = ''
    else:
        #иначе заменяем краски Cyan Magenta Yellow Black на их заглавные буквы и ставим их в начало строки
        logger.debug('inks {}'.format(inks))
        for ink in cmyk:
            if ink in inks:
                inks.remove(ink)
                replaced_colors += ink[0]
        if replaced_colors:
            inks.insert(0, replaced_colors)

        # inks == ['CM', 'ReflexBlueC', '246C']

        # объеденяем список в строку через дефис и добавляем спереди подчеркивание
        short_colors = '_' + '-'.join(inks)
    return short_colors


def get_jpeg_path():
    """
    Джипеги хранятся в директориях соответственно их году. Фунцкция убеждается, что эта директория существует,
    и возвращает путь на нее
    proof_subpath - путь от setting.MEDIA_ROOT - это значение сохраняется в базе
    proof_path - абсолютный путь
    :param pdf:
    :return:
    """
    current_year = str(datetime.now().year)
    proof_subpath = os.path.join('proof', current_year)
    proof_path = os.path.join(settings.MEDIA_ROOT, proof_subpath)
    if not os.path.exists(proof_path):
        os.makedirs(proof_path)
    return proof_subpath, proof_path


def get_bbox(fname):
    """
    Функция определяет координаты значимого изображения. С помощью этих координат можно обрезать белые поля.
    Функция возвращает словарь, где ключ - номер страницы, значения - список bbox [x1, y1, x2, y2] -
    координаты нижнего левого и верхнего правого углов изображения в пунктах.
    """
    args = ["gs"]
    args += ["-o", "%stdout%"]
    args += ["-dQUIET"]
    args += ["-sDEVICE=bbox"]
    args += ["-f", fname]

    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout_data, stderr_data) = p.communicate(None)

    # remove %%BoundingBox, retain only %%HiResBoundingBox
    gs_result = stderr_data.splitlines()
    cleaned_result = [x for x in gs_result if '%%HiResBoundingBox' in x]

    bbox = {}
    for num, line in enumerate(cleaned_result, 1):
        data = line.split()
        if data[0] == "%%HiResBoundingBox:":
            bbox[num] = [ float(s) for s in data[1:5] ]

    return bbox


def read_shelve():

    shelf = settings.SHELF
    d = shelve.open(shelf, flag='c')

    try:
        import_mode = d['IMPORT_MODE']
    except KeyError:
        d['IMPORT_MODE'] = False
        import_mode = False

    d.close()
    return import_mode


def write_shelve(mode):
    shelf = settings.SHELF
    d = shelve.open(shelf, flag='c')
    d['IMPORT_MODE'] = mode
    d.close()


def emergency_termination(pdf, e):
    """
    Отсылает уведомление о проишествии, выполняет очистку и экстренно останавливает программу
    :return: 
    """
    message = e
    receivers = Employee.objects.filter(user__is_superuser=True).filter(telegram_notify=True)
    logger.error('EMERGENCY TERMINATION: {}'.format(e))
    pdf.cleaning_temps()
    exit()
