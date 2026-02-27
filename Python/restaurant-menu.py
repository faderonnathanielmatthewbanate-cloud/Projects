def Jolly_bae_menu():
    print("\n" + "-" * 50)
    print("              Value Meals            ")
    print("-" * 50)
    print("\n" + "-" * 50)
    print("Menu:")
    print("-" * 50)
    print("1. Regular Meals")
    print("2. Combo Meals")
    print("3. Family Meals")
    print("4. Party Meals")
    print("5. Jolli-Saver Meals")
    print("6. Return To Role Selection")
    print("-" * 50)
    print("Enter your choice (1-6): ", end="")


def jolly_bae_menu():
    # The 'Master Container' - A Nested Dictionary
    menu = {
        "1": {
            "category": "Regular Meals",
            "items": {
                "1": ("1pc Chickenjoy w/ Rice", 95), "2": ("2pc Chickenjoy w/ Rice", 180),
                "3": ("1pc Spicy Chickenjoy", 100), "4": ("1pc Burger Steak", 60),
                "5": ("2pc Burger Steak", 115), "6": ("Jolly Spaghetti Solo", 60),
                "7": ("Palabok Fiesta Solo", 120), "8": ("Yumburger Solo", 40),
                "9": ("Cheesy Yumburger", 65), "10": ("Tuna Pie (2pcs)", 90)
            }
        },
        "2": {
            "category": "Combo Meals",
            "items": {
                "1": ("C1: Chickenjoy + Drink", 115), "2": ("C2: 2pc Chickenjoy + Drink", 200),
                "3": ("C3: Chickenjoy + Spag + Drink", 160), "4": ("C4: Chickenjoy + Palabok + Drink", 210),
                "5": ("J1: Burger Steak + Spag + Drink", 130), "6": ("S1: Spag + Yumburger + Drink", 110),
                "7": ("S2: Spag + Fries + Drink", 105), "8": ("B1: Yumburger + Fries + Drink", 95),
                "9": ("B2: Cheesy Yum + Fries + Drink", 120), "10": ("B3: Aloha Yum + Fries + Drink", 185)
            }
        },
        "3": {
            "category": "Family Meals",
            "items": {
                "1": ("6pc Chickenjoy Bucket", 450), "2": ("8pc Chickenjoy Bucket", 590),
                "3": ("6pc Spicy Bucket", 480), "4": ("Family Pan Spaghetti", 250),
                "5": ("Family Pan Palabok", 400), "6": ("Chicken + Spag Family Meal", 550),
                "7": ("Burger Steak Family Pan", 320), "8": ("Bucket of Fries", 150),
                "9": ("Peach Mango Pie 3-Pack", 130), "10": ("Tuna Pie 3-Pack", 135)
            }
        },
        "4": {
            "category": "Party Meals",
            "items": {
                "1": ("Party Bundle A (12pc+2 Spag)", 1200), "2": ("Party Bundle B (18pc+20 Yum)", 2500),
                "3": ("12pc Chickenjoy Bucket", 850), "4": ("15pc Chickenjoy Bucket", 1050),
                "5": ("Jolly Spaghetti Party Size", 650), "6": ("Palabok Fiesta Party Size", 850),
                "7": ("Burger Steak Party Tray (20pc)", 950), "8": ("Pie Party Pack (12pcs)", 500),
                "9": ("Sundae Party Set (10 cups)", 450), "10": ("Mixed Bucket (6 Reg/6 Spicy)", 880)
            }
        },
        "5": {
            "category": "Jolli-Saver Meals",
            "items": {
                "1": ("Budget Yumburger", 35), "2": ("Jr. Burger Steak", 55),
                "3": ("Jr. Jolly Spaghetti", 50), "4": ("Fries & Coke Float", 75),
                "5": ("Yumburger & Pineapple Juice", 70), "6": ("Jolli-Hotdog", 60),
                "7": ("Tuna Pie & Coffee", 80), "8": ("Steak & Peach Mango Pie", 99),
                "9": ("Rice & Extra Gravy Bowl", 30), "10": ("Iced Barako & Yumburger", 85)
            }
        }
    }

    print("--- WELCOME TO JOLLY-BAE ---")
    print("1. Regular Meals\n2. Combo Meals\n3. Family Meals\n4. Party Meals\n5. Jolli-Saver Meals")
    
    cat_choice = input("\nSelect a category (1-5): ")

    if cat_choice in menu:
        selected_cat = menu[cat_choice]
        print(f"\n--- {selected_cat['category']} ---")
        
        # Iterating through the items in the chosen category
        for code, details in selected_cat['items'].items():
            name, price = details
            print(f"[{code}] {name.ljust(30)} ₱{price}")
            
        item_choice = input("\nSelect item number to order: ")
        
        if item_choice in selected_cat['items']:
            item_name, item_price = selected_cat['items'][item_choice]
            print(f"\nAdded {item_name} to cart. Total: ₱{item_price}")
        else:
            print("Invalid item choice.")
    else:
        print("Invalid category.")



def display_role_menu():
    print("\n")
    print("              Select Your Role              ")
    print("-" * 50)
    print("1. Customer")
    print("2. Admin Staff")
    print("3. Exit")
    print("-" * 50)
    print("Enter your choice (1-3): ", end="")


def main():
    print("\n" + "-" * 51)
    print("             Welcome to Jolli-Bae            ")
    print("-" * 51)


    # Role selection menu
    while True:
        display_role_menu()
        
        while True:
            try:
                role_choice = int(input())
                if 1 <= role_choice <= 3:
                    break
                else:
                    print("Invalid input. Please enter a number between 1 and 3: ", end="")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 3: ", end="")

        if role_choice == 2:
            print("\n--- Admin Staff Menu ---")
            print("Admin Staff access granted.")
            print("Cuyson na bahala.")
            continue

        if role_choice == 3:
            print("\nThank you for using the system. Goodbye!")
            return

        # Continue to main menu for Customer only
        running = True
        while running:
            jolly_bae_menu()

            while True:
                try:
                    choice = int(input())
                    if 1 <= choice <= 6:
                        break
                    else:
                        print("Invalid input. Please enter a number between 1 and 6: ", end="")
                except ValueError:
                    print("Invalid input. Please enter a number between 1 and 6: ", end="")

            if 1 <= choice <= 5:
                jolly_bae_menu()
                menu_return_choice = input("\nDo you want to **[R]**eturn to Homepage or **[E]**end the program? (R/E): ")

                if menu_return_choice.upper() == 'E':
                    print("\nThank you for using the system. Goodbye!")
                    running = False
                elif menu_return_choice.upper() == 'R':
                    running = True  # Return to main menu

            elif choice == 6:
                running = False
