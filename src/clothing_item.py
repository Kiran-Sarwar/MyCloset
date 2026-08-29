from uuid import uuid4


class ClothingItem:
    def __init__(
        self,
        name: str,
        category: str,
        occasion: str,
        color: str,
        season: str,
        item_type: str = "",
        image_path: str = "",
        item_id: str = ""
    ) -> None:
        self.id = item_id if item_id else str(uuid4())
        self.name = name
        self.category = category
        self.occasion = occasion
        self.color = color
        self.season = season
        self.item_type = item_type
        self.image_path = image_path

    def display(self) -> None:
        print(f"ID: {self.id}")
        print(f"Name: {self.name}")
        print(f"Category: {self.category}")
        print(f"Type: {self.item_type}")
        print(f"Occasion: {self.occasion}")
        print(f"Color: {self.color}")
        print(f"Season: {self.season}")
        print(f"Image: {self.image_path}")