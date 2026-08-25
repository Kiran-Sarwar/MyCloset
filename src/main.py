from wardrobe_manager import WardrobeManager

wardrobe_manager = WardrobeManager()

# Load saved wardrobe ONCE at program startup (outside the loop)
wardrobe_manager.load_wardrobe()

# Menu Interface Loop
while True:
    print("\n========== MyCloset ==========")
    print("1. Add clothing")
    print("2. View wardrobe")
    print("3. Search by category")
    print("4. Search by occasion")
    print("5. Remove clothing")
    print("6. Show item count")
    print("7. Save wardrobe")
    print("8. Exit")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        name = input("Enter clothing name: ")
        category = input("Enter category: ")
        occasion = input("Enter occasion: ")
        color = input("Enter color: ")
        season = input("Enter season: ")
        wardrobe_manager.add_clothing(name, category, occasion, color, season)

    elif choice == "2":
        wardrobe_manager.view_wardrobe()

    elif choice == "3":
        category = input("Enter category to search: ")
        wardrobe_manager.search_by_category(category)

    elif choice == "4":
        occasion = input("Enter occasion to search: ")
        wardrobe_manager.search_by_occasion(occasion)

    elif choice == "5":
        name = input("Enter clothing name to remove: ")
        wardrobe_manager.remove_clothing(name)

    elif choice == "6":
        wardrobe_manager.show_item_count()

    elif choice == "7":
        wardrobe_manager.save_wardrobe()

    elif choice == "8":
        print("Exiting MyCloset. Goodbye!")
        break

    else:
        print("Invalid option. Please try again.")