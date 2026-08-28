from flask import Flask, render_template, request, redirect, url_for
from wardrobe_manager import WardrobeManager

app = Flask(__name__)

wardrobe_manager = WardrobeManager()
wardrobe_manager.load_wardrobe()


def get_dashboard_data():
    return {
        "total_items": len(wardrobe_manager.wardrobe),
        "tops_count": wardrobe_manager.get_category_count("Tops"),
        "bottoms_count": wardrobe_manager.get_category_count("Bottoms"),
        "one_piece_count": wardrobe_manager.get_category_count("One-Piece"),
        "outerwear_count": wardrobe_manager.get_category_count("Outerwear"),
        "shoes_count": wardrobe_manager.get_category_count("Shoes"),
        "accessories_count": wardrobe_manager.get_category_count("Accessories")
    }


@app.route("/")
def home():
    dashboard_data = get_dashboard_data()

    return render_template(
        "index.html",
        wardrobe=wardrobe_manager.wardrobe,
        **dashboard_data
    )


@app.route("/add", methods=["GET", "POST"])
def add_item():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        item_type = request.form.get("item_type", "").strip()
        occasion = request.form.get("occasion", "").strip()
        color = request.form.get("color", "").strip()
        season = request.form.get("season", "").strip()

        wardrobe_manager.add_clothing(
            name,
            category,
            occasion,
            color,
            season,
            item_type
        )

        wardrobe_manager.save_wardrobe()

        return redirect(url_for("home"))

    return render_template("add_item.html")


@app.route("/search")
def search():
    name = request.args.get("name", "").strip()
    category = request.args.get("category", "").strip()
    item_type = request.args.get("item_type", "").strip()
    occasion = request.args.get("occasion", "").strip()
    color = request.args.get("color", "").strip()
    season = request.args.get("season", "").strip()

    results = wardrobe_manager.wardrobe

    # Search by item name
    if name:
        results = [
            item
            for item in results
            if name.lower() in item.name.lower()
        ]

    # Filter by category
    if category:
        results = [
            item
            for item in results
            if item.category.lower() == category.lower()
        ]

    # Filter by item type
    if item_type:
        results = [
            item
            for item in results
            if item.item_type.lower() == item_type.lower()
        ]

    # Filter by occasion
    if occasion:
        results = [
            item
            for item in results
            if item.occasion.lower() == occasion.lower()
        ]

    # Filter by color
    if color:
        results = [
            item
            for item in results
            if item.color.lower() == color.lower()
        ]

    # Filter by season
    if season:
        results = [
            item
            for item in results
            if item.season.lower() == season.lower()
        ]

    dashboard_data = get_dashboard_data()

    return render_template(
        "index.html",
        wardrobe=results,
        search_name=name,
        search_category=category,
        search_type=item_type,
        search_occasion=occasion,
        search_color=color,
        search_season=season,
        **dashboard_data
    )


@app.route("/remove/<name>", methods=["POST"])
def remove_item(name):
    wardrobe_manager.remove_clothing(name)
    wardrobe_manager.save_wardrobe()

    return redirect(url_for("home"))


@app.route("/edit/<name>", methods=["GET", "POST"])
def edit_item(name):
    item = None

    for clothing_item in wardrobe_manager.wardrobe:
        if clothing_item.name.lower() == name.lower():
            item = clothing_item
            break

    if item is None:
        return redirect(url_for("home"))

    if request.method == "POST":
        new_name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        item_type = request.form.get("item_type", "").strip()
        occasion = request.form.get("occasion", "").strip()
        color = request.form.get("color", "").strip()
        season = request.form.get("season", "").strip()

        wardrobe_manager.edit_clothing(
            name,
            new_name,
            category,
            occasion,
            color,
            season,
            item_type
        )

        wardrobe_manager.save_wardrobe()

        return redirect(url_for("home"))

    return render_template(
        "edit_item.html",
        item=item
    )


if __name__ == "__main__":
    app.run(debug=True)