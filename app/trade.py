from dataclasses import dataclass
from enum import Enum

# from ib_async import IB, Contract, Order
# from ib_async import IB, Contract, Order
import ib_async as iba

# from ibapi.client import Contract, Order


class TradeSignal(Enum):
    BUY = 1
    SELL = 2
    HOLD = 3


class Stage(Enum):
    CONNECT: 1
    ENTRY = 2
    CONFIRM_ENTRY = 3
    HOLD: 4
    EXIT = 5
    CONFIRM_EXIT = 6
    DISCONNECT: 7


@dataclass
class PriceChange:
    val: float = 0.0
    cct: float = 0.0


@dataclass
class TrackId:
    buy: int = None
    sell: int = None
    reqMktData: int = None


class Trade:
    def __init__(self, symbol, position: int):
        self.symbol: str = symbol
        self.client = self.start_client()
        self.stage: Stage = None
        self.size: int = 0
        self.position = position
        self.stop_loss: float = 0.0
        self.entry_price: float = 0.0
        self.exit_price: float = 0.0
        self.conid = None
        self.unreal_pnlval: float = 0.0
        self.unreal_pnlpct: float = 0.0

    def start_client(self) -> iba.IB:
        ib = iba.IB()
        ib.connect()
        ib.reqMarketDataType(1)
        return ib

    def define_contract(self) -> iba.Contract:
        contract = Contract(self.symbol, se)
        contract.symbol = self.symbol
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        contract.primaryExchange = "NASDAQ"
        return contract

    # order is define in the tickPrice function
    # price dependency
    def create_order_fn(self, reqId: int, action: str, ordertype: str):
        order = Order()

        def create_order(lmtprice: float):
            order.symbol = self.symbol
            order.orderId = reqId
            order.action = action
            order.orderType = ordertype
            order.lmtPrice = lmtprice
            order.totalQuantity = self.position
            # order.outsideRth = False
            order.outsideRth = True
            return order

        return create_order

    def buy_limit():
        pass
