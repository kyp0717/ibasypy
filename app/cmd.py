from ib_client import IBClient
from trade import Trade


class Cmd:
    def __init_(self, client: IBClient, trade: Trade):
        self.client = client
        self.trade = trade

    def buy_limit(self, price):
        contract = self.trade.define_contract(self.trade.symbol)
        ordfn = self.create_order_fn(
            reqId=self.trade.client.order_id, action="BUY", ordertype="LMT"
        )
        ord = ordfn(price)
        self.client.placeOrder(self.client.order_id, contract, ord)

    # order is define in the tickPrice function
    # price dependency
