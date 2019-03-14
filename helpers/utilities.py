__all__ = ['Environment', 'ImageStreamer', 'make_file_path']

import binascii
import os
import time
from io import BytesIO
from flask import request
from copy import deepcopy


def make_file_path(extension='jpg'):
    return f'{str(time.time()).replace(".", "")}.{extension}'


class Environment(object):
    def __init__(self):
        self.default = {
        }
        self.default.update(os.environ)

    def __getattr__(self, key):
        environ = deepcopy(self.default)
        for k, v in request.headers.items():
            environ[k.lower()] = v
        return {k.lower().replace('-', '_').replace('x_', ''): v for k, v in environ.items()}.get(key)


class ImageStreamer(object):
    def __init__(self):
        self.streamer = BytesIO()

    def flush(self):
        self.streamer.close()
        self.streamer = BytesIO()
    @staticmethod
    def encode_data(raw_data):
        return binascii.b2a_base64(raw_data).decode()

    @staticmethod
    def decode_data(encoded_data):
        return binascii.a2b_base64(encoded_data)

    @staticmethod
    def get_image_format(img, img_format):
        img_format = img_format if img_format else img.format
        img_format = img_format if img_format else 'jpg'
        return img_format

    def dumps(self):
        self.streamer.seek(0)
        raw_data = self.streamer.read()
        self.streamer.flush()
        return self.encode_data(raw_data)

    def convert(self, img, img_format=None):
        img_format = self.get_image_format(img, img_format)
        img.save(self.streamer, format=img_format)
        return self.dumps()

    def create_file_object(self, img, filename):
        img_format = self.get_image_format(img, None)
        ext = 'GIF' if img_format.lower() == 'gif' else 'JPEG'
        img.save(self.streamer, ext)
        return filename, self.streamer.getvalue(), f'image/{ext}'

