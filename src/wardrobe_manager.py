from clothing_item import ClothingItem
from pathlib import Path

class WardrobeManager:

    def __init__(self) -> None:
        self.wardrobe: list[ClothingItem] = []
        self.file_path = Path(__file__).parent / "wardrobe.txt"

    def add_clothing(
        self,
        name: str,
        category: str,
        occasion: str,
        color: str,
        season: str
    ) -> None:

        clothing_item = ClothingItem(
            name,
            category,
            occasion,
            color,
            season
        )

        self.wardrobe.append(clothing_item)

        print(f"{name} has been added to your wardrobe.")

    def view_wardrobe(self) -> None:

        if not self.wardrobe:
            print("Your wardrobe is empty.")
        else:
            print("\n--- Your Wardrobe ---")

            for item in self.wardrobe:
                item.display()

    def search_by_category(self, category: str) -> list[ClothingItem]:

        found_items = [
            item
            for item in self.wardrobe
            if item.category.lower() == category.lower()
        ]

        if not found_items:
            print(f"No items found in category: {category}")
            return []

        print(f"\n--- Items in Category: {category} ---")

        for item in found_items:
            item.display()

        return found_items

    def search_by_occasion(self, occasion: str) -> list[ClothingItem]:

        found_items = [
            item
            for item in self.wardrobe
            if item.occasion.lower() == occasion.lower()
        ]

        if not found_items:
            print(f"No items found for occasion: {occasion}")
            return []

        print(f"\n--- Items for Occasion: {occasion} ---")

        for item in found_items:
            item.display()

        return found_items

    def remove_clothing(self, name: str) -> None:

        for item in self.wardrobe:

            if item.name.lower() == name.lower():

                self.wardrobe.remove(item)

                print(f"{name} has been removed from your wardrobe.")

                return

        print(f"{name} not found in your wardrobe.")

    def show_item_count(self) -> None:

        count = len(self.wardrobe)

        print(f"You have {count} item(s) in your wardrobe.")

    def save_wardrobe(self) -> None:

        with open(self.file_path, "w") as file:

            for item in self.wardrobe:

                file.write(
                    f"{item.name},{item.category},{item.occasion},"
                    f"{item.color},{item.season}\n"
                )

        print("Wardrobe saved to wardrobe.txt.")

    def load_wardrobe(self) -> None:

        # Clear current wardrobe before loading saved items.
        self.wardrobe.clear()

        try:

            with open(self.file_path, "r") as file:

                for line in file:

                    if line.strip():

                        name, category, occasion, color, season = (
                            line.strip().split(",")
                        )

                        item = ClothingItem(
                            name,
                            category,
                            occasion,
                            color,
                            season
                        )

                        self.wardrobe.append(item)

            print("Wardrobe loaded from wardrobe.txt.")

        except FileNotFoundError:

            print("No saved wardrobe found.")