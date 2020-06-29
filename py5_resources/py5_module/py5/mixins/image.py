import io
from pathlib import Path
import weakref
from typing import overload, NewType, Any, Callable, Union, Dict, List  # noqa

from PIL import Image
import cairosvg

from ..converter import Converter


class ImageMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._py5applet = kwargs['py5applet']
        self._converter = Converter(self._py5applet)
        self._weak_image_refs = []

    # TODO: what about alpha mask images?
    # TODO: are there other PImage functions I should be paying attention to?

    # *** BEGIN METHODS ***

    def flush_image_cache(self) -> None:
        self._weak_image_refs = []

    @overload
    def image(self, img: Any, a: float, b: float, cache: bool = False) -> None:
        """$class_image"""
        pass

    @overload
    def image(self, img: Any, a: float, b: float, c: float, d: float, cache: bool = False) -> None:
        """$class_image"""
        pass

    def image(self, *args, cache: bool = False) -> None:
        """$class_image"""
        pimage = self._check_cache_or_convert(args[0], cache)
        self._py5applet.image(pimage, *args[1:])

    def create_image(self, mode: str, width: int, height: int, color: Any) -> Image.Image:
        """$class_create_image"""
        return Image.new(mode, (width, height), color)

    def load_image(self, filename: Union[str, Path]) -> Image.Image:
        """$class_load_image"""
        filename = Path(filename)
        if filename.suffix.lower() == '.svg':
            with open(filename, 'r') as f:
                return Image.open(io.BytesIO(cairosvg.svg2png(file_obj=f)))
        else:
            return Image.open(filename)

    def texture(self, image: Any, cache: bool = False) -> None:
        """$class_texture"""
        pimage = self._check_cache_or_convert(image, cache)
        self._py5applet.texture(pimage)

    def _check_cache_or_convert(self, image, cache):
        pimage = None
        cache_hit = False

        if cache:
            pimage = self._check_cache(image)
            if pimage is not None:
                cache_hit = True

        if pimage is None:
            pimage = self._converter.to_pimage(image)

        if cache and not cache_hit:
            self._store_cache(image, pimage)

        return pimage

    def _check_cache(self, image):
        if isinstance(image, tuple):
            image = image[0]
        for ref, pimage in reversed(self._weak_image_refs):
            if ref() is None:
                self._weak_image_refs.remove((ref, pimage))
            if image is ref():
                return pimage
        return None

    def _store_cache(self, image, pimage):
        if isinstance(image, tuple):
            image = image[0]
        self._weak_image_refs.append((weakref.ref(image), pimage))