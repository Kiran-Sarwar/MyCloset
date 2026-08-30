from itertools import product

from clothing_item import ClothingItem


class RecommendationEngine:
    """
    Rule-based outfit recommendation engine for MyCloset.

    The engine:
    - filters clothing by occasion and season
    - supports multiple outfit structures
    - evaluates color compatibility
    - scores outfits from 0 to 100
    - ranks recommendations from highest to lowest
    """

    NEUTRAL_COLORS = {
        "black",
        "white",
        "grey",
        "gray",
        "beige",
        "cream",
        "navy",
        "brown",
    }

    COLOR_FAMILIES = {
        "red": {
            "red",
            "maroon",
            "burgundy",
            "pink",
        },
        "blue": {
            "blue",
            "navy",
            "sky blue",
            "light blue",
        },
        "green": {
            "green",
            "olive",
            "mint",
        },
        "yellow": {
            "yellow",
            "mustard",
        },
        "purple": {
            "purple",
            "lavender",
        },
        "orange": {
            "orange",
            "rust",
        },
        "brown": {
            "brown",
            "tan",
            "camel",
            "beige",
        },
    }

    COMPLEMENTARY_COLORS = {
        frozenset({"red", "green"}),
        frozenset({"blue", "orange"}),
        frozenset({"yellow", "purple"}),
    }

    def __init__(
        self,
        wardrobe: list[ClothingItem]
    ) -> None:

        self.wardrobe = wardrobe

    def _matches_season(
        self,
        item: ClothingItem,
        season: str
    ) -> bool:

        item_season = item.season.strip().lower()
        requested_season = season.strip().lower()

        return (
            item_season == requested_season
            or item_season in {
                "all-season",
                "all season",
            }
        )

    def _matches_occasion(
        self,
        item: ClothingItem,
        occasion: str
    ) -> bool:

        return (
            item.occasion.strip().lower()
            == occasion.strip().lower()
        )

    def get_suitable_items(
        self,
        occasion: str,
        season: str
    ) -> list[ClothingItem]:

        return [
            item
            for item in self.wardrobe
            if (
                self._matches_occasion(
                    item,
                    occasion
                )
                and self._matches_season(
                    item,
                    season
                )
            )
        ]

    def _get_color_family(
        self,
        color: str
    ) -> str | None:

        normalized_color = color.strip().lower()

        for family_name, family_colors in self.COLOR_FAMILIES.items():

            if normalized_color in family_colors:
                return family_name

        return None

    def _colors_are_compatible(
        self,
        first_color: str,
        second_color: str
    ) -> bool:

        first = first_color.strip().lower()
        second = second_color.strip().lower()

        # Missing colors are treated as compatible
        # because there is not enough information
        # to reject the combination.
        if not first or not second:
            return True

        # Exact same color is compatible.
        if first == second:
            return True

        first_family = self._get_color_family(first)
        second_family = self._get_color_family(second)

        # Same color family is compatible.
        if (
            first_family is not None
            and second_family is not None
            and first_family == second_family
        ):
            return True

        # Complementary color families are compatible.
        if (
            first_family is not None
            and second_family is not None
            and frozenset({
                first_family,
                second_family
            }) in self.COMPLEMENTARY_COLORS
        ):
            return True

        # Neutral colors work with other colors.
        if (
            first in self.NEUTRAL_COLORS
            or second in self.NEUTRAL_COLORS
        ):
            return True

        # Different non-neutral, non-complementary
        # colors are considered incompatible.
        return False

    def _color_pair_score(
        self,
        first_color: str,
        second_color: str
    ) -> int:
        """
        Score a pair of colors.

        Maximum pair score: 30.

        Scoring:
        - Same color: 30
        - Same color family: 27
        - Neutral with another color: 30
        - Complementary colors: 24
        - Unknown/missing color: 20
        - Other known combinations: 12
        """

        first = first_color.strip().lower()
        second = second_color.strip().lower()

        # Missing or unknown color information.
        if not first or not second:
            return 20

        # Exact same color.
        if first == second:
            return 30

        first_family = self._get_color_family(first)
        second_family = self._get_color_family(second)

        # Same family must be checked BEFORE neutral colors.
        # Example: navy + blue = same blue family = 27.
        if (
            first_family is not None
            and second_family is not None
            and first_family == second_family
        ):
            return 27

        # Neutral colors combine well with other colors.
        if (
            first in self.NEUTRAL_COLORS
            or second in self.NEUTRAL_COLORS
        ):
            return 30

        # Complementary color families.
        if (
            first_family is not None
            and second_family is not None
            and frozenset({
                first_family,
                second_family
            }) in self.COMPLEMENTARY_COLORS
        ):
            return 24

        # Unknown color.
        if first_family is None or second_family is None:
            return 20

        # Different known non-neutral colors.
        return 12

    def _color_score(
        self,
        outfit: list[ClothingItem]
    ) -> int:
        """
        Calculate the overall color compatibility.

        Maximum: 30 points.
        """

        if len(outfit) < 2:
            return 30

        pair_scores = []

        for index, first_item in enumerate(outfit):

            for second_item in outfit[index + 1:]:

                pair_scores.append(
                    self._color_pair_score(
                        first_item.color,
                        second_item.color
                    )
                )

        if not pair_scores:
            return 30

        return round(
            sum(pair_scores) / len(pair_scores)
        )

    def _has_complete_structure(
        self,
        outfit: list[ClothingItem]
    ) -> bool:

        categories = {
            item.category.strip().lower()
            for item in outfit
        }

        # Standard:
        # Top + Bottom + Shoes
        if {
            "tops",
            "bottoms",
            "shoes",
        }.issubset(categories):

            return True

        # One-piece:
        # One-Piece + Shoes
        if {
            "one-piece",
            "shoes",
        }.issubset(categories):

            return True

        return False

    def _has_layered_structure(
        self,
        outfit: list[ClothingItem]
    ) -> bool:

        categories = {
            item.category.strip().lower()
            for item in outfit
        }

        return {
            "tops",
            "bottoms",
            "outerwear",
            "shoes",
        }.issubset(categories)

    def score_outfit(
        self,
        outfit: list[ClothingItem]
    ) -> int:
        """
        Score an outfit from 0 to 100.

        Scoring:
        - Occasion: 30
        - Season: 25
        - Colors: 30
        - Structure: 15
        """

        if not outfit:
            return 0

        score = 0

        # ------------------------------------------
        # Occasion
        # ------------------------------------------

        occasions = {
            item.occasion.strip().lower()
            for item in outfit
        }

        if len(occasions) == 1:
            score += 30

        # ------------------------------------------
        # Season
        # ------------------------------------------

        seasons = {
            item.season.strip().lower()
            for item in outfit
        }

        if len(seasons) == 1:

            score += 25

        elif all(
            season in {
                "all-season",
                "all season",
            }
            for season in seasons
        ):

            score += 25

        # ------------------------------------------
        # Colors
        # ------------------------------------------

        score += self._color_score(
            outfit
        )

        # ------------------------------------------
        # Structure
        # ------------------------------------------

        if self._has_complete_structure(
            outfit
        ):

            score += 15

        elif self._has_layered_structure(
            outfit
        ):

            score += 15

        return min(
            score,
            100
        )

    def generate_outfits(
        self,
        occasion: str,
        season: str
    ) -> list[list[ClothingItem]]:

        suitable_items = self.get_suitable_items(
            occasion,
            season
        )

        tops = [
            item
            for item in suitable_items
            if item.category.strip().lower()
            == "tops"
        ]

        bottoms = [
            item
            for item in suitable_items
            if item.category.strip().lower()
            == "bottoms"
        ]

        one_pieces = [
            item
            for item in suitable_items
            if item.category.strip().lower()
            == "one-piece"
        ]

        outerwear = [
            item
            for item in suitable_items
            if item.category.strip().lower()
            == "outerwear"
        ]

        shoes = [
            item
            for item in suitable_items
            if item.category.strip().lower()
            == "shoes"
        ]

        outfits = []

        # ------------------------------------------
        # Standard outfits
        # Top + Bottom + Shoes
        # ------------------------------------------

        for top, bottom, shoe in product(
            tops,
            bottoms,
            shoes
        ):

            outfits.append([
                top,
                bottom,
                shoe,
            ])

        # ------------------------------------------
        # One-piece outfits
        # One-Piece + Shoes
        # ------------------------------------------

        for one_piece, shoe in product(
            one_pieces,
            shoes
        ):

            outfits.append([
                one_piece,
                shoe,
            ])

        # ------------------------------------------
        # Layered outfits
        # Top + Bottom + Outerwear + Shoes
        # ------------------------------------------

        for top, bottom, jacket, shoe in product(
            tops,
            bottoms,
            outerwear,
            shoes
        ):

            outfits.append([
                top,
                bottom,
                jacket,
                shoe,
            ])

        return outfits

    def recommend_outfits(
        self,
        occasion: str,
        season: str
    ) -> list[tuple[list[ClothingItem], int]]:

        outfits = self.generate_outfits(
            occasion,
            season
        )

        scored_outfits = [
            (
                outfit,
                self.score_outfit(outfit)
            )
            for outfit in outfits
        ]

        scored_outfits.sort(
            key=lambda result: result[1],
            reverse=True
        )

        return scored_outfits