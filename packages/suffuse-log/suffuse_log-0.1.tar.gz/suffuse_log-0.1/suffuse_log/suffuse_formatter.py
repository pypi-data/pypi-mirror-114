import logging
from collections import OrderedDict
from typing import Dict, Tuple

from .ansi_config import AnsiConfig


class SuffuseFormatter(logging.Formatter):
    def __init__(
        self,
        log_ansi_config: "OrderedDict[str, AnsiConfig]",
        header_delim: str = " | ",
        header_delim_styles: Tuple[str, ...] = ("dim_style",),
        date_format: str = "%Y-%m-%d %H:%M:%S",
    ):

        self.log_ansi_config = log_ansi_config

        # we color the delimiters before we pass them into the parent class
        styled_delimiter = AnsiConfig.style(text=header_delim, styles=header_delim_styles)
        _fmt = styled_delimiter.join(self.log_ansi_config.keys())
        _fmt = _fmt.replace(")d", ")s")
        _fmt = _fmt.replace(")f", ")s")

        super().__init__(fmt=_fmt, datefmt=date_format)

        # to optimize run times when given "*", tell AnsiConfig which attributes this formatter expects
        if not AnsiConfig.formatter_specific_attributes:
            AnsiConfig.formatter_specific_attributes = tuple(k[2:-2] for k in self.log_ansi_config)

    def formatMessage(self, record: logging.LogRecord) -> str:
        """
        Override the base method to stylize the input values. This is the main entry point into our logic.

        NOTE - The [2:-2] notation recurring here is transforming %(attribute)s to attribute.

        Args:
            record (logging.LogRecord): the LogRecord of the log about to be emitted

        Returns:
            str: the log message to be emitted
        """

        # for the attributes in the log_ansi_config, determine how we style the corresponding values
        styled_attributes: Dict[str, str] = {}
        for attr, ansi_config in self.log_ansi_config.items():
            attr_name = attr[2:-2]
            if ansi_config:
                ansi_config.modify(record=record, attr=attr_name, styled_attributes=styled_attributes)

        # for any attributes we did not style, set those values here
        for attr in self.log_ansi_config:
            attr_name = attr[2:-2]
            if attr_name not in styled_attributes:
                styled_attributes[attr_name] = AnsiConfig.get_attr(record, attr_name)

        return self._fmt % styled_attributes  # type: ignore


def defaultConfig(log_level_no: int = 20):
    bright = "bright_style"

    format_date = "%Y-%m-%d %H:%M:%S"

    format_ansi = OrderedDict()
    format_ansi["%(asctime)s"] = AnsiConfig()
    format_ansi["%(levelname)s"] = AnsiConfig(
        {
            "DEBUG": ("green_fore", "dim_style"),
            "INFO": ("blue_fore",),
            "WARNING": ("yellow_fore",),
            "ERROR": (bright, "red_fore"),
            "CRITICAL": (bright, "red_fore"),
        },
        ("levelname", "message", "name", "module", "lineno"),
    )

    format_ansi["%(name)s"] = AnsiConfig()
    format_ansi["%(module)s"] = AnsiConfig()
    format_ansi["%(lineno)s"] = AnsiConfig()

    format_ansi["%(message)s"] = AnsiConfig(
        {
            "*error*": (bright,),
            "*important*": (bright,),
            "*critical*": (bright,),
            "*warn*": (bright,),
            "*alert*": (bright,),
        },
        case_sensitive_glob=False,
    )

    logging.basicConfig(level=log_level_no)

    suffuse_formatter = SuffuseFormatter(
        log_ansi_config=format_ansi,
        date_format=format_date,
    )

    handler = logging.StreamHandler()
    handler.setFormatter(suffuse_formatter)

    logger = logging.getLogger()
    logger.handlers.clear()
    logger.addHandler(handler)

    return logger
