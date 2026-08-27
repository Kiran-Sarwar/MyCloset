# MyCloset 🧥

MyCloset is a digital wardrobe application built with Python and Flask. It allows users to manage their clothing items through a simple web interface and provides a foundation for future wardrobe organization and AI-powered styling features.

##  Current Features

MyCloset currently supports:

* Add clothing items to your wardrobe
* Remove clothing items
* Persistent wardrobe storage
* Dashboard wardrobe statistics
* Filter clothing items by:

  * Category
  * Type
  * Occasion
  * Color
  * Season
* Combine multiple filters
* Dynamic clothing-type filtering
* Responsive web interface
* Automated tests for wardrobe management functionality

##  Tech Stack

* **Python**
* **Flask**
* **HTML**
* **CSS**
* **Jinja2**
* **unittest**
* **Git & GitHub**

##  Project Structure

```text
MyCloset/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   └── bug_report.md
│   └── pull_request_template.md
├── docs/
│   ├── phase-0-product-definition.md
│   ├── phase-1-backend-and-flask-foundation.md
│   └── PHASE_2.md
├── src/
│   ├── app.py
│   ├── clothing_item.py
│   ├── main.py
│   ├── wardrobe_manager.py
│   ├── wardrobe.txt
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   └── templates/
│       ├── add_item.html
│       ├── base.html
│       └── index.html
├── tests/
│   └── test_wardrobe_manager.py
├── .gitignore
├── CONTRIBUTING.md
└── README.md
```

##  Getting Started

### Prerequisites

Make sure Python is installed on your system.

You can check your Python installation with:

```bash
python --version
```

### Clone the Repository

```bash
git clone https://github.com/Kiran-Sarwar/MyCloset.git
cd MyCloset
```

### Install Flask

If Flask is not already installed:

```bash
pip install flask
```

##  Running MyCloset

From the project root, run:

```bash
python src/app.py
```

Flask will start the development server. Open the local address displayed in your terminal in your web browser.

##  Running Tests

To run the automated test suite:

```bash
python -m unittest discover tests
```

Make sure all existing tests pass before submitting a contribution.

##  Contributing

Contributions are welcome!

If you would like to contribute:

1. Check the open GitHub Issues.
2. Look for issues labeled `good first issue` if you're new to the project.
3. Fork the repository.
4. Create a new branch for your contribution.
5. Make your changes.
6. Run the test suite.
7. Push your branch.
8. Open a Pull Request.

Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) for the complete contribution guidelines.

### Good First Issues

Beginner-friendly issues are available for contributors who are new to open-source development.

If you are interested in working on an issue, please check the repository's Issues section and follow the instructions provided in the issue.

##  Roadmap

MyCloset is being developed in several stages.

### Phase 3B — Better Wardrobe Data

* Improve clothing metadata
* Add search
* Add sorting
* Improve wardrobe organization
* Prepare data structures for recommendations

### Phase 3C — Recommendation Engine

* Build rule-based recommendations
* Recommend outfits based on occasion, season, and color
* Learn the fundamentals of recommendation systems
* Test recommendation logic

### Phase 3D — Computer Vision

* Clothing image upload
* Image processing
* Clothing classification
* Connect image information to wardrobe items

### Phase 3E — AI Stylist

* Outfit recommendations
* Natural-language interaction
* Smarter personalization
* AI-assisted styling

### Phase 3F — Polish & Deployment

* Security improvements
* Better user experience
* Performance improvements
* Deployment
* Documentation
* Portfolio presentation

##  Current Status

MyCloset has completed:

* Phase 0 — Product Definition
* Phase 1 — Backend and Flask Foundation
* Phase 2 — Flask Web Application
* Phase 3A — Open Source Foundation

The project is currently moving into **Phase 3B: Better Wardrobe Data**.

##  About the Project

MyCloset is being developed as a learning-focused open-source project with the long-term goal of exploring recommendation systems, computer vision, and AI-assisted styling.

Contributions, ideas, bug reports, and feedback are welcome.

---

**Made with Python and Flask.**
