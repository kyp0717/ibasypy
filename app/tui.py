from rich.console import Console

console = Console()


class TUI:
    def __init__(self, console):
        console = console

    def start_console(self) -> Console:
        c = Console()
        return c

    def buy_ask(self, symbol, price):
        console.print(f"buy {symbol} at {price}? y/n ", end="")
