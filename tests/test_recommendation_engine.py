import unittest
import sys
import os
from unittest import result

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "src"
        )
    )
)

from clothing_item import ClothingItem
from recommendation_engine import RecommendationEngine


class TestRecommendationEngine(unittest.TestCase):

    def setUp(self):
        self.wardrobe = [
            ClothingItem(
                "White T-shirt",
                "Tops",
                "Casual",
                "White",
                "Summer",
                "T-Shirt"
            ),
            ClothingItem(
                "Black T-shirt",
                "Tops",
                "Casual",
                "Black",
                "Summer",
                "T-Shirt"
            ),
            ClothingItem(
                "Blue Jeans",
                "Bottoms",
                "Casual",
                "Blue",
                "All-Season",
                "Jeans"
            ),
            ClothingItem(
                "Black Trousers",
                "Bottoms",
                "Casual",
                "Black",
                "Summer",
                "Trousers"
            ),
            ClothingItem(
                "White Sneakers",
                "Shoes",
                "Casual",
                "White",
                "All-Season",
                "Sneakers"
            ),
            ClothingItem(
                "Black Sneakers",
                "Shoes",
                "Casual",
                "Black",
                "Summer",
                "Sneakers"
            ),
            ClothingItem(
                "Black Coat",
                "Outerwear",
                "Casual",
                "Black",
                "Winter",
                "Coat"
            ),
        ]

        self.engine = RecommendationEngine(
            self.wardrobe
        )

    def test_get_suitable_items(self):
        results = self.engine.get_suitable_items(
            "Casual",
            "Summer"
        )

        self.assertEqual(len(results), 6)

        names = [
            item.name
            for item in results
        ]

        self.assertNotIn(
            "Black Coat",
            names
        )

    def test_get_suitable_items_case_insensitive(self):
        results = self.engine.get_suitable_items(
            "CASUAL",
            "SUMMER"
        )

        self.assertEqual(len(results), 6)

    def test_all_season_items_are_included(self):
        results = self.engine.get_suitable_items(
            "Casual",
            "Summer"
        )

        names = [
            item.name
            for item in results
        ]

        self.assertIn(
            "Blue Jeans",
            names
        )

        self.assertIn(
            "White Sneakers",
            names
        )

    def test_generate_outfits(self):
        outfits = self.engine.generate_outfits(
            "Casual",
            "Summer"
        )

        self.assertEqual(
            len(outfits),
            8
        )

    def test_generate_outfits_wrong_occasion(self):
        outfits = self.engine.generate_outfits(
            "Formal",
            "Summer"
        )

        self.assertEqual(
            outfits,
            []
        )

    def test_generate_outfits_wrong_season(self):
        outfits = self.engine.generate_outfits(
            "Casual",
            "Winter"
        )

        self.assertEqual(
            outfits,
            []
        )

    def test_neutral_colors_are_compatible(self):
        result = self.engine._colors_are_compatible(
            "Black",
            "Blue"
        )

        self.assertTrue(result)

    def test_same_colors_are_compatible(self):
        result = self.engine._colors_are_compatible(
            "Black",
            "Black"
        )

        self.assertTrue(result)

    def test_different_non_neutral_colors(self):
        result = self.engine._colors_are_compatible(
        "Red",
        "Blue"
    )
        self.assertFalse(result)

    def test_score_outfit(self):
        outfit = [
            self.wardrobe[0],
            self.wardrobe[2],
            self.wardrobe[4]
        ]

        score = self.engine.score_outfit(
            outfit
        )

        self.assertGreater(
            score,
            0
        )

    def test_recommend_outfits_returns_scores(self):
        recommendations = self.engine.recommend_outfits(
            "Casual",
            "Summer"
        )

        self.assertEqual(
            len(recommendations),
            8
        )

        outfit, score = recommendations[0]

        self.assertEqual(
            len(outfit),
            3
        )

        self.assertIsInstance(
            score,
            int
        )

    def test_recommendations_are_sorted(self):
        recommendations = self.engine.recommend_outfits(
            "Casual",
            "Summer"
        )

        scores = [
            score
            for outfit, score in recommendations
        ]

        self.assertEqual(
            scores,
            sorted(
                scores,
                reverse=True
            )
        )
    def test_score_is_between_zero_and_one_hundred(self):
        recommendations = self.engine.recommend_outfits(
            "Casual",
            "Summer"
        )

        for outfit, score in recommendations:
            self.assertGreaterEqual(
                score,
                0
            )

            self.assertLessEqual(
                score,
                100
            )

    def test_color_score_is_maximum_for_compatible_outfit(self):
        outfit = [
            self.wardrobe[0],  # White T-shirt
            self.wardrobe[2],  # Blue Jeans
            self.wardrobe[4],  # White Sneakers
        ]

        score = self.engine._color_score(
            outfit
        )

        self.assertEqual(
            score,
            30
        )

    def test_complete_outfit_gets_structure_points(self):
        outfit = [
            self.wardrobe[0],
            self.wardrobe[2],
            self.wardrobe[4],
        ]

        score = self.engine.score_outfit(
            outfit
        )

        self.assertGreaterEqual(
            score,
            15
        )

    def test_one_piece_outfit_is_generated(self):

        wardrobe = [
            ClothingItem(
                "Black Dress",
                "One-Piece",
                "Party",
                "Black",
                "Summer",
                "Dress"
            ),
            ClothingItem(
                "Black Heels",
                "Shoes",
                "Party",
                "Black",
                "Summer",
                "Heels"
            ),
        ]

        engine = RecommendationEngine(
            wardrobe
        )

        outfits = engine.generate_outfits(
            "Party",
            "Summer"
        )

        self.assertEqual(
            len(outfits),
            1
        )

        self.assertEqual(
            len(outfits[0]),
            2
        )

        self.assertEqual(
            outfits[0][0].category,
            "One-Piece"
        )

        self.assertEqual(
            outfits[0][1].category,
            "Shoes"
        )


    def test_one_piece_outfit_gets_structure_points(self):

        wardrobe = [
            ClothingItem(
                "Black Dress",
                "One-Piece",
                "Party",
                "Black",
                "Summer",
                "Dress"
            ),
            ClothingItem(
                "Black Heels",
                "Shoes",
                "Party",
                "Black",
                "Summer",
                "Heels"
            ),
        ]

        engine = RecommendationEngine(
            wardrobe
        )

        outfit = [
            wardrobe[0],
            wardrobe[1]
        ]

        score = engine.score_outfit(
            outfit
        )

        self.assertEqual(
            score,
            100
        )


    def test_layered_outfit_is_generated(self):

        wardrobe = [
            ClothingItem(
                "White T-shirt",
                "Tops",
                "Casual",
                "White",
                "Winter",
                "T-Shirt"
            ),
            ClothingItem(
                "Blue Jeans",
                "Bottoms",
                "Casual",
                "Blue",
                "Winter",
                "Jeans"
            ),
            ClothingItem(
                "Black Jacket",
                "Outerwear",
                "Casual",
                "Black",
                "Winter",
                "Jacket"
            ),
            ClothingItem(
                "White Sneakers",
                "Shoes",
                "Casual",
                "White",
                "Winter",
                "Sneakers"
            ),
        ]

        engine = RecommendationEngine(
            wardrobe
        )

        outfits = engine.generate_outfits(
            "Casual",
            "Winter"
        )

        self.assertEqual(
            len(outfits),
            2
        )

        layered_outfits = [
            outfit
            for outfit in outfits
            if len(outfit) == 4
        ]

        self.assertEqual(
            len(layered_outfits),
            1
        )


    def test_layered_outfit_gets_structure_points(self):

        wardrobe = [
            ClothingItem(
                "White T-shirt",
                "Tops",
                "Casual",
                "White",
                "Winter",
                "T-Shirt"
            ),
            ClothingItem(
                "Blue Jeans",
                "Bottoms",
                "Casual",
                "Blue",
                "Winter",
                "Jeans"
            ),
            ClothingItem(
                "Black Jacket",
                "Outerwear",
                "Casual",
                "Black",
                "Winter",
                "Jacket"
            ),
            ClothingItem(
                "White Sneakers",
                "Shoes",
                "Casual",
                "White",
                "Winter",
                "Sneakers"
            ),
        ]

        engine = RecommendationEngine(
            wardrobe
        )

        outfit = [
            wardrobe[0],
            wardrobe[1],
            wardrobe[2],
            wardrobe[3],
        ]

        score = engine.score_outfit(
            outfit
        )

        self.assertGreaterEqual(
            score,
            15
        )

        self.assertLessEqual(
            score,
            100
        )

    def test_same_colors_get_high_color_score(self):

        wardrobe = [
            ClothingItem(
                "Black Shirt",
                "Tops",
                "Casual",
                "Black",
                "Summer"
            ),
            ClothingItem(
                "Black Jeans",
                "Bottoms",
                "Casual",
                "Black",
                "Summer"
            ),
        ]

        engine = RecommendationEngine(
            wardrobe
        )

        score = engine._color_pair_score(
            "Black",
            "Black"
        )

        self.assertEqual(
            score,
            30
        )


    def test_neutral_color_gets_high_color_score(self):

        wardrobe = []

        engine = RecommendationEngine(
            wardrobe
        )

        score = engine._color_pair_score(
            "White",
            "Red"
        )

        self.assertEqual(
            score,
            30
        )


    def test_same_color_family_gets_good_score(self):

        wardrobe = []

        engine = RecommendationEngine(
            wardrobe
        )

        score = engine._color_pair_score(
            "Blue",
            "Navy"
        )

        self.assertEqual(
            score,
            27
        )


    def test_complementary_colors_get_good_score(self):

        wardrobe = []

        engine = RecommendationEngine(
            wardrobe
        )

        score = engine._color_pair_score(
            "Red",
            "Green"
        )

        self.assertEqual(
            score,
            24
        )

if __name__ == "__main__":
    unittest.main()