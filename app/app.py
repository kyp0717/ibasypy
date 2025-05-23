import cmd

from rich.console import Console

import key_listener as kl
import trade as t

cs = Console()
cs.clear()

asset = cs.input("Define asset: ")
t = t.Trade(asset)

while True:
    match t.stage:
        case t.stage.ENTRY:
            price = cmd.get_ask()
            cs.print(f"buy {t.symbol} at {price}? y/n ", end="")
            input = kl.get_single_key()
            if input == "y":
                t.enter(price)
            else:
                continue
        case t.stage.HOLD:
            price = cmd.get_bid()
