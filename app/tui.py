from rich.console import Console
from rich.text import Text
from trade import STAGE, Trade

console = Console()


class TUI:
    def __init__(self, console: Console, trade: Trade):
        self.cs = console
        self.tr = trade

    def show_heading(self):
        h = f"\n ********* [u]{self.tr.symbol}[/u] ********* "
        wh = Text(h)
        self.cs.print(wh)

    def show_pnl(self):
        t = f" Unrealized PnL: {self.tr.unreal_pnlval:.2f}"
        wt = Text(t)
        if self.tr.unreal_pnlval == 0:
            wt.stylize("blue")
        elif self.tr.unreal_pnlval < 0:
            wt.stylize("red")
        elif self.tr.unreal_pnlval > 0:
            wt.stylize("green")
        self.cs.print(wt)

    def req_contract(self):
        pass

    def show_entry(self):
        h = f" [ ReqID {self.tr.ids.buy} ] Entry Price: {self.tr.entry_price} "
        self.cs.print(h)

    def show_check_entry(self):
        h = f" [ ReqID {self.tr.ids.buy} ] Entry Price: {self.tr.entry_price} "
        self.cs.print(h)

    def show(self):
        match self.tr.stage:
            case STAGE.ENTRY:
                self.show_heading
