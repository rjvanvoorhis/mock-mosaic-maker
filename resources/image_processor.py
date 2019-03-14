import os
import json
import requests
from helpers import Environment, ImageStreamer, make_file_path
from photomosaic.scripts import create_photomosaic
from PIL import Image
import logging


class ImageProcessor(object):
    def __init__(self, username, image_data, filename):
        self.logger = logging.getLogger(__name__)
        self.logger.debug(username, filename)
        self.env = Environment()
        self.extension = 'gif' if filename.endswith('gif') else 'jpg'
        self.img_file = make_file_path(self.extension)
        self.progress_file = make_file_path('jpg') if self.extension == 'jpg' else None
        self.alternate_file = make_file_path('gif') if self.extension == 'jpg' else None
        self.gallery_url = f'{self.env.mosaic_api_url}/users/{username}/gallery'
        self.pending_url = f'{self.env.mosaic_api_url}/users/{username}/pending_json'
        self.streamer = ImageStreamer()
        self.auth = self.env.authorization
        with open(self.img_file, 'wb') as fn:
            fn.write(self.streamer.decode_data(image_data))

    def process_image(self, tile_size=8, enlargement=1):
        if self.extension == 'gif':
            self.logger.debug(f'Processing gif with enlargement {enlargement} and tile_size {tile_size}')
            self.handle_gif(tile_size, enlargement)
        else:
            self.logger.debug(f'Processing gif with enlargement {enlargement} and tile_size {tile_size}')
            self.handle_image(tile_size, enlargement)
        self.post_image()
        msg = f'uploaded {self.img_file}{"" if not self.alternate_file else "and progress gif " + self.alternate_file}'
        self.logger.debug(msg)

        return {'message': msg}

    def handle_image(self, tile_size=8, enlargement=1):
        create_photomosaic(self.img_file, output_file=self.progress_file, save_intermediates=False,
                           alternate_filename=None, tile_size=tile_size, enlargement=enlargement)
        img = Image.open(self.progress_file)
        self.load_progress(img, filename=self.progress_file, progress=0.5, total_frames=2)
        create_photomosaic(self.img_file, output_file=self.img_file, save_intermediates=True,
                           alternate_filename=self.alternate_file, tile_size=tile_size, enlargement=enlargement)

    def handle_gif(self, tile_size=8, enlargement=1):
        create_photomosaic(self.img_file, output_file=self.img_file, save_intermediates=True, alternate_filename=None,
                           progress_callback=self.gif_callback, tile_size=tile_size, enlargement=enlargement)

    def post_image(self):
        files = {
            'mosaic_file': (self.img_file, open(self.img_file, 'rb'), f'image/{self.extension}'),
        }
        if self.alternate_file is not None:
            files['alternate_file'] = (self.alternate_file, open(self.alternate_file, 'rb'), 'image/gif')
        requests.post(self.gallery_url, files=files, headers={'Authorization': self.auth})
        for fn, cm, mimetype in files.values():
            cm.close()
        self.cleanup()

    def cleanup(self):
        for fp in [self.img_file, self.alternate_file, self.progress_file]:
            if fp is not None and os.path.exists(fp):
                os.remove(fp)

    def gif_callback(self, idx, item):
        frame_directory = os.path.dirname(item.output_file)
        total_frames = len(os.listdir(frame_directory)) if os.path.exists(frame_directory) else idx
        progress = float(idx / max(1, total_frames))
        self.load_progress(item.image_data.img, item.output_file, progress, total_frames)

    def load_progress(self, img, filename, progress, total_frames, max_size=500):
        img = img.copy()
        img.thumbnail((max_size, max_size))
        file_obj = self.streamer.create_file_object(img, filename)
        payload = {
            'progress': progress,
            'total_frames': total_frames
        }
        requests.patch(self.pending_url, data=payload, files={'frame': file_obj},
                       headers={'Authorization': self.auth})
        self.logger.debug(f'Sent frame with progress {progress} to {self.pending_url}')
        self.streamer.flush()

