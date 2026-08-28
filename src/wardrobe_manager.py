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
        season: str,
        item_type: str = ""
    ) -> None:
        clothing_item = ClothingItem(
            name,
            category,
            occasion,
            color,
            season,
            item_type
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

    def search_by_category(
        self,
        category: str
    ) -> list[ClothingItem]:
        return [
            item
            for item in self.wardrobe
            if item.category.lower() == category.lower()
        ]

    def search_by_occasion(
        self,
        occasion: str
    ) -> list[ClothingItem]:
        return [
            item
            for item in self.wardrobe
            if item.occasion.lower() == occasion.lower()
        ]

    def search(
        self,
        keyword: str
    ) -> list[ClothingItem]:
        keyword = keyword.lower()
        return [
            item
            for item in self.wardrobe
            if (
                keyword in item.name.lower()
                or keyword in item.category.lower()
                or keyword in item.item_type.lower()
                or keyword in item.occasion.lower()
                or keyword in item.color.lower()
                or keyword in item.season.lower()
            )
        ]

    def remove_clothing(self, name: str) -> None:
        for item in self.wardrobe:
            if item.name.lower() == name.lower():
                self.wardrobe.remove(item)
                print(
                    f"{name} has been removed from your wardrobe."
                )
                return

        print(f"{name} not found in your wardrobe.")

    def edit_clothing(
        self,
        old_name: str,
        name: str,
        category: str,
        occasion: str,
        color: str,
        season: str,
        item_type: str = ""
    ) -> None:
        for item in self.wardrobe:
            if item.name.lower() == old_name.lower():
                item.name = name
                item.category = category
                item.occasion = occasion
                item.color = color
                item.season = season
                item.item_type = item_type

                print(
                    f"{old_name} has been updated to {name}."
                )
                return

        print(f"{old_name} not found in your wardrobe.")

    def show_item_count(self) -> None:
        count = len(self.wardrobe)
        print(
            f"You have {count} item(s) in your wardrobe."
        )

    def get_category_count(self, category: str) -> int:
        return sum(
            1
            for item in self.wardrobe
            if item.category.lower() == category.lower()
        )

    def save_wardrobe(self) -> None:
        with open(self.file_path, "w") as file:
            for item in self.wardrobe:
                file.write(
                    f"{item.name},{item.category},{item.item_type},"
                    f"{item.occasion},{item.color},{item.season}\n"
                )

        print("Wardrobe saved to wardrobe.txt.")

    def load_wardrobe(self) -> None:
        self.wardrobe.clear()

        try:
            with open(self.file_path, "r") as file:
                for line in file:
                    if not line.strip():
                        continue

                    parts = line.strip().split(",")

                    if len(parts) == 6:
                        name, category, item_type, occasion, color, season = (
                            parts
                        )
                    elif len(parts) == 5:
                        name, category, occasion, color, season = parts
                        item_type = ""
                    else:
                        continue

                    item = ClothingItem(
                        name,
                        category,
                        occasion,
                        color,
                        season,
                        item_type
                    )

                    self.wardrobe.append(item)

            print("Wardrobe loaded from wardrobe.txt.")

        except FileNotFoundError:
            print("No saved wardrobe found.")