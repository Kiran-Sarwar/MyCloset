from pathlib import Path
from uuid import uuid4

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify
)

from werkzeug.utils import secure_filename
from wardrobe_manager import WardrobeManager


app = Flask(__name__)

wardrobe_manager = WardrobeManager()
wardrobe_manager.load_wardrobe()


# --------------------------------------------------
# Image Upload Configuration
# --------------------------------------------------

UPLOAD_FOLDER = Path(app.static_folder) / "uploads"

ALLOWED_IMAGE_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "gif",
    "webp"
}

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

UPLOAD_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


def allowed_image(filename: str) -> bool:
    """
    Check whether the uploaded file has
    an allowed image extension.
    """

    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in ALLOWED_IMAGE_EXTENSIONS


def save_uploaded_image(file) -> str:
    """
    Save an uploaded image and return the
    relative path used by the application.
    """

    if file is None:
        return ""

    if not file.filename:
        return ""

    if not allowed_image(file.filename):
        return ""

    original_filename = secure_filename(
        file.filename
    )

    extension = Path(
        original_filename
    ).suffix.lower()

    unique_filename = (
        f"{uuid4()}{extension}"
    )

    file_path = (
        UPLOAD_FOLDER / unique_filename
    )

    file.save(file_path)

    return f"uploads/{unique_filename}"


def get_dashboard_data():

    return {
        "total_items": len(
            wardrobe_manager.wardrobe
        ),

        "tops_count": (
            wardrobe_manager.get_category_count(
                "Tops"
            )
        ),

        "bottoms_count": (
            wardrobe_manager.get_category_count(
                "Bottoms"
            )
        ),

        "one_piece_count": (
            wardrobe_manager.get_category_count(
                "One-Piece"
            )
        ),

        "outerwear_count": (
            wardrobe_manager.get_category_count(
                "Outerwear"
            )
        ),

        "shoes_count": (
            wardrobe_manager.get_category_count(
                "Shoes"
            )
        ),

        "accessories_count": (
            wardrobe_manager.get_category_count(
                "Accessories"
            )
        )
    }


# --------------------------------------------------
# Home
# --------------------------------------------------

@app.route("/")
def home():

    dashboard_data = get_dashboard_data()

    return render_template(
        "index.html",
        wardrobe=wardrobe_manager.wardrobe,
        **dashboard_data
    )


# --------------------------------------------------
# Detect Clothing Image
# --------------------------------------------------

@app.route(
    "/detect",
    methods=["POST"]
)
def detect_image():

    image = request.files.get("image")

    if image is None or not image.filename:

        return jsonify({
            "success": False,
            "message": "No image was provided."
        }), 400


    if not allowed_image(image.filename):

        return jsonify({
            "success": False,
            "message": "Unsupported image format."
        }), 400


    original_filename = secure_filename(
        image.filename
    )

    extension = Path(
        original_filename
    ).suffix.lower()

    temporary_filename = (
        f"detect_{uuid4()}{extension}"
    )

    temporary_path = (
        UPLOAD_FOLDER / temporary_filename
    )


    try:

        image.save(temporary_path)


        detection = (
            wardrobe_manager
            .detect_uploaded_clothing(
                str(temporary_path)
            )
        )


        if detection is None:

            return jsonify({
                "success": False,
                "message": (
                    "No clothing item was detected."
                )
            })


        detected_category = (
            detection["category"]
        )


        mycloset_category = (
            wardrobe_manager
            .convert_detection_to_category(
                detected_category
            )
        )


        # Use the user-friendly clothing name

        detected_item_type = (
            detection["display_name"]
        )


        return jsonify({

            "success": True,

            "category": mycloset_category,

            "item_type": detected_item_type,

            "confidence": detection["confidence"],

            # Send confidence status to the frontend
            "confidence_status": (
                detection["confidence_status"]
            )

        })


    except Exception as error:

        print(
            "\nComputer Vision detection failed:"
        )

        print(error)


        return jsonify({
            "success": False,
            "message": (
                "Could not analyze the image."
            )
        }), 500


    finally:

        if temporary_path.exists():

            temporary_path.unlink()


# --------------------------------------------------
# Add Clothing Item
# --------------------------------------------------

