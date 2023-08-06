import re
from dataclasses import dataclass
from typing import Dict, Union, List

_YetAnotherINI = Dict[
    str, Union[
        str, Dict[str, Union[str, None]], List[str], None
    ]
]  # {"a": "b", "c": {"d": "e"}, "f": ["g", "h", "i"]}


def parse_from_file(filename: str, encoding="utf-8"):
    return parse(open(filename, encoding=encoding).read())


_DICT_HEADER_REGEX = re.compile(r"\s*\[\s*(.+?)\s*]\s*")
_LIST_HEADER_REGEX = re.compile(r"\s*<\s*(.+?)\s*>\s*")
_KEY_VALUE = re.compile(r"(.+?)\s*=\s*(.+)")


def _write_key_value_to_dict(dict_, line):
    match = _KEY_VALUE.fullmatch(line)
    if match:
        dict_[match.group(1)] = match.group(2)
    else:
        dict_[line] = None


@dataclass
class _HeaderInfo:
    name: str
    is_key_value: bool


def parse(string: str):
    header_info = None
    sections = {}
    lines_iterator = iter(string.split("\n"))
    for line in lines_iterator:
        if line:
            for regex, is_key_value in (
                (_DICT_HEADER_REGEX, True),
                (_LIST_HEADER_REGEX, False)
            ):
                match = regex.fullmatch(line)
                if match:
                    header_info = _HeaderInfo(
                        name=match.group(1), is_key_value=is_key_value
                    )
                    break
            else:
                if header_info:
                    if header_info.is_key_value:
                        _write_key_value_to_dict(
                            dict_=sections.setdefault(header_info.name, {}),
                            line=line
                        )
                    else:
                        sections.setdefault(header_info.name, []).append(line)
                else:
                    _write_key_value_to_dict(dict_=sections, line=line)
    return sections
