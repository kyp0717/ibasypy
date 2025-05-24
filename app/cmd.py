import ibapi.client as ibc
from ib_client import IBClient
from trade import Trade


class Cmd:
    def __init_(self, client: IBClient, trade: Trade):
        self.client = client
        self.trade = trade

    def define_contract(self, symbol) -> ibc.Contract:
        contract = ibc.Contract()
        contract.symbol = symbol
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        contract.primaryExchange = "NASDAQ"
        return contract

    def buy_limit(self, price):
        contract = self.define_contract(self.trade.symbol)
        ordfn = self.create_order_fn(
            reqId=self.client.order_id, action="BUY", ordertype="LMT"
        )
        ord = ordfn(price)
        self.client.placeOrder(self.client.order_id, contract, ord)

    # order is define in the tickPrice function
    # price dependency
    def create_order_fn(self, reqId: int, action: str, ordertype: str):
        order = ibc.Order()

        def create_order(lmtprice: float):
            order.symbol = self.trade.symbol
            order.orderId = reqId
            order.action = action
            order.orderType = ordertype
            order.lmtPrice = lmtprice
            order.totalQuantity = self.trade.position
            # order.outsideRth = False
            order.outsideRth = True
            return order

        return create_order
