# Phase 3C — Rule-Based Recommendation Engine

**Status:** Completed

**Completion Date:** August 30, 2026

## Overview

Phase 3C introduced the first intelligent recommendation layer to MyCloset.

The goal of this phase was to improve the basic outfit generator from Phase 3 by introducing rule-based outfit evaluation and ranking.

Instead of simply generating possible combinations, MyCloset now evaluates outfits based on factors such as color compatibility and outfit structure, then ranks the generated outfits by their compatibility score.

This phase establishes the foundation for future AI-powered styling and recommendation features.

## Features Completed

### 1. Rule-Based Recommendation Engine

A dedicated `RecommendationEngine` was introduced to handle outfit generation, evaluation, scoring, and ranking.

The recommendation engine works with the existing wardrobe data provided by `ClothingItem`.

### 2. Suitable Item Filtering

The recommendation engine identifies clothing items suitable for a selected:

* Occasion
* Season

Items are matched case-insensitively.

Items marked as `All-Season` are also considered suitable for seasonal recommendations.

### 3. Outfit Generation

The engine generates possible outfit combinations from suitable wardrobe items.

The current system supports combinations using:

* Tops
* Bottoms
* Shoes
* One-Piece items
* Outerwear

The engine can generate both standard outfits and layered outfits.

### 4. One-Piece Outfit Support

The recommendation engine supports outfits built around one-piece clothing items such as dresses.

A one-piece outfit can be combined with suitable shoes without requiring a separate top and bottom.

For example:

```text
Dress + Heels
```

### 5. Layered Outfit Support

The engine supports layered outfits by allowing outerwear to be added to a suitable base outfit.

For example:

```text
T-shirt + Jeans + Jacket + Sneakers
```

This allows the recommendation system to create more realistic outfits for seasons such as Winter.

### 6. Color Compatibility

A rule-based color compatibility system was introduced.

The engine evaluates relationships between clothing colors.

The current rules support:

* Same colors
* Neutral colors
* Compatible color families
* Complementary colors
* Incompatible non-neutral colors

Examples include:

```text
Black + Black → Highly compatible
White + Red → Highly compatible
Blue + Navy → Good compatibility
Red + Green → Compatible under complementary-color rules
```

Incompatible combinations receive lower scores.

### 7. Outfit Scoring

Each generated outfit receives a compatibility score from **0 to 100**.

The score considers factors including:

* Color compatibility
* Outfit structure
* Completeness of the outfit
* Compatibility between clothing items

A complete outfit receives structure points, while compatible colors increase the overall score.

### 8. Outfit Ranking

Generated outfits are evaluated and sorted by their score.

The highest-scoring outfit is returned first.

This changes the system from simply generating combinations to actually recommending the combinations that are considered better according to the current rules.

### 9. Web Integration

The recommendation engine was integrated into the existing Flask application.

The `/outfits` route now uses the recommendation system to generate ranked outfit recommendations.

The Outfit Recommendations page displays:

* Outfit number
* Occasion
* Season
* Compatibility score
* Clothing categories
* Clothing names
* Clothing colors
* Clothing images when available

### 10. Image Support in Recommendations

Existing wardrobe images are now displayed alongside clothing items in recommended outfits when an image is available.

This makes the recommendation page more visual and provides a better foundation for future computer-vision features.

## Technical Implementation

The recommendation system was separated into its own module:

```text
src/recommendation_engine.py
```

The main responsibilities of `RecommendationEngine` include:

```text
get_suitable_items()
generate_outfits()
score_outfit()
recommend_outfits()
_colors_are_compatible()
_color_pair_score()
_color_score()
```

`WardrobeManager` provides access to the recommendation system through:

```text
generate_outfits()
recommend_outfits()
```

The Flask application uses:

```text
/outfits
```

to display the recommendations through the web interface.

## Recommendation Process

The current recommendation pipeline works approximately as follows:

```text
User selects occasion + season
            ↓
Find suitable wardrobe items
            ↓
Separate items by category
            ↓
Generate possible outfit combinations
            ↓
Evaluate outfit structure
            ↓
Evaluate color compatibility
            ↓
Calculate outfit score
            ↓
Sort outfits by score
            ↓
Display ranked recommendations
```

## Testing

A dedicated test suite was added for the recommendation engine:

```text
tests/test_recommendation_engine.py
```

The tests cover:

* Suitable item filtering
* Case-insensitive filtering
* All-season item support
* Outfit generation
* Invalid occasion handling
* Invalid season handling
* Color compatibility
* Color scoring
* Outfit scoring
* Score range validation
* Recommendation ranking
* One-piece outfit generation
* One-piece outfit scoring
* Layered outfit generation
* Layered outfit scoring
* Same-color compatibility
* Neutral-color compatibility
* Color-family compatibility
* Complementary-color compatibility

The complete test suite passed successfully after implementation.

## Current Limitations

The recommendation engine is intentionally rule-based and does not yet use machine learning or artificial intelligence.

It currently does not:

* Understand clothing from images automatically
* Detect clothing categories using computer vision
* Automatically identify clothing colors from photographs
* Understand patterns or textures
* Learn a user's personal style
* Learn from user feedback
* Understand fashion trends
* Consider body type or fit
* Automatically determine the occasion
* Automatically determine the season from an image
* Generate completely novel outfits using generative AI

The system depends on the clothing information currently stored in the wardrobe.

These limitations are intentional because the recommendation engine is designed to serve as a foundation for the more advanced intelligent features planned for later phases.

## Relationship to Phase 3

Phase 3 introduced the basic outfit generator.

Phase 3C improves that generator by adding intelligence through rule-based evaluation.

The progression is:

```text
Phase 3:
Generate possible outfits

        ↓

Phase 3C:
Generate → Evaluate → Score → Rank

        ↓

Future:
Understand images → Learn preferences → Recommend intelligently
```

## Phase 3C Outcome

Phase 3C successfully transformed MyCloset's basic outfit generator into a rule-based recommendation system.

MyCloset can now:

1. Find suitable clothing based on occasion and season.
2. Generate different outfit combinations.
3. Support one-piece outfits.
4. Support layered outfits.
5. Evaluate color compatibility.
6. Score generated outfits.
7. Rank outfits by compatibility.
8. Display ranked recommendations through the Flask web interface.
9. Display clothing images in recommendations when available.

This provides the foundation for the next major stage of the MyCloset roadmap.

## Next Phase

The next stage is **Phase 3D — Computer Vision**.

The goal of Phase 3D is to reduce the amount of information users need to enter manually.

Instead of requiring users to manually provide all clothing attributes, MyCloset will begin analyzing uploaded clothing photographs.

The longer-term workflow is:

```text
User uploads clothing photo
            ↓
Computer Vision analyzes image
            ↓
Identify clothing category/type
            ↓
Extract basic visual attributes
            ↓
Store clothing information
            ↓
Recommendation Engine
            ↓
Outfit Recommendations
```

Phase 3D will therefore connect the existing wardrobe and recommendation foundation to the original vision of an intelligent digital wardrobe.