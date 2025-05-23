import cmd
import threading
import time

import key_listener as kl
import trade as t
from ib_client import IBClient, qu_bid, qu_orderstatus
from rich.console import Console

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

asset = cs.input("Define asset: ")
t = t.Trade(asset)
cmd = cmd.Cmd(client)

while True:
    match t.stage:
        case t.stage.ENTRY:
            price = qu_bid.get(timeout=2)
            cs.print(f"buy {t.symbol} at {price}? y/n ", end="")
            input = kl.get_single_key()
            if input == "y":
                cmd.buy_limit(price)
                t.stage = t.STAGE.CHECK_ENTRY
            else:
                time.sleep(1)
                continue
        case t.stage.CHECK_ENTRY:
            ordstat = qu_orderstatus.get(timeout=2)
            if ordstat["status"] == "Filled":
                cs.print(f"{t.reqId} Status: {ordstat['status']} ")
                cs.print(f"{t.reqId} Entry Price: {ordstat['avgFillPrice']} ")
                t.entry_price = ordstat["avgFillPrice"]
                t.stage = t.STAGE.HOLD
            else:
                time.sleep(1)
                continue
        case t.stage.HOLD:
            price = cmd.get_bid()
