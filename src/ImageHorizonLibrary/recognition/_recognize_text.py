# -*- coding: utf-8 -*-
from os.path import isfile

import pyautogui as ag
from robot.api import logger as LOGGER
from PIL import Image

from ..errors import InvalidImageException, OCRException

try:
    import pytesseract
    from pytesseract import Output
except ImportError:
    pytesseract = None


class _RecognizeText(object):
    '''
    Additional OCR keywords. Requires the optional dependency
    ``pytesseract`` plus a working Tesseract binary on PATH.
    '''

    def _ocr_data(self, image, lang):
        # image_to_data returns a per-word table including a confidence
        # column ('conf', 0..100; -1 for non-text blocks).
        return pytesseract.image_to_data(image, lang=lang,
                                         output_type=Output.DICT)

    def _filter_text(self, data, confidence):
        words = []
        for text, conf in zip(data['text'], data['conf']):
            text = text.strip()
            if not text:
                continue
            try:
                conf = float(conf)
            except (TypeError, ValueError):
                continue
            if confidence is None or conf >= confidence:
                words.append(text)
        return ' '.join(words)

    def _read_text(self, image, confidence, lang):
        if not self.has_ocr:
            raise OCRException(
                'OCR is not available. Install the optional dependency with '
                '`pip install pytesseract` and make sure the Tesseract binary '
                'is installed and on PATH.')
        if confidence is None:
            confidence = self.ocr_confidence
        if confidence is not None:
            confidence = float(confidence)
        data = self._ocr_data(image, lang)
        return self._filter_text(data, confidence)

    def get_text_from_image(self, reference_image, confidence: float = None, lang: str = 'deu'):
        '''
        Reads text from a reference image file using OCR.

        ``reference_image`` is normalized as described in
        `Reference image names`.

        ``confidence`` is a percentage (0-100). Words recognized with a lower
        OCR confidence are discarded. If not given, the library-level
        ``ocr_confidence`` is used (no filtering by default).

        ``lang`` is the Tesseract language code (e.g. ``eng``, ``deu``).
        Default is german / ``deu``.

        Returns the recognized text as a string.
        v1.3 Keyword
        '''
        path = self._normalize(reference_image)
        if not isfile(path):
            raise InvalidImageException(
                f'Image path not found2: "{path}".')
        text = self._read_text(Image.open(path), confidence, lang)
        LOGGER.info(f'OCR read from "{reference_image}": {text}')
        return text


    def get_text_from_location(self, width: int, height: int, location: tuple = None, x_offset: int = 0, y_offset: int = 0,
                               confidence: float = None, lang: str = 'eng'):
        '''Reads text from a rectangular region of the screen using OCR.
        Takes a screenshot via PyAutoGUI.

        ``width`` and ``height`` define the region in
        pixels from the current or given location.

        ``location`` is used as before, *with* offset in both planes.

        ``x_offset`` (int): offset on the x-plane. Positive is offset to the right, negative to the left
        ``y_offset`` (int): offset on the y-plane. Positive is offset to the top, negative to the bottom

        ``confidence`` and ``lang`` behave as in `Get Text From Image`.

        Returns the recognized text as a string.
        v1.3 Keyword
        '''
        # location can be none
        if location:
            x, y = self._get_advanced_location(location, x_offset, y_offset)
        else:
            # get cur. location
            x0, y0 = ag.position()
            x, y = self._get_advanced_location((x0, y0), x_offset, y_offset)

        region = (x, y, int(width), int(height))
        text = self._read_text(ag.screenshot(region=region), confidence, lang)
        LOGGER.info(f'OCR read from region {region}: {text}')
        return text
