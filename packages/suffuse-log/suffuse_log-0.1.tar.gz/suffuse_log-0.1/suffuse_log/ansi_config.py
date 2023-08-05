import fnmatch
import logging
import re
from typing import Callable, Dict, Optional, Tuple, Union

from .ansi_swatch import ANSI_MAP, STYLE_OFF

ANSI_STYLES = Tuple[str, ...]
MAP_VALUE_COLOR = Union[Dict[str, ANSI_STYLES], Dict[str, Tuple[str]]]
MAP_ATTRIBUTE_COLOR = ANSI_STYLES
MAP_CALLABLE_RESULT_COLOR = Dict[Callable, ANSI_STYLES]


class AnsiConfig:
    formatter_specific_attributes = (
        "name",
        "levelno",
        "levelname",
        "pathname",
        "filename",
        "module",
        "lineno",
        "funcName",
        "created",
        "asctime",
        "msecs",
        "relativeCreated",
        "thread",
        "threadName",
        "process",
        "message",
    )

    @staticmethod
    def style(text: str, styles: Tuple[str, ...]) -> str:
        """
        Where the actual styling takes place. Given a string and a list of ansi_map keys,
        will stylize the input string using the corresponding ansi_map values.

        Args:
            text (str): Value to be formatted
            styles (Tuple[str]): List of ansi_map keys that correspond to ansi codes.

        Returns:
            str: the ansi-styled string
        """
        try:
            if styles:
                ansi_prefix = "".join([ANSI_MAP[style] for style in styles])
                return f"{ansi_prefix}{text}{STYLE_OFF}"
            else:
                return text
        except KeyError:
            raise KeyError(
                "Provided ansi key doesn't exist. Check the attribute is spelled correctly, it exists, or the global ansi map is configured properly."
            )

    @staticmethod
    def get_attr(record: logging.LogRecord, attr: str) -> str:
        """Given a log record, extract the datapoint we need to ansi style.

        Args:
            record (logging.LogRecord): Log record of the message about to be emitted.
            attr (str): String name of the attribute to fetch

        Returns:
            str: value of the log record's attribute
        """
        return record.__dict__[attr]

    def __init__(
        self,
        match_to_color_map: Optional[Union[MAP_VALUE_COLOR, MAP_ATTRIBUTE_COLOR, MAP_CALLABLE_RESULT_COLOR]] = None,
        target_attributes: Tuple[str, ...] = tuple(),
        case_sensitive_glob=True,
    ):

        self.match_to_color_map = match_to_color_map
        self.target_attributes = target_attributes

        self.case_sensitive_glob = case_sensitive_glob

    def all_attributes(self) -> Tuple[str, ...]:
        """
        Return the formatter-specific attributes. Is initiatilized as all possible attributes,
        but the SuffuseFormatter overwrites depending on the log_ansi_map it is supplied.

        Returns:
            Tuple[str]: logger attribute names
        """
        return self.formatter_specific_attributes

    def modify(self, record: logging.LogRecord, attr: str, styled_attributes: Dict[str, str]):
        """Given a log record, modify the formatter's styled_attribute dictionary to contain the ansi-styled values.

        If no target attributes are provided, it is assumed that we are modifying the current iterable key. If "*" is provided,
        then all format fields declared will be ansi styled.

        Args:
            record (logging.LogRecord): Log record of the message about to be emitted.
            attr (str): String name of the attribute to fetch
            styled_attributes (Dict[str, str]): dictionary defined in the formatMessage method of the SuffuseFormatter.
        """
        if self.target_attributes == ("*",):
            self.target_attributes = self.all_attributes()

        if isinstance(self.match_to_color_map, tuple):
            self._handle_tuple(record, attr, styled_attributes)

        elif isinstance(self.match_to_color_map, dict):
            self._handle_dictionary(record, attr, styled_attributes)

        else:
            raise TypeError(f"Input type '{type(self.match_to_color_map)}' is not supported.")

    def _handle_dictionary(self, record: logging.LogRecord, attr: str, styled_attributes: Dict[str, str]):
        """If the AnsiConfig is provided with a dictionary match_to_color_map, then the logic specific to processing
        that format exists here. It accounts for glob formatting and callable invoking.

        If no target attributes are provided, it is assumed that we are modifying the current iterable key.

        Args:
            record (logging.LogRecord): Log record of the message about to be emitted.
            attr (str): String name of the attribute to fetch
            styled_attributes (Dict[str, str]): dictionary defined in the formatMessage method of the SuffuseFormatter.
        """
        target_attributes = self.target_attributes or (attr,)
        value = self.get_attr(record, attr)

        for k, v in self.match_to_color_map.items():  # type: ignore
            if isinstance(k, str):
                if self._is_glob_match(pattern=k, value=value):
                    self._modify_target_attributes(record, target_attributes, styled_attributes, v)

            elif isinstance(k, callable):  # type: ignore
                if callable(value):
                    self._modify_target_attributes(record, target_attributes, styled_attributes, v)
            else:
                raise TypeError(f"Currently only string (glob patterns) or callables are supported as keys here.")

    def _handle_tuple(self, record: logging.LogRecord, attr: str, styled_attributes: Dict[str, str]):
        """If the AnsiConfig is provided with a tuple match_to_color_map, then the logic specific to processing
        that format exists here. A tuple immediately indicates we are only modifying the current iterable key.

        If no target attributes are provided, it is assumed that we are modifying the current iterable key.

        Args:
            record (logging.LogRecord): Log record of the message about to be emitted.
            attr (str): String name of the attribute to fetch
            styled_attributes (Dict[str, str]): dictionary defined in the formatMessage method of the SuffuseFormatter.
        """
        target_attributes = self.target_attributes or (attr,)
        self._modify_target_attributes(record, target_attributes, styled_attributes)

    def _is_glob_match(self, pattern: str, value: str) -> bool:
        """Logic to allow glob matching on strings, and accounting for case-insensitivity.

        Args:
            pattern (str): Pattern to execute against the value.
            value (str): Value to be assessed.

        Returns:
            bool: True if the pattern matches the value.
        """

        if self.case_sensitive_glob:
            return fnmatch.fnmatch(pattern, value)
        else:
            case_insensitive_pattern = re.compile(fnmatch.translate(pattern), re.IGNORECASE)
            return bool(re.match(case_insensitive_pattern, value))

    def _modify_target_attributes(
        self,
        record: logging.LogRecord,
        target_attributes: Tuple[str, ...],
        styled_attributes: Dict[str, str],
        styles: ANSI_STYLES = tuple(),
    ):
        """Singular location where we style a value. Modifies the style_attributes dictionary in place.

        Args:
            record (logging.LogRecord): Log record of the message about to be emitted.
            target_attributes (Tuple[str]): String name(s) of the attribute to fetch
            styled_attributes (Dict[str, str]): dictionary defined in the formatMessage method of the SuffuseFormatter.
            styles (ANSI_STYLES, optional): Tuple of ansi names / enums to fetch against the global ansi map. Defaults to tuple().
        """
        for target_attribute in target_attributes:
            # if we've already seen this value then grab the previously formatted version
            if target_attribute in styled_attributes:
                styled_attributes[target_attribute] = self.style(
                    text=styled_attributes[target_attribute], styles=styles
                )
            else:
                value = self.get_attr(record, target_attribute)
                if target_attribute == "levelname" and target_attribute not in styled_attributes:
                    # .rjust(8) is len('critical')
                    styled_attributes[target_attribute] = self.style(text=value.rjust(8), styles=styles)
                else:
                    styled_attributes[target_attribute] = self.style(text=value, styles=styles)

    def __bool__(self):
        return bool(self.match_to_color_map)
