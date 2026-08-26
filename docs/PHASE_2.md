# MyCloset — Phase 2

## Flask Web Application

Phase 2 transformed MyCloset from a Python-based wardrobe manager into a functional web application using Flask.

---

## Phase 2 Goals

The main goals of Phase 2 were:

- Build a web interface for MyCloset
- Connect the Python backend to the frontend
- Allow users to add clothing items
- Allow users to remove clothing items
- Store wardrobe data persistently
- Search and filter wardrobe items
- Create a clean and responsive interface
- Introduce a structured clothing category system

---

## Technologies Used

- Python
- Flask
- HTML
- Jinja2
- CSS
- JavaScript
- Git
- GitHub

---

## Features Implemented

### 1. Wardrobe Dashboard

The homepage displays:

- Total number of wardrobe items
- Number of Tops
- Number of Bottoms

---

### 2. Add Clothing Items

Users can add clothing items through a web form.

Each item contains:

- Name
- Category
- Type
- Occasion
- Color
- Season

---

### 3. Dynamic Category and Type

The Type dropdown changes depending on the selected Category.

For example:

**Tops**

- T-Shirt
- Shirt
- Blouse
- Sweater
- Hoodie

**Bottoms**

- Jeans
- Trousers
- Shorts
- Skirt

**One-Piece**

- Dress
- Jumpsuit

**Outerwear**

- Jacket
- Coat
- Blazer

**Shoes**

- Sneakers
- Boots
- Sandals
- Formal Shoes

**Accessories**

- Bag
- Scarf
- Hat
- Belt
- Jewelry

---

### 4. Remove Clothing Items

Users can remove clothing items directly from the wardrobe.

The change is also saved to the wardrobe file.

---

### 5. Persistent Storage

Wardrobe data is stored in:

`src/wardrobe.txt`

The application:

- Saves new items
- Saves removed items
- Loads existing items when Flask starts

Therefore, wardrobe data remains available after restarting the application.

---

## Filtering System

MyCloset supports filtering using:

- Category
- Type
- Occasion
- Color
- Season

Multiple filters can be combined.

For example:

```text
Category: Tops
Type: T-Shirt
Occasion: Casual
Color: Black
Season: Summer