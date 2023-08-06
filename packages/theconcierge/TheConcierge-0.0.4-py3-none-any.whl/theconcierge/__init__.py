__title__ = "theconcierge"
__version__ = "0.0.4"
__author__ = "Luigi Malaguti"
__copyright__ = "Copyright (c) 2021 Luigi Malaguti"
__license__ = 'GPLv3'


from .main.theconcierge import TheConcierge
from .settings.config import Config


__all__ = [
    "TheConcierge",
    "Config"
]
