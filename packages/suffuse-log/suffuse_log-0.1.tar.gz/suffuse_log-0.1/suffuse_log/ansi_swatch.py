import typing
from types import MappingProxyType

import colorama.ansi as ca

ANSI_MAP: typing.Dict[str, str] = {}
STYLE_OFF = "\033[0m"


def default_ansi_swatch():
    """
    Builds the default ansi swatch dictionary from the colorama library. Handles the conversion
    of dynamically built attributes to human-readable strings.
    """
    colorama_ansi_map = {"Fore": ca.Fore, "Back": ca.Back, "Style": ca.Style}

    # unpack class design and assign ansi codes to names
    output_ansi_map = {}
    for class_name, ansi_class in colorama_ansi_map.items():
        for ansi_name, ansi_code in ansi_class.__dict__.items():
            breadcrumbed_name = f"{ansi_name}_{class_name}".lower()  # i.e. 'red_fore', 'blue_back', 'bright_style'
            output_ansi_map[breadcrumbed_name] = ansi_code

    return MappingProxyType(output_ansi_map)


def load_ansi_map(ansi_map: typing.Dict[str, str] = None):
    """Sets the global ansi map dictionary. Exists to allow a user to supply their own string to ansi code maps.

    Args:
        ansi_mao (typing.Dict[str, str], optional): User-supplied ansi map. Defaults to None.
    """
    global ANSI_MAP
    ANSI_MAP = ansi_map or default_ansi_swatch()


load_ansi_map()
