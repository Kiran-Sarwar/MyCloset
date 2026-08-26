# MyCloset — Phase 1: Backend and Flask Foundation

## 1. Phase Overview

Phase 1 focused on building the core backend of MyCloset and connecting it to a basic web interface.

The goal of this phase was to take the Python-based wardrobe system developed during the preparation stage and make its stored wardrobe data accessible through a Flask website.

---

## 2. Objectives

The main objectives of Phase 1 were:

- Build the core clothing item model.
- Create a wardrobe management system.
- Add basic wardrobe operations.
- Store wardrobe data in a file.
- Load saved wardrobe data when the application starts.
- Create unit tests for the wardrobe manager.
- Introduce Flask.
- Connect the Python backend to an HTML webpage.
- Display saved wardrobe items dynamically in the browser.
- Maintain the project using Git and GitHub.

---

## 3. Project Structure

At the end of Phase 1, the project has the following structure:

    MyCloset/
    │
    ├── docs/
    │   └── phase 0 product definition.md
    │
    ├── src/
    │   ├── __pycache__/
    │   ├── templates/
    │   │   └── index.html
    │   ├── app.py
    │   ├── clothing_items.py
    │   ├── main.py
    │   ├── wardrobe.txt
    │   └── wardrobe_manager.py
    │
    ├── tests/
    │   └── test_wardrobe_manager.py
    │
    └── .gitignore

The `__pycache__` directory is ignored by Git through the project's `.gitignore` file.

---

## 4. ClothingItem Class

The `ClothingItem` class represents an individual item in the wardrobe.

Each clothing item contains:

- Name
- Category
- Occasion
- Color
- Season

This class provides the basic data model for MyCloset.

---

## 5. WardrobeManager Class

The `WardrobeManager` class is responsible for managing the user's collection of clothing items.

The wardrobe is stored as a list of `ClothingItem` objects.

The class currently supports:

- Adding clothing items
- Removing clothing items
- Viewing the wardrobe
- Searching by category
- Searching by occasion
- Showing the number of clothing items
- Saving the wardrobe
- Loading the wardrobe

---

## 6. Adding and Removing Clothing

The `add_clothing()` method creates a new `ClothingItem` and adds it to the wardrobe list.

The `remove_clothing()` method searches for an item by name and removes it from the wardrobe.

These operations were tested during Phase 1.

---

## 7. Searching the Wardrobe

MyCloset currently supports searching by category and occasion.

### Category Search

Users can search for clothing items belonging to a particular category.

### Occasion Search

Users can search for clothing items based on the occasion for which they are intended.

The searches are case-insensitive.

---

## 8. Item Count

The `show_item_count()` method counts the number of clothing items currently stored in the wardrobe.

It uses Python's built-in `len()` function to determine the number of items.

---

## 9. File Persistence

MyCloset uses a text file named `wardrobe.txt` to save wardrobe information.

Each clothing item is stored using the following format:

    name,category,occasion,color,season

For example:

    pants,pants,formal,re,summers
    dress,kjh,sf,ksjdhf,sjhf

The `save_wardrobe()` method writes the current wardrobe to the file.

The `load_wardrobe()` method reads the saved items from the file and recreates the corresponding `ClothingItem` objects.

This allows the wardrobe to persist after the program is closed.

---

## 10. Unit Testing

Unit tests were created for the `WardrobeManager`.

The tests verify important operations such as:

- Adding clothing
- Removing clothing
- Managing multiple items
- Checking wardrobe behavior

The tests were successfully executed using:

    python -m unittest discover tests

Successful testing confirmed that the core wardrobe management functionality was working as expected.

---

## 11. Flask Integration

Flask was introduced to create the web interface for MyCloset.

The Flask application is contained in:

    src/app.py

The application creates a `WardrobeManager`, loads the saved wardrobe, and passes the wardrobe data to the HTML template.

The main route is:

    /

This route renders the homepage.

---

## 12. HTML and Jinja Template

The webpage is located at:

    src/templates/index.html

The page uses Jinja templating to display the wardrobe dynamically.

The template checks whether the wardrobe contains any items.

If items exist, it loops through them and displays:

- Name
- Category
- Occasion
- Color
- Season

If there are no items, it displays a message indicating that the wardrobe is empty.

---

## 13. Backend-to-Frontend Data Flow

The current application follows this basic flow:

    wardrobe.txt
          ↓
    load_wardrobe()
          ↓
    WardrobeManager
          ↓
    Flask application
          ↓
    Jinja template
          ↓
    HTML webpage
          ↓
    Chrome

This successfully connects the Python backend with the web frontend.

---

## 14. Phase 1 Testing

The application was tested in a web browser.

Saved wardrobe entries were successfully loaded and displayed on the MyCloset webpage.

Example items displayed during testing included:

    pants

    Category: pants
    Occasion: formal
    Color: re
    Season: summers

and:

    dress

    Category: kjh
    Occasion: sf
    Color: ksjdhf
    Season: sjhf

This confirmed that the backend data was successfully being passed to the frontend and rendered by the Jinja template.

---

## 15. Git and GitHub

Git was used throughout the development of MyCloset to track changes.

The Flask integration and related changes were committed using the commit message:

    Connect wardrobe to Flask website

The commit was successfully pushed to GitHub.

The repository was verified afterward using:

    git status

The final output confirmed:

    nothing to commit, working tree clean

This confirmed that the local project and GitHub repository were synchronized.

---

## 16. Phase 1 Completion Status

Phase 1 is officially complete.

### Completed

- [x] ClothingItem model
- [x] WardrobeManager
- [x] Add clothing functionality
- [x] Remove clothing functionality
- [x] View wardrobe functionality
- [x] Search by category
- [x] Search by occasion
- [x] Item count
- [x] Save wardrobe
- [x] Load wardrobe
- [x] Unit testing
- [x] Flask application
- [x] HTML/Jinja template
- [x] Backend and frontend connection
- [x] Browser testing
- [x] Git version control
- [x] GitHub synchronization
- [x] Project documentation

---

## 17. Limitations at the End of Phase 1

Although the wardrobe can now be displayed through a web interface, the website is still basic.

Currently:

- Clothing cannot be added through the webpage.
- Clothing cannot be removed through the webpage.
- There are no interactive forms.
- There is no polished user interface.
- There is no filtering interface on the website.
- The application does not yet provide outfit recommendations.
- The application does not yet include advanced wardrobe features.

These features are intentionally left for future phases.

---

## Transition to Phase 2

Phase 2 will focus on making MyCloset interactive.

The first major goal will be allowing users to add clothing items directly through the website instead of manually editing `wardrobe.txt`.

This will introduce concepts such as:

- HTML forms
- Flask routes
- GET and POST requests
- Form data
- Connecting user input to Python
- Updating the wardrobe
- Saving new data

The project will gradually evolve from a basic backend with a display page into a functional digital wardrobe application.

---

# Phase 1: COMPLETE