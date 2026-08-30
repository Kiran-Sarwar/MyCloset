from pathlib import Path

from clothing_item import ClothingItem
from database import Database
from recommendation_engine import RecommendationEngine


class WardrobeManager:

    def __init__(
        self,
        db_path: str | Path | None = None
    ) -> None:

        self.wardrobe: list[ClothingItem] = []

        self.legacy_file_path = (
            Path(__file__).parent / "wardrobe.txt"
        )

        if db_path is None:
            db_path = Path(__file__).parent / "mycloset.db"

        self.database = Database(db_path)

        self._migrate_legacy_data()

    def _migrate_legacy_data(self) -> None:
        """
        Migrate existing wardrobe.txt data into SQLite
        when the database is empty.
        """

        if self.database.has_items():
            return

        if not self.legacy_file_path.exists():
            return

        migrated_items = []

        with open(
            self.legacy_file_path,
            "r",
            encoding="utf-8"
        ) as file:

            for line in file:

                if not line.strip():
                    continue

                parts = line.strip().split(",")

                if len(parts) == 8:

                    (
                        item_id,
                        name,
                        category,
                        item_type,
                        occasion,
                        color,
                        season,
                        image_path
                    ) = parts

                elif len(parts) == 7:

                    (
                        item_id,
                        name,
                        category,
                        item_type,
                        occasion,
                        color,
                        season
                    ) = parts

                    image_path = ""

                elif len(parts) == 6:

                    (
                        name,
                        category,
                        item_type,
                        occasion,
                        color,
                        season
                    ) = parts

                    item_id = ""
                    image_path = ""

                elif len(parts) == 5:

                    (
                        name,
                        category,
                        occasion,
                        color,
                        season
                    ) = parts

                    item_id = ""
                    item_type = ""
                    image_path = ""

                else:
                    continue

                item = ClothingItem(
                    name,
                    category,
                    occasion,
                    color,
                    season,
                    item_type,
                    image_path,
                    item_id
                )

                migrated_items.append(item)

        if migrated_items:
            self.database.save_items(
                migrated_items
            )

    def add_clothing(
        self,
        name: str,
        category: str,
        occasion: str,
        color: str,
        season: str,
        item_type: str = "",
        image_path: str = ""
    ) -> None:

        clothing_item = ClothingItem(
            name,
            category,
            occasion,
            color,
            season,
            item_type,
            image_path
        )

        self.wardrobe.append(
            clothing_item
        )

        print(
            f"{name} has been added to your wardrobe."
        )

    def view_wardrobe(self) -> None:

        if not self.wardrobe:
            print(
                "Your wardrobe is empty."
            )

        else:

            print(
                "\n--- Your Wardrobe ---"
            )

            for item in self.wardrobe:
                item.display()

    def search_by_category(
        self,
        category: str
    ) -> list[ClothingItem]:

        return [
            item
            for item in self.wardrobe
            if item.category.lower()
            == category.lower()
        ]

    def search_by_occasion(
        self,
        occasion: str
    ) -> list[ClothingItem]:

        return [
            item
            for item in self.wardrobe
            if item.occasion.lower()
            == occasion.lower()
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

    def remove_clothing(
        self,
        name: str
    ) -> None:

        for item in self.wardrobe:

            if item.name.lower() == name.lower():

                self.wardrobe.remove(item)

                print(
                    f"{name} has been removed from your wardrobe."
                )

                return

        print(
            f"{name} not found in your wardrobe."
        )

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

        print(
            f"{old_name} not found in your wardrobe."
        )

    def recommend_items(
        self,
        occasion: str,
        season: str
    ) -> list[ClothingItem]:

        return [
            item
            for item in self.wardrobe
            if (
                item.occasion.lower()
                == occasion.lower()
                and (
                    item.season.lower()
                    == season.lower()
                    or item.season.lower()
                    == "all-season"
                    or item.season.lower()
                    == "all season"
                )
            )
        ]

    def generate_outfits(
        self,
        occasion: str,
        season: str
    ) -> list[list[ClothingItem]]:

        engine = RecommendationEngine(
            self.wardrobe
        )

        return engine.generate_outfits(
            occasion,
            season
        )

    def recommend_outfits(
        self,
        occasion: str,
        season: str
    ) -> list[tuple[list[ClothingItem], int]]:

        engine = RecommendationEngine(
            self.wardrobe
        )

        return engine.recommend_outfits(
            occasion,
            season
        )

    def show_item_count(self) -> None:

        count = len(self.wardrobe)

        print(
            f"You have {count} item(s) in your wardrobe."
        )

    def get_category_count(
        self,
        category: str
    ) -> int:

        return sum(
            1
            for item in self.wardrobe
            if item.category.lower()
            == category.lower()
        )

    def save_wardrobe(self) -> None:

        self.database.save_items(
            self.wardrobe
        )

        print(
            "Wardrobe saved to mycloset.db."
        )

    def load_wardrobe(self) -> None:

        self.wardrobe = (
            self.database.load_items()
        )

        print(
            "Wardrobe loaded from mycloset.db."
        )