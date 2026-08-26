class ClothingItem:

    def __init__(
        self,
        name: str,
        category: str,
        occasion: str,
        color: str,
        season: str,
        item_type: str = ""
    ) -> None:

        self.name = name
        self.category = category
        self.occasion = occasion
        self.color = color
        self.season = season
        self.item_type = item_type

    def display(self) -> None:

        print(f"Name: {self.name}")
        print(f"Category: {self.category}")
        print(f"Type: {self.item_type}")
        print(f"Occasion: {self.occasion}")
        print(f"Color: {self.color}")
        print(f"Season: {self.season}")