from flask import Flask, render_template, request, redirect, url_for

from wardrobe_manager import WardrobeManager


app = Flask(__name__)

wardrobe_manager = WardrobeManager()

wardrobe_manager.load_wardrobe()


def get_dashboard_data():

    return {
        "total_items": len(wardrobe_manager.wardrobe),
        "tops_count": wardrobe_manager.get_category_count("Tops"),
        "bottoms_count": wardrobe_manager.get_category_count("Bottoms")
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

    category = request.args.get("category", "").strip()
    item_type = request.args.get("item_type", "").strip()
    occasion = request.args.get("occasion", "").strip()
    color = request.args.get("color", "").strip()
    season = request.args.get("season", "").strip()

    results = wardrobe_manager.wardrobe

    if category:

        results = [
            item
            for item in results
            if item.category.lower() == category.lower()
        ]

    if item_type:

        results = [
            item
            for item in results
            if item.item_type.lower() == item_type.lower()
        ]

    if occasion:

        results = [
            item
            for item in results
            if item.occasion.lower() == occasion.lower()
        ]

    if color:

        results = [
            item
            for item in results
            if item.color.lower() == color.lower()
        ]

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


if __name__ == "__main__":
    app.run(debug=True)