from dataclasses import dataclass
from itertools import islice


@dataclass(slots=True)
class Item:
    id: int
    name: str
    price: float
    deleted: bool = False


class ItemStorage:

    def __init__(self):
        self.items = {}

    def add_new_item(self, name: str, price: float) -> Item:
        new_item = Item(id=len(self.items) + 1, name=name, price=price, deleted=False)
        self.items[new_item.id] = new_item
        return new_item
    
    def get_item(self, item_id: int) -> Item | None:
        return self.items.get(item_id)
    
    def replace_item(self, item_id: int, name: str, price: float) -> Item:
        if item_id in self.items:
            item = Item(item_id, name, price, deleted=False)
            self.items[item_id] = item
            return item
        else:
            raise ValueError("Item not found")
        
    def update_item(
        self, 
        item_id: int,
        name: str | None = None,
        price: float | None = None,
    ) -> Item:
        if item_id in self.items:
            if name is not None:
                self.items[item_id].name = name
            if price is not None:
                self.items[item_id].price = price
            return self.items[item_id]
        else:
            raise ValueError("Item not found")
        
    def delete_item(self, item_id: int) -> None:
        if item_id in self.items:
            self.items[item_id].deleted = True
        else:
            raise ValueError("Item not found")
    
    def paginate_items_filtered(
        self,
        offset: int = 0,
        limit: int = 10,
        min_price: float | None = None,
        max_price: float | None = None,
        show_deleted: bool = False,
    ) -> list[Item]:
        
        def filter_item(item: Item) -> bool:
            if not show_deleted and item.deleted:
                return False
            if min_price and item.price < min_price:
                return False
            if max_price and item.price > max_price:
                return False
            return True
        
        items = islice(filter(filter_item, list(self.items.values())), offset, limit)
        return list(items)
    

items_storage = ItemStorage()