class ClothingItem:
    def __init__(self, name: str, category: str, occasion: str, color: str, season: str) -> None:
        self.name: str = name
        self.category: str = category
        self.occasion: str = occasion
        self.color: str = color
        self.season: str = season

    def display(self) -> None:
        print(f"Name: {self.name}, Category: {self.category}, Occasion: {self.occasion}, Color: {self.color}, Season: {self.season}")