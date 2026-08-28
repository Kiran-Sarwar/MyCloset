import unittest
import sys
import os
import tempfile
import shutil

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "src")
    )
)

from wardrobe_manager import WardrobeManager


class TestWardrobeManager(unittest.TestCase):

    def test_add_clothing(self):
        manager = WardrobeManager()

        manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer"
        )

        self.assertEqual(len(manager.wardrobe), 1)
        self.assertEqual(
            manager.wardrobe[0].name,
            "Black T-shirt"
        )

    def test_search_by_category(self):
        manager = WardrobeManager()

        manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer"
        )

        manager.add_clothing(
            "Blue Jeans",
            "Bottoms",
            "Casual",
            "Blue",
            "All-Season"
        )

        results = manager.search_by_category("Tops")

        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0].name,
            "Black T-shirt"
        )

    def test_search_by_occasion(self):
        manager = WardrobeManager()

        manager.add_clothing(
            "Navy Suit",
            "Outerwear",
            "Formal",
            "Navy",
            "All-Season"
        )

        manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer"
        )

        results = manager.search_by_occasion("Formal")

        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0].name,
            "Navy Suit"
        )

    def test_search_keyword(self):
        manager = WardrobeManager()

        manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer",
            "T-Shirt"
        )

        manager.add_clothing(
            "Blue Jeans",
            "Bottoms",
            "Casual",
            "Blue",
            "All-Season",
            "Jeans"
        )

        results = manager.search("black")

        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0].name,
            "Black T-shirt"
        )

    def test_search_keyword_case_insensitive(self):
        manager = WardrobeManager()

        manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer",
            "T-Shirt"
        )

        results = manager.search("BLACK")

        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0].name,
            "Black T-shirt"
        )

    def test_search_keyword_not_found(self):
        manager = WardrobeManager()

        manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer",
            "T-Shirt"
        )

        results = manager.search("Wedding")

        self.assertEqual(results, [])

    def test_remove_clothing(self):
        manager = WardrobeManager()

        manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer"
        )

        manager.add_clothing(
            "Blue Jeans",
            "Bottoms",
            "Casual",
            "Blue",
            "All-Season"
        )

        manager.remove_clothing("Black T-shirt")

        self.assertEqual(len(manager.wardrobe), 1)
        self.assertEqual(
            manager.wardrobe[0].name,
            "Blue Jeans"
        )

    def test_edit_clothing(self):
        manager = WardrobeManager()

        manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer",
            "T-Shirt"
        )

        manager.edit_clothing(
            "Black T-shirt",
            "White Polo",
            "Tops",
            "Casual",
            "White",
            "Summer",
            "Shirt"
        )

        self.assertEqual(len(manager.wardrobe), 1)
        self.assertEqual(
            manager.wardrobe[0].name,
            "White Polo"
        )
        self.assertEqual(
            manager.wardrobe[0].color,
            "White"
        )
        self.assertEqual(
            manager.wardrobe[0].item_type,
            "Shirt"
        )

    def test_edit_clothing_case_insensitive(self):
        manager = WardrobeManager()

        manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer"
        )

        manager.edit_clothing(
            "BLACK T-SHIRT",
            "White T-shirt",
            "Tops",
            "Casual",
            "White",
            "Summer"
        )

        self.assertEqual(
            manager.wardrobe[0].name,
            "White T-shirt"
        )

    def test_edit_clothing_not_found(self):
        manager = WardrobeManager()

        manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer"
        )

        manager.edit_clothing(
            "Blue Shirt",
            "White Shirt",
            "Tops",
            "Casual",
            "White",
            "Summer"
        )

        self.assertEqual(len(manager.wardrobe), 1)
        self.assertEqual(
            manager.wardrobe[0].name,
            "Black T-shirt"
        )

    def test_recommend_items(self):
        manager = WardrobeManager()

        manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer"
        )

        manager.add_clothing(
            "Blue Jeans",
            "Bottoms",
            "Casual",
            "Blue",
            "All-Season"
        )

        manager.add_clothing(
            "Black Coat",
            "Outerwear",
            "Casual",
            "Black",
            "Winter"
        )

        results = manager.recommend_items(
            "Casual",
            "Summer"
        )

        self.assertEqual(len(results), 2)
        self.assertEqual(
            results[0].name,
            "Black T-shirt"
        )
        self.assertEqual(
            results[1].name,
            "Blue Jeans"
        )

    def test_recommend_items_case_insensitive(self):
        manager = WardrobeManager()

        manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer"
        )

        results = manager.recommend_items(
            "CASUAL",
            "SUMMER"
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0].name,
            "Black T-shirt"
        )

    def test_recommend_items_not_found(self):
        manager = WardrobeManager()

        manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer"
        )

        results = manager.recommend_items(
            "Formal",
            "Winter"
        )

        self.assertEqual(results, [])

    def test_generate_outfits(self):
        manager = WardrobeManager()

        manager.add_clothing(
            "White T-shirt",
            "Tops",
            "Casual",
            "White",
            "Summer"
        )

        manager.add_clothing(
            "Blue Jeans",
            "Bottoms",
            "Casual",
            "Blue",
            "All-Season"
        )

        manager.add_clothing(
            "White Sneakers",
            "Shoes",
            "Casual",
            "White",
            "All-Season"
        )

        outfits = manager.generate_outfits(
            "Casual",
            "Summer"
        )

        self.assertEqual(len(outfits), 1)

        self.assertEqual(
            outfits[0][0].name,
            "White T-shirt"
        )

        self.assertEqual(
            outfits[0][1].name,
            "Blue Jeans"
        )

        self.assertEqual(
            outfits[0][2].name,
            "White Sneakers"
        )

    def test_generate_multiple_outfits(self):
        manager = WardrobeManager()

        manager.add_clothing(
            "White T-shirt",
            "Tops",
            "Casual",
            "White",
            "Summer"
        )

        manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer"
        )

        manager.add_clothing(
            "Blue Jeans",
            "Bottoms",
            "Casual",
            "Blue",
            "Summer"
        )

        manager.add_clothing(
            "Black Trousers",
            "Bottoms",
            "Casual",
            "Black",
            "Summer"
        )

        manager.add_clothing(
            "White Sneakers",
            "Shoes",
            "Casual",
            "White",
            "Summer"
        )

        manager.add_clothing(
            "Black Sneakers",
            "Shoes",
            "Casual",
            "Black",
            "Summer"
        )

        outfits = manager.generate_outfits(
            "Casual",
            "Summer"
        )

        self.assertEqual(len(outfits), 8)

    def test_generate_outfits_not_found(self):
        manager = WardrobeManager()

        manager.add_clothing(
            "White T-shirt",
            "Tops",
            "Casual",
            "White",
            "Summer"
        )

        manager.add_clothing(
            "Blue Jeans",
            "Bottoms",
            "Casual",
            "Blue",
            "Summer"
        )

        outfits = manager.generate_outfits(
            "Formal",
            "Winter"
        )

        self.assertEqual(outfits, [])

    def test_show_item_count(self):
        manager = WardrobeManager()

        self.assertEqual(len(manager.wardrobe), 0)

        manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer"
        )

        manager.add_clothing(
            "Blue Jeans",
            "Bottoms",
            "Casual",
            "Blue",
            "All-Season"
        )

        self.assertEqual(len(manager.wardrobe), 2)

        manager.remove_clothing("Black T-shirt")

        self.assertEqual(len(manager.wardrobe), 1)

    def test_search_category_not_found(self):
        manager = WardrobeManager()

        manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer"
        )

        results = manager.search_by_category("Footwear")

        self.assertEqual(results, [])

    def test_search_occasion_not_found(self):
        manager = WardrobeManager()

        manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer"
        )

        results = manager.search_by_occasion("Wedding")

        self.assertEqual(results, [])

    def test_save_and_load_wardrobe(self):
        original_directory = os.getcwd()
        temporary_directory = tempfile.mkdtemp()

        try:
            os.chdir(temporary_directory)

            manager = WardrobeManager()

            manager.add_clothing(
                "Black T-shirt",
                "Tops",
                "Casual",
                "Black",
                "Summer"
            )

            manager.add_clothing(
                "Blue Jeans",
                "Bottoms",
                "Casual",
                "Blue",
                "All-Season"
            )

            manager.save_wardrobe()

            new_manager = WardrobeManager()
            new_manager.load_wardrobe()

            self.assertEqual(
                len(new_manager.wardrobe),
                2
            )

            self.assertEqual(
                new_manager.wardrobe[0].name,
                "Black T-shirt"
            )

            self.assertEqual(
                new_manager.wardrobe[1].name,
                "Blue Jeans"
            )

        finally:
            os.chdir(original_directory)
            shutil.rmtree(temporary_directory)


if __name__ == "__main__":
    unittest.main()