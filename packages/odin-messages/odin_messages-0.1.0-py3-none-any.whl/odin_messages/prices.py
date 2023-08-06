from pydantic import BaseModel

from odin_messages.base import BaseEventMessage


class PriceWatchMesagge(BaseEventMessage):
    exchange: str
    market_code: str
    ask_price: float
    bid_price: float
