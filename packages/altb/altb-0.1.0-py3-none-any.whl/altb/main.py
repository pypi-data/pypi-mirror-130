import curses
import pkg_resources
from typing import Union, List

import typer
from blessed import Terminal
from rich.text import Text
from rich.live import Live
from rich.console import ConsoleRenderable, Console, ConsoleOptions, RenderResult
from rich.padding import Padding


app = typer.Typer()


__version__ = pkg_resources.get_distribution('altb').version


class Selector(ConsoleRenderable):
    def __init__(self, options: List[Union[Text, str]]):
        self.options = options
        self.marked = set()
        self._hovered = 0

    def increment(self):
        if self._hovered < len(self.options) - 1:
            self._hovered += 1

        else:
            self._hovered = 0

    def decrement(self):
        if self._hovered > 0:
            self._hovered -= 1

        else:
            self._hovered = len(self.options) - 1

    def select(self):
        element = self._hovered
        if element in self.marked:
            self.marked.remove(element)

        else:
            self.marked.add(element)

    @property
    def selections(self):
        return [self.options[i] for i in self.marked]

    def __rich_console__(
            self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        for i, row in enumerate(self.options):
            marked_char = "⬢" if i in self.marked else "⬡"
            hovered_char = "⮞" if i == self._hovered else " "
            symbol_style_fg = "default"
            symbol_style_bg = "default"
            text_style_fg = "default"
            text_style_bg = "default"
            hovered_style_fg = "default"
            hovered_style_bg = "default"
            if i == self._hovered:
                hovered_style_bg = symbol_style_bg = text_style_bg = "white"
                hovered_style_fg = symbol_style_fg = text_style_fg = "grey11"

            if i in self.marked:
                text_style_fg = "green4"
                symbol_style_fg = "green4"

            text_style = f"{text_style_fg} on {text_style_bg}"
            symbol_style = f"{symbol_style_fg} on {symbol_style_bg}"
            hovered_style = f"{hovered_style_fg} on {hovered_style_bg}"
            rendered_row = Text(f"{hovered_char} ", style=hovered_style) + \
                           Text(f"{marked_char} ", style=symbol_style) + \
                           Text(row, style=text_style, justify="left")

            yield Padding(rendered_row, pad=(0, 2), style=hovered_style, expand=False)


def run_selector(options):
    term = Terminal()
    selector = Selector(options)
    with term.cbreak(), term.hidden_cursor():
        with Live(selector, auto_refresh=False) as live:  # update 4 times a second to feel fluid
            try:
                while True:
                    val = term.inkey(timeout=0.5)
                    if val.is_sequence and val.code == curses.KEY_DOWN:
                        selector.increment()

                    elif val.is_sequence and val.code == curses.KEY_UP:
                        selector.decrement()

                    elif str(val) == " ":
                        selector.select()

                    elif val.is_sequence and val.code == curses.KEY_ENTER:
                        live.update(f'Selected: {selector.selections}')
                        return selector.selections

                    live.refresh()

            except KeyboardInterrupt:
                live.update('Canceled..', refresh=True)


@app.command()
def config():
    pass


def main():
    app()


if __name__ == '__main__':
    main()
