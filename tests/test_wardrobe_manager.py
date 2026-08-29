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

    def setUp(self):
        self.temporary_directory = tempfile.mkdtemp()

        self.database_path = os.path.join(
            self.temporary_directory,
            "test_mycloset.db"
        )

        self.manager = WardrobeManager(
            db_path=self.database_path
        )

    def tearDown(self):
        shutil.rmtree(
            self.temporary_directory
        )

    def test_add_clothing(self):
        self.manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer"
        )

        self.assertEqual(
            len(self.manager.wardrobe),
            1
        )

        self.assertEqual(
            self.manager.wardrobe[0].name,
            "Black T-shirt"
        )

    def test_search_by_category(self):
        self.manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer"
        )

        self.manager.add_clothing(
            "Blue Jeans",
            "Bottoms",
            "Casual",
            "Blue",
            "All-Season"
        )

        results = self.manager.search_by_category(
            "Tops"
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0].name,
            "Black T-shirt"
        )

    def test_search_by_occasion(self):
        self.manager.add_clothing(
            "Navy Suit",
            "Outerwear",
            "Formal",
            "Navy",
            "All-Season"
        )

        self.manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer"
        )

        results = self.manager.search_by_occasion(
            "Formal"
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0].name,
            "Navy Suit"
        )

    def test_search_keyword(self):
        self.manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer",
            "T-Shirt"
        )

        self.manager.add_clothing(
            "Blue Jeans",
            "Bottoms",
            "Casual",
            "Blue",
            "All-Season",
            "Jeans"
        )

        results = self.manager.search("black")

        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0].name,
            "Black T-shirt"
        )

    def test_search_keyword_case_insensitive(self):
        self.manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer",
            "T-Shirt"
        )

        results = self.manager.search("BLACK")

        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0].name,
            "Black T-shirt"
        )

    def test_search_keyword_not_found(self):
        self.manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer",
            "T-Shirt"
        )

        results = self.manager.search("Wedding")

        self.assertEqual(results, [])

    def test_remove_clothing(self):
        self.manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer"
        )

        self.manager.add_clothing(
            "Blue Jeans",
            "Bottoms",
            "Casual",
            "Blue",
            "All-Season"
        )

        self.manager.remove_clothing(
            "Black T-shirt"
        )

        self.assertEqual(
            len(self.manager.wardrobe),
            1
        )

        self.assertEqual(
            self.manager.wardrobe[0].name,
            "Blue Jeans"
        )

    def test_edit_clothing(self):
        self.manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer",
            "T-Shirt"
        )

        self.manager.edit_clothing(
            "Black T-shirt",
            "White Polo",
            "Tops",
            "Casual",
            "White",
            "Summer",
            "Shirt"
        )

        self.assertEqual(
            len(self.manager.wardrobe),
            1
        )

        self.assertEqual(
            self.manager.wardrobe[0].name,
            "White Polo"
        )

        self.assertEqual(
            self.manager.wardrobe[0].color,
            "White"
        )

        self.assertEqual(
            self.manager.wardrobe[0].item_type,
            "Shirt"
        )

    def test_edit_clothing_case_insensitive(self):
        self.manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer"
        )

        self.manager.edit_clothing(
            "BLACK T-SHIRT",
            "White T-shirt",
            "Tops",
            "Casual",
            "White",
            "Summer"
        )

        self.assertEqual(
            self.manager.wardrobe[0].name,
            "White T-shirt"
        )

    def test_edit_clothing_not_found(self):
        self.manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer"
        )

        self.manager.edit_clothing(
            "Blue Shirt",
            "White Shirt",
            "Tops",
            "Casual",
            "White",
            "Summer"
        )

        self.assertEqual(
            len(self.manager.wardrobe),
            1
        )

        self.assertEqual(
            self.manager.wardrobe[0].name,
            "Black T-shirt"
        )

    def test_recommend_items(self):
        self.manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer"
        )

        self.manager.add_clothing(
            "Blue Jeans",
            "Bottoms",
            "Casual",
            "Blue",
            "All-Season"
        )

        self.manager.add_clothing(
            "Black Coat",
            "Outerwear",
            "Casual",
            "Black",
            "Winter"
        )

        results = self.manager.recommend_items(
            "Casual",
            "Summer"
        )

        self.assertEqual(len(results), 2)

    def test_recommend_items_case_insensitive(self):
        self.manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer"
        )

        results = self.manager.recommend_items(
            "CASUAL",
            "SUMMER"
        )

        self.assertEqual(len(results), 1)

    def test_recommend_items_not_found(self):
        self.manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer"
        )

        results = self.manager.recommend_items(
            "Formal",
            "Winter"
        )

        self.assertEqual(results, [])

    def test_generate_outfits(self):
        self.manager.add_clothing(
            "White T-shirt",
            "Tops",
            "Casual",
            "White",
            "Summer"
        )

        self.manager.add_clothing(
            "Blue Jeans",
            "Bottoms",
            "Casual",
            "Blue",
            "All-Season"
        )

        self.manager.add_clothing(
            "White Sneakers",
            "Shoes",
            "Casual",
            "White",
            "All-Season"
        )

        outfits = self.manager.generate_outfits(
            "Casual",
            "Summer"
        )

        self.assertEqual(len(outfits), 1)

    def test_generate_multiple_outfits(self):
        self.manager.add_clothing(
            "White T-shirt",
            "Tops",
            "Casual",
            "White",
            "Summer"
        )

        self.manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer"
        )

        self.manager.add_clothing(
            "Blue Jeans",
            "Bottoms",
            "Casual",
            "Blue",
            "Summer"
        )

        self.manager.add_clothing(
            "Black Trousers",
            "Bottoms",
            "Casual",
            "Black",
            "Summer"
        )

        self.manager.add_clothing(
            "White Sneakers",
            "Shoes",
            "Casual",
            "White",
            "Summer"
        )

        self.manager.add_clothing(
            "Black Sneakers",
            "Shoes",
            "Casual",
            "Black",
            "Summer"
        )

        outfits = self.manager.generate_outfits(
            "Casual",
            "Summer"
        )

        self.assertEqual(len(outfits), 8)

    def test_generate_outfits_not_found(self):
        self.manager.add_clothing(
            "White T-shirt",
            "Tops",
            "Casual",
            "White",
            "Summer"
        )

        self.manager.add_clothing(
            "Blue Jeans",
            "Bottoms",
            "Casual",
            "Blue",
            "Summer"
        )

        outfits = self.manager.generate_outfits(
            "Formal",
            "Winter"
        )

        self.assertEqual(outfits, [])

    def test_show_item_count(self):
        self.manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer"
        )

        self.manager.add_clothing(
            "Blue Jeans",
            "Bottoms",
            "Casual",
            "Blue",
            "All-Season"
        )

        self.assertEqual(
            len(self.manager.wardrobe),
            2
        )

        self.manager.remove_clothing(
            "Black T-shirt"
        )

        self.assertEqual(
            len(self.manager.wardrobe),
            1
        )

    def test_search_category_not_found(self):
        self.manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer"
        )

        results = self.manager.search_by_category(
            "Footwear"
        )

        self.assertEqual(results, [])

    def test_search_occasion_not_found(self):
        self.manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer"
        )

        results = self.manager.search_by_occasion(
            "Wedding"
        )

        self.assertEqual(results, [])

    def test_save_and_load_wardrobe(self):
        self.manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer"
        )

        self.manager.add_clothing(
            "Blue Jeans",
            "Bottoms",
            "Casual",
            "Blue",
            "All-Season"
        )

        self.manager.save_wardrobe()

        new_manager = WardrobeManager(
            db_path=self.database_path
        )

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

    # Phase 4 Task 1 tests

    def test_clothing_item_has_unique_id(self):
        self.manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer"
        )

        self.manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer"
        )

        first_item = self.manager.wardrobe[0]
        second_item = self.manager.wardrobe[1]

        self.assertIsNotNone(first_item.id)
        self.assertIsNotNone(second_item.id)

        self.assertNotEqual(
            first_item.id,
            second_item.id
        )

    def test_clothing_item_image_path(self):
        self.manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer",
            "T-Shirt",
            "uploads/black-tshirt.jpg"
        )

        self.assertEqual(
            self.manager.wardrobe[0].image_path,
            "uploads/black-tshirt.jpg"
        )

    def test_save_and_load_preserves_id_and_image(self):
        self.manager.add_clothing(
            "Black T-shirt",
            "Tops",
            "Casual",
            "Black",
            "Summer",
            "T-Shirt",
            "uploads/black-tshirt.jpg"
        )

        original_id = self.manager.wardrobe[0].id

        self.manager.save_wardrobe()

        new_manager = WardrobeManager(
            db_path=self.database_path
        )

        new_manager.load_wardrobe()

        self.assertEqual(
            new_manager.wardrobe[0].id,
            original_id
        )

        self.assertEqual(
            new_manager.wardrobe[0].image_path,
            "uploads/black-tshirt.jpg"
        )


if __name__ == "__main__":
    unittest.main()