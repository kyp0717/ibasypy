from ib_client import IBClient
from trade import Trade


class Cmd:
    def __init__(self, client: IBClient, trade: Trade):
        self.client = client
        self.trade = trade

    def buy_limit(self, price):
        self.client.nextId()
        ordfn = self.trade.create_order_fn(
            reqId=self.client.order_id, action="BUY", ordertype="LMT"
        )
        ord = ordfn(price)
        self.client.placeOrder(self.client.order_id, self.trade.contract, ord)

    def sell_limit(self, price):
        self.client.nextId()
        ordfn = self.trade.create_order_fn(
            reqId=self.client.order_id, action="SELL", ordertype="LMT"
        )
        ord = ordfn(price)
        self.client.placeOrder(self.client.order_id, self.trade.contract, ord)

    # order is define in the tickPrice function
    # price dependency
