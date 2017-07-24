# coding=utf-8
import exceptions
from PIL import Image, ImageEnhance
from django.conf import settings

from livecamsbay.settings import IMG_SIZE


def count_new_size(size, original_size=IMG_SIZE['original']):
    """
    Расчет новых размеров картинки относительно IMG_SIZE['original']
    """
    new_size = min(float(size[0]) / original_size[0], float(size[1]) / original_size[1])
    return tuple(int(x / new_size) for x in size)


def count_crop(current_size, original_size=IMG_SIZE['original']):
    """
    Расчет размеров картинки с учетом crop
    """
    return tuple((current_size[x] - original_size[x]) / 2 + original_size[x] * y for y in range(2) for x in range(2))


def resize_image(image, new_size=None, crop=True):
    """
    Ресайз изображения
    """
    resized = image.resize(new_size or count_new_size(image.size), Image.ANTIALIAS)
    box = count_crop(resized.size)
    return resized.crop(box=box) if crop else resized


def add_watermark(image, watermark, opacity=1, wm_interval=0):
    """
    Добавление водного знака картинке
    """
    assert 0 <= opacity <= 1
    if opacity < 1:
        if watermark.mode != 'RGBA':
            watermark = watermark.convert('RGBA')
        else:
            watermark = watermark.copy()
        alpha = watermark.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        watermark.putalpha(alpha)
    layer = Image.new('RGBA', (image.size), (0, 0, 0, 0))
    for y in range(0, image.size[1], watermark.size[1] + wm_interval):
        for x in range(0, image.size[0], watermark.size[0] + wm_interval):
            layer.paste(watermark, (x, y))
    return Image.composite(layer, image, layer)


def get_thumb_url(f):
    """
    Создание превьюшки файла.
    Если картинка, то она ресайзится.
    Если другой файл, то превьюшка выбирается из settings.FILE_MIME_TYPE
    """
    if hasattr(f, 'content_type'):
        content_type = f.content_type
    else:
        import mimetypes
        filaname = str(f)
        content_type = mimetypes.guess_type(filaname)[0]
        # на случай, если ранее загруженная картинка не найдена на диске,
        # открываем деволтную картинку
        try:
            f = open(filaname, 'r')
        except exceptions.IOError:
            f = open(settings.IMAGE_NOT_FOUND, 'r')

    if content_type.startswith('image'):
        import os
        from easy_thumbnails.files import get_thumbnailer

        thumbnailer = get_thumbnailer(f, relative_name='preview/' + os.path.basename(f.name))
        thumb_url = thumbnailer.get_thumbnail(settings.PREVIEW_THUMBNAIL_OPTIONS).url
    else:
        thumb_url = settings.FILE_MIME_TYPE.get(content_type)
        thumb_url = thumb_url() if hasattr(thumb_url, '__call__') else thumb_url
    return thumb_url
