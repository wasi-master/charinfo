import unicodedata
import argparse
import re
from typing import Any, Optional, Callable, List, Dict, Union, TypeVar
from re import Pattern

CATEGORIES = {
    "Cc": "Other, control",
    "Cf": "Other, format",
    "Cn": "Other, not assigned",
    "Co": "Other, private use",
    "Cs": "Other, surrogate",
    "Ll": "Letter, lowercase",
    "Lm": "Letter, modifier",
    "Lo": "Letter, other",
    "Lt": "Letter, titlecase",
    "Lu": "Letter, uppercase",
    "Mc": "Mark, spacing combining",
    "Me": "Mark, enclosing",
    "Mn": "Mark, nonspacing",
    "Nd": "Number, decimal digit",
    "Nl": "Number, letter",
    "No": "Number, other",
    "Pc": "Punctuation, connector",
    "Pd": "Punctuation, dash",
    "Pe": "Punctuation, close",
    "Pf": "Punctuation, final quote",
    "Pi": "Punctuation, initial quote",
    "Po": "Punctuation, other",
    "Ps": "Punctuation, open",
    "Sc": "Symbol, currency",
    "Sk": "Symbol, modifier",
    "Sm": "Symbol, math",
    "So": "Symbol, other",
    "Zl": "Separator, line",
    "Zp": "Separator, paragraph",
    "Zs": "Separator, space",
}

COMBINING_CLASSES = {
    "0": "Not Reordered",
    "1": "Overlay",
    "10": "CCC10",
    "103": "CCC103",
    "107": "CCC107",
    "11": "CCC11",
    "118": "CCC118",
    "12": "CCC12",
    "122": "CCC122",
    "129": "CCC129",
    "13": "CCC13",
    "130": "CCC130",
    "132": "CCC132",
    "14": "CCC14",
    "15": "CCC15",
    "16": "CCC16",
    "17": "CCC17",
    "18": "CCC18",
    "19": "CCC19",
    "20": "CCC20",
    "202": "Attached Below",
    "21": "CCC21",
    "214": "Attached Above",
    "216": "Attached Above Right",
    "218": "Below Left",
    "22": "CCC22",
    "220": "Below",
    "222": "Below Right",
    "224": "Left",
    "226": "Right",
    "228": "Above Left",
    "23": "CCC23",
    "230": "Above",
    "232": "Above Right",
    "233": "Double Below",
    "234": "Double Above",
    "24": "CCC24",
    "240": "Iota Subscript",
    "25": "CCC25",
    "26": "CCC26",
    "27": "CCC27",
    "28": "CCC28",
    "29": "CCC29",
    "30": "CCC30",
    "31": "CCC31",
    "32": "CCC32",
    "33": "CCC33",
    "34": "CCC34",
    "35": "CCC35",
    "36": "CCC36",
    "6": "6",
    "7": "Nukta",
    "8": "Kana Voicing",
    "84": "CCC84",
    "9": "Virama",
    "91": "CCC91",
}

T = TypeVar("T", str, bytes)


def regex_arg(
    regex: Pattern, type_: Callable[[str], Any] = str
) -> Callable[[str], str]:
    def inner(arg: str) -> str:
        match = regex.match(arg)
        if not match:
            raise argparse.ArgumentTypeError

        try:
            return type_(match.group(1))
        except:
            return type_(match.group(0))

    return inner


def _bool(string: Union[str, int]) -> bool:
    return string == "ON" or string == 1


def _split(string: T, length: int) -> List[T]:
    return [string[i : i + length] for i in range(0, len(string), length)]


class CharacterInfo:
    __slots__ = (
        "char",
        "name",
        "combining",
        "category",
        "is_bidirectional",
        "is_mirrored",
        "html_entity",
        "html_entity_alt",
        "css_entity",
        "utf_8_entity",
        "utf_8_encoding",
        "utf_16_encoding",
        "utf_32_encoding",
        "binary_code",
        "decimal_code",
        "octal_code",
        "hex_code",
    )

    def __init__(self, char: str):
        # General Data
        self.char = char
        self.name = unicodedata.name(char)
        self.combining = _bool(unicodedata.combining(char))
        self.category = CATEGORIES[unicodedata.category(char)]
        self.is_bidirectional = _bool(unicodedata.bidirectional(char))
        self.is_mirrored = _bool(unicodedata.mirrored(char))

        # Entities
        self.html_entity = f"&#{ord(char)};"
        self.html_entity_alt = f"&#{hex(ord(char)).lstrip('0')};"
        self.css_entity = f"\\{hex(ord(char)).lstrip('0x').zfill(4)}"
        self.utf_8_entity = f"\\u{hex(ord(char)).lstrip('0x').zfill(4)}"

        # Encodings
        self.utf_8_encoding = f"{' '.join('0x'+ x.zfill(2) for x in _split(hex(ord(char)).lstrip('0x'), 2))}"
        self.utf_16_encoding = f"{' '.join('0x'+ x.zfill(4) for x in _split(hex(ord(char)).lstrip('0x'), 4))}"
        self.utf_32_encoding = f"{'0x'+hex(ord(char)).lstrip('0x').zfill(8)}"

        # Character Codes
        self.binary_code = bin(ord(char))[2:]
        self.decimal_code = ord(char)
        self.octal_code = oct(ord(char)).lstrip("0o")
        self.hex_code = hex(ord(char))


argumentparser = argparse.ArgumentParser(description="Print unicode character info")
argumentparser.add_argument(
    "characters", nargs="?", help="The character(s) to print info for", default=[]
)
argumentparser.add_argument(
    "-n",
    "--name",
    help="The name of the character to print info for (can be used multiple times)",
    action="append",
    default=[],
)
argumentparser.add_argument(
    "-u",
    "--unicode",
    help="The unicode of the character to print info for (can be used multiple times)",
    action="append",
    default=[],
    type=regex_arg(re.compile(r"(?:\\u|U\+|&#1|&#x)(?P<code>[0-9]{4})")),
)
argumentparser.add_argument(
    "-d",
    "--decimal",
    help="The decimal value of the unicode codepoint of the character to print info for (can be used multiple times)",
    action="append",
    default=[],
    type=regex_arg(re.compile(r"[0-9]{1,5}"), type_=int),
)
args = argumentparser.parse_args()
for i in args.name:
    args.characters.append(unicodedata.lookup(i))
for i in args.unicode:
    args.characters.append(chr(int(i, 16)))
for i in args.decimal:
    args.characters.append(chr(i))