@app.route(
    "/add",
    methods=["GET", "POST"]
)
def add_item():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()


        category = request.form.get(
            "category",
            ""
        ).strip()


        item_type = request.form.get(
            "item_type",
            ""
        ).strip()


        occasion = request.form.get(
            "occasion",
            ""
        ).strip()


        color = request.form.get(
            "color",
            ""
        ).strip()


        season = request.form.get(
            "season",
            ""
        ).strip()


        image = request.files.get(
            "image"
        )


        image_path = save_uploaded_image(
            image
        )


        # --------------------------------------------------
        # Computer Vision Detection
        # --------------------------------------------------

        if image_path:

            uploaded_file_path = (
                UPLOAD_FOLDER
                / Path(image_path).name
            )


            try:

                detection = (
                    wardrobe_manager
                    .detect_uploaded_clothing(
                        str(uploaded_file_path)
                    )
                )


                if detection:

                    detected_category = (
                        detection["category"]
                    )


                    # Use the friendly display name

                    detected_item_type = (
                        detection["display_name"]
                    )


                    category = (
                        wardrobe_manager
                        .convert_detection_to_category(
                            detected_category
                        )
                    )


                    item_type = detected_item_type


                    print(
                        "\nComputer Vision Detection:"
                    )


                    print(
                        f"- Category: {category}"
                    )


                    print(
                        f"- Type: {item_type}"
                    )


                    print(
                        f"- Confidence: "
                        f"{detection['confidence']}"
                    )


                    print(
                        f"- Confidence Status: "
                        f"{detection['confidence_status']}"
                    )


                else:

                    print(
                        "\nNo clothing item detected."
                    )


            except Exception as error:

                print(
                    "\nComputer Vision detection "
                    "failed:"
                )

                print(error)


                print(
                    "Continuing with the "
                    "user-provided category and type."
                )


        wardrobe_manager.add_clothing(
            name,
            category,
            occasion,
            color,
            season,
            item_type,
            image_path
        )


        wardrobe_manager.save_wardrobe()


        return redirect(
            url_for("home")
        )


    return render_template(
        "add_item.html"
    )


# --------------------------------------------------
# Search and Filters
# --------------------------------------------------

@app.route("/search")
def search():

    name = request.args.get(
        "name",
        ""
    ).strip()


    category = request.args.get(
        "category",
        ""
    ).strip()


    item_type = request.args.get(
        "item_type",
        ""
    ).strip()


    occasion = request.args.get(
        "occasion",
        ""
    ).strip()


    color = request.args.get(
        "color",
        ""
    ).strip()


    season = request.args.get(
        "season",
        ""
    ).strip()


    results = wardrobe_manager.wardrobe


    # Search by item name

    if name:

        results = [
            item
            for item in results
            if name.lower()
            in item.name.lower()
        ]


    # Filter by category

    if category:

        results = [
            item
            for item in results
            if item.category.lower()
            == category.lower()
        ]


    # Filter by item type

    if item_type:

        results = [
            item
            for item in results
            if item.item_type.lower()
            == item_type.lower()
        ]


    # Filter by occasion

    if occasion:

        results = [
            item
            for item in results
            if item.occasion.lower()
            == occasion.lower()
        ]


    # Filter by color

    if color:

        results = [
            item
            for item in results
            if item.color.lower()
            == color.lower()
        ]


    # Filter by season

    if season:

        results = [
            item
            for item in results
            if item.season.lower()
            == season.lower()
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


# --------------------------------------------------
# Outfit Recommendations
# --------------------------------------------------

@app.route("/outfits")
def outfits():

    occasion = request.args.get(
        "occasion",
        ""
    ).strip()


    season = request.args.get(
        "season",
        ""
    ).strip()


    recommendations = []


    if occasion and season:

        recommendations = (
            wardrobe_manager
            .recommend_outfits(
                occasion,
                season
            )
        )


    return render_template(
        "outfits.html",
        recommendations=recommendations,
        selected_occasion=occasion,
        selected_season=season
    )


# --------------------------------------------------
# Edit Clothing Item
# --------------------------------------------------

@app.route(
    "/edit/<name>",
    methods=["GET", "POST"]
)
def edit_item(name):

    item = None


    for clothing_item in wardrobe_manager.wardrobe:

        if clothing_item.name.lower() == name.lower():

            item = clothing_item

            break


    if item is None:

        return redirect(
            url_for("home")
        )


    if request.method == "POST":

        new_name = request.form.get(
            "name",
            ""
        ).strip()


        category = request.form.get(
            "category",
            ""
        ).strip()


        item_type = request.form.get(
            "item_type",
            ""
        ).strip()


        occasion = request.form.get(
            "occasion",
            ""
        ).strip()


        color = request.form.get(
            "color",
            ""
        ).strip()


        season = request.form.get(
            "season",
            ""
        ).strip()


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


        return redirect(
            url_for("home")
        )


    return render_template(
        "edit_item.html",
        item=item
    )


# --------------------------------------------------
# Remove Clothing Item
# --------------------------------------------------

@app.route(
    "/remove/<name>",
    methods=["POST"]
)
def remove_item(name):

    item = None


    for clothing_item in wardrobe_manager.wardrobe:

        if clothing_item.name.lower() == name.lower():

            item = clothing_item

            break


    if item is not None:

        wardrobe_manager.remove_clothing(
            name
        )

        wardrobe_manager.save_wardrobe()


    return redirect(
        url_for("home")
    )


# --------------------------------------------------
# Run Application
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        debug=True
    )