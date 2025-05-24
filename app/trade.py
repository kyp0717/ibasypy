from dataclasses import dataclass
from enum import Enum

from ib_client import IBClient


class STAGE(Enum):
    CONNECT = 1
    ENTRY = 2
    CHECK_ENTRY = 3
    HOLD = 4
    EXIT = 5
    CHECK_EXIT = 6
    DISCONNECT = 7


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
    def __init__(self, symbol, position: int, client: IBClient):
        self.symbol: str = symbol
        self.client = client
        self.stage: STAGE = None
        self.size: int = 0
        self.position = position
        self.stop_loss: float = 0.0
        self.entry_price: float = 0.0
        self.exit_price: float = 0.0
        self.conid = None
        self.unreal_pnlval: float = 0.0
        self.unreal_pnlpct: float = 0.0
        # TODO: Add order history to so that we can confirm order status
