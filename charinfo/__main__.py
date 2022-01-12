from .core import args, CharacterInfo
import rich
from rich.text import Text
from rich.panel import Panel
from rich.console import Console
from rich.columns import Columns
from rich.highlighter import RegexHighlighter
from rich.theme import Theme


class CharacterInfoHighlighter(RegexHighlighter):
    highlights = [
        r"(?P<true>True)|(?P<false>False)",
        r"(?P<entity_prefix>&#|&#x|\\|\\u)",
        r"(?P<hex_code_prefix>0x)",
    ]
    base_style = "char."


console = Console(
    theme=Theme(
        {
            "char.true": "bright_green",
            "char.false": "bright_red",
            "char.entity_prefix": "bright_black",
            "char.hex_code_prefix": "bright_black",
        }
    ),
    highlighter=CharacterInfoHighlighter(),
)


def run():
    panels = []
    for character in args.characters:
        char = CharacterInfo(character)
        info = "".join(
            [
                f"[green]Character:[/] {char.char}\n"
                f"[green]Name:[/] {char.name.title()}\n"
                f"[green]Category:[/] {char.category}\n"
                f"[green]Combining:[/] {char.combining}\n"
                f"[green]Is Bidirectional:[/] {char.is_bidirectional}\n"
                f"[green]Is Mirrored:[/] {char.is_mirrored}\n"
                "\n"
                f"[cyan]HTML Entity:[/] {char.html_entity}\n"
                f"[cyan]HTML Entity (Alternative):[/] {char.html_entity_alt}\n"
                f"[cyan]CSS Entity:[/] {char.css_entity}\n"
                f"[cyan]UTF-8 Entity:[/] {char.utf_8_entity}\n"
                "\n"
                f"[magenta]UTF-8 Encoding:[/] {char.utf_8_encoding}\n"
                f"[magenta]UTF-16 Encoding:[/] {char.utf_16_encoding}\n"
                f"[magenta]UTF-32 Encoding:[/] {char.utf_32_encoding}\n"
                "\n"
                f"[yellow]Binary Code:[/] {char.binary_code}\n"
                f"[yellow]Decimal Code:[/] {char.decimal_code}\n"
                f"[yellow]Octal Code:[/] {char.octal_code}\n"
                f"[yellow]Hex Code:[/] {char.hex_code}"
            ]
        )
        panels.append(Panel(info, title=f"[bold]{char.name}[/bold]"))

    console.print(Columns(panels))


if __name__ == "__main__":
    run()
