import argparse
import cmd
import queue
import sys
import threading
import time

import key_listener as kl
from ib_client import IBClient, qu_ask, qu_bid, qu_contract, qu_orderstatus
from rich.console import Console
from trade import STAGE, Trade
from tui import TUI

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description="get symbol and quantity")

# Add arguments
parser.add_argument("symbol", type=str, help="symbol")
parser.add_argument("size", type=int, help="size")
# Parse the arguments
args = parser.parse_args()

cs = Console()
cs.clear()

## Must instantiate the client first because it carries the console instance
client = IBClient()
client.connect("127.0.0.1", 7500, clientId=1001)
## delay market data
## set to 1 for real-time market data
client.reqMarketDataType(1)
# ibclient_thread = threading.Thread(target=start_ib_client, args=(client,), daemon=True)
ibclient_thread = threading.Thread(target=client.run, daemon=True)
ibclient_thread.start()
# Wait for next valid order ID to give time for thread to start up
while client.order_id is None:
    time.sleep(0.5)


t = Trade(symbol=args.symbol, position=args.size)
t.ids.initial = client.order_id
t.tws_ids.initial = client.order_id
t.define_contract()

cmd = cmd.Cmd(client=client, trade=t)

cmd.get_contract()
t.ids.contract = client.order_id
# get method is blocking
c = qu_contract.get(timeout=2)
t.conid = c["conId"]
t.define_contract()
# request market data
cmd.stream_mkt_data()
t.ids.market_data = client.order_id

tui = TUI(console=cs, trade=t)

while True:
    # TODO: capture error message
    # TODO: capture order history
    tui.show()
    match t.stage:
        case STAGE.ENTRY:
            try:
                msg = qu_ask.get(timeout=2)
                cs.print(
                    f"\n >>> buy {t.symbol} at {msg['price']}? y/n ",
                    end="",
                )
                input = kl.get_single_key()
                if input == "y":
                    cmd.buy_limit(msg["price"])
                    t.ids.buy = client.order_id
                    cs.print(
                        f" reqid {client.order_id} >>> buy limit order submitted ",
                        end="",
                    )
                    t.stage = STAGE.CHECK_ENTRY
                else:
                    # time.sleep(1)
                    continue
            except queue.Empty:
                # TODO: provide the option to cancel the order and exit app
                cs.print(" [ TWS ] ask queue empty")
                continue
        case STAGE.CHECK_ENTRY:
            try:
                ordstat = qu_orderstatus.get(timeout=2)
                cs.print(f" reqid {client.order_id} >>> Status: {ordstat['status']} ")
                cs.print(
                    f" reqid {client.order_id} >>> Entry Price: {ordstat['avgFillPrice']} "
                )
                if ordstat["status"] == "Filled":
                    t.entry_price = ordstat["avgFillPrice"]
                    tui.show_entry()
                    t.stage = STAGE.HOLD
                else:
                    cs.print("order not filled")
                    cs.print(ordstat)
                    time.sleep(1)
                    continue
            except queue.Empty:
                cs.print("order status queue empty")
                continue
        case STAGE.HOLD:
            try:
                msg = qu_bid.get(timeout=2)
                t.unreal_pnlval = t.position * (msg["price"] - t.entry_price)
                t.unreal_pnlpct = (msg["price"] - t.entry_price) / t.entry_price
                cs.print(f"\n >>> sell {t.symbol} at {msg['price']}? y/n ", end="")
                input = kl.get_single_key()
                # cs.print("\n")
                if input == "y":
                    cmd.sell_limit(msg["price"])
                    cs.print(
                        f" reqid {client.order_id} >>> sell limit order submitted ",
                        end="",
                    )
                    t.stage = STAGE.CHECK_EXIT
                else:
                    time.sleep(1)
                    continue
            except queue.Empty:
                cs.print("bid queue empty")
                continue
        case STAGE.CHECK_EXIT:
            try:
                ordstat = qu_orderstatus.get(timeout=2)
                if ordstat["status"] == "Filled":
                    cs.print(
                        f" reqid {client.order_id} >>> Status: {ordstat['status']} "
                    )
                    cs.print(
                        f" reqid {client.order_id} >>> Exit Price: {ordstat['avgFillPrice']} "
                    )
                    t.exit_price = ordstat["avgFillPrice"]
                    t.stage = STAGE.DISCONNECT
                else:
                    cs.print("order not filled")
                    cs.print(ordstat)
                    time.sleep(1)
                    continue
            except queue.Empty:
                cs.print("order status queue empty")
                continue
        case STAGE.DISCONNECT:
            s = cs.input("Shutdown Algo? (y/n)")
            if s == "y":
                client.disconnect()
                cs.print("Disconnecting from TWS...")
                break

ibclient_thread.join()
sys.exit(0)
