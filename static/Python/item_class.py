from datetime import datetime as dt


class Item:
    def __init__(self, id: str, name: str, buy: bool, created_at: dt, price: float) -> None:  # , emoji: str
        self.id = id
        self.name = name
        self.buy = buy
        self.created_at = created_at
        self.price = price
        # self.emoji = emoji
