"""
Files functionality for the API
"""

import os
import re
import base64
import string
import random
import json
import binascii

import requests
from PIL import Image, ExifTags, UnidentifiedImageError

from ..errors import ErrorUpload


with open('sets.json', 'r') as file:
    sets = json.loads(file.read())
    SIDE_OPTIMIZED = sets['side_optimized']


def get_file(url, num):
    """ Check existence the file by name """

    for i in os.listdir(f'../data/load/{url}/'):
        if re.search(rf"^{str(num)}.", i):
            return i

    return None

def max_image(url):
    """ Next image ID """

    files = os.listdir(url)
    count = 0

    for i in files:
        j = re.findall(r'\d+', i)
        if len(j) and int(j[0]) > count:
            count = int(j[0])

    return count+1

def load_image(data, encoding='base64', file_format='png'):
    """ Upload image """

    if data is None:
        return data

    if encoding != 'bytes':
        try:
            match = re.search(r'^\w+\.\w+$', data)
        except TypeError:
            raise ErrorUpload('image')

        if match:
            return data

    url = '../data/load/'
    url_opt = url + 'opt/'

    if encoding == 'base64':
        try:
            file_format = re.search(r'data:image/.+;base64,', data).group()[11:-8]
            b64 = data.split(',')[1]
            data = base64.b64decode(b64)
        except (AttributeError, binascii.Error):
            raise ErrorUpload('image')

    file_id = max_image(url)
    offset = '0' * max(0, 10-len(str(file_id)))
    payload = ''.join(random.choice(string.ascii_lowercase) for _ in range(6))
    file_id = f'{offset}{file_id}{payload}'
    file_format = file_format.lower()
    file_name = f'{file_id}.{file_format}'
    url += file_name
    url_opt += file_name

    # TODO: check image data before save
    with open(url, 'wb') as file:
        try:
            file.write(data)
        except TypeError:
            raise ErrorUpload('image')

    # EXIF data
    # pylint: disable=protected-access

    try:
        try:
            img = Image.open(url)
        except UnidentifiedImageError:
            raise ErrorUpload('image')

        orientation = None

        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break

        exif = dict(img._getexif().items())

        if exif[orientation] == 3:
            img = img.transpose(Image.ROTATE_180)
        elif exif[orientation] == 6:
            img = img.transpose(Image.ROTATE_270)
        elif exif[orientation] == 8:
            img = img.transpose(Image.ROTATE_90)

        img.save(url)
        img.close()

    except (AttributeError, KeyError, IndexError):
        pass

    # Optimized version
    if SIDE_OPTIMIZED:
        img = Image.open(url)

        if img.size[0] > img.size[1]:
            hpercent = (SIDE_OPTIMIZED / float(img.size[1]))
            wsize = int(float(img.size[0]) * float(hpercent))
            img = img.resize((wsize, SIDE_OPTIMIZED), Image.ANTIALIAS)
        else:
            wpercent = (SIDE_OPTIMIZED / float(img.size[0]))
            hsize = int(float(img.size[1]) * float(wpercent))
            img = img.resize((SIDE_OPTIMIZED, hsize), Image.ANTIALIAS)

        img.save(url_opt)

    # Response
    return file_name

def reimg(text):
    """ Load all images images from the text to the server """

    if text is None:
        return text

    # Base64
    while True:
        fragment = re.search(
            r'<img [^>]*src=[^>]+data:image/\w+;base64,[^\'">]+=[^>]+>', text
        )

        if fragment is None:
            break

        first, _ = fragment.span()
        meta_fragment = re.search(
            r'data:image/\w+;base64,[^\'">]+=', fragment.group()
        )

        meta_first, meta_last = meta_fragment.span()
        data = load_image(meta_fragment.group())
        text = text[:first+meta_first] \
               + '/load/' + data \
               + text[first+meta_last:]

    # External links
    while True:
        fragment = re.search(
            r'<img [^>]*src=[^\'">]*[\'"][^\'">]*http[^\'">]+[^>]*>', text
        )

        if fragment is None:
            break

        first, _ = fragment.span()
        meta_fragment = re.search(
            r'http[^\'">]+', fragment.group()
        )

        meta_first, meta_last = meta_fragment.span()
        link = meta_fragment.group()
        data = requests.get(link).content

        if '.' in link:
            file_format = link.split('.')[-1]

            if (
                'latex' in file_format
                or '/' in file_format
                or len(file_format) > 5
            ):
                file_format = 'png'

        else:
            file_format = None

        data = load_image(data, encoding='bytes', file_format=file_format)
        text = text[:first+meta_first] \
               + '/load/' + data \
               + text[first+meta_last:]

    return text
