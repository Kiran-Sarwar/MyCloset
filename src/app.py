from flask import Flask, render_template
from wardrobe_manager import WardrobeManager

app = Flask(__name__)

wardrobe_manager = WardrobeManager()
wardrobe_manager.load_wardrobe()


@app.route("/")
def home():
    return render_template(
        "index.html",
        wardrobe=wardrobe_manager.wardrobe
    )


if __name__ == "__main__":
    app.run(debug=True)