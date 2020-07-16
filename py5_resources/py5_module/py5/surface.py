# -*- coding: utf-8 -*-
# *** FORMAT PARAMS ***
import functools
from typing import overload, Any  # noqa

from .methods import Py5Exception  # noqa
from .mixins.image import _check_pimage_cache_or_convert  # noqa
from .java_types import Py5Image  # noqa


py5surface_class_members_code = None  # DELETE


def _return_py5surface(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        return Py5Surface(f(self_, *args))
    return decorated


class Py5Surface:

    def __init__(self, psurface):
        self._instance = psurface


{py5surface_class_members_code}