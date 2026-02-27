def display_main_menu():
    print("\n" + "-" * 50)
    print("                  Value Meals            ")
    print("-" * 50)
    print("Menu:")
    print("-" * 50)
    print("1. Regular Meals")
    print("2. Combo Meals")
    print("3. Family Meals")
    print("4. Party Meals")
    print("5. Jolli-Saver Meals")
    print("6. View Cart")
    print("7. Return To Role Selection")
    print("-" * 50)
    print("Enter your choice (1-7): ", end="")


def display_data(option):
    data_entries = []
    if option == 1:
        data_entries = [
            "1. 1pc Chickenjoy w/ Rice - ₱95",
            "2. 2pc Chickenjoy w/ Rice - ₱180",
            "3. 1pc Spicy Chickenjoy - ₱100",
            "4. 1pc Burger Steak - ₱60",
            "5. 2pc Burger Steak - ₱115",
            "6. Jolly Spaghetti Solo - ₱60",
            "7. Palabok Fiesta Solo - ₱120",
            "8. Yumburger Solo - ₱40",
            "9. Cheesy Yumburger - ₱65",
            "10. Tuna Pie (2pcs) - ₱90"
        ]
        category = "Regular Meals"
    elif option == 2:
        data_entries = [
            "1. C1: Chickenjoy + Drink - ₱115",
            "2. C2: 2pc Chickenjoy + Drink - ₱200",
            "3. C3: Chickenjoy + Spag + Drink - ₱160",
            "4. C4: Chickenjoy + Palabok + Drink - ₱210",
            "5. J1: Burger Steak + Spag + Drink - ₱130",
            "6. S1: Spag + Yumburger + Drink - ₱110",
            "7. S2: Spag + Fries + Drink - ₱105",
            "8. B1: Yumburger + Fries + Drink - ₱95",
            "9. B2: Cheesy Yum + Fries + Drink - ₱120",
            "10. B3: Aloha Yum + Fries + Drink - ₱185"
        ]
        category = "Combo Meals"
    elif option == 3:
        data_entries = [
            "1. 6pc Chickenjoy Bucket - ₱450",
            "2. 8pc Chickenjoy Bucket - ₱590",
            "3. 6pc Spicy Bucket - ₱480",
            "4. Family Pan Spaghetti - ₱250",
            "5. Family Pan Palabok - ₱400",
            "6. Chicken + Spag Family Meal - ₱550",
            "7. Burger Steak Family Pan - ₱320",
            "8. Bucket of Fries - ₱150",
            "9. Peach Mango Pie 3-Pack - ₱130",
            "10. Tuna Pie 3-Pack - ₱135"
        ]
        category = "Family Meals"
    elif option == 4:
        data_entries = [
            "1. Party Bundle A (12pc+2 Spag) - ₱1200",
            "2. Party Bundle B (18pc+20 Yum) - ₱2500",
            "3. 12pc Chickenjoy Bucket - ₱850",
            "4. 15pc Chickenjoy Bucket - ₱1050",
            "5. Jolly Spaghetti Party Size - ₱650",
            "6. Palabok Fiesta Party Size - ₱850",
            "7. Burger Steak Party Tray (20pc) - ₱950",
            "8. Pie Party Pack (12pcs) - ₱500",
            "9. Sundae Party Set (10 cups) - ₱450",
            "10. Mixed Bucket (6 Reg/6 Spicy) - ₱880"
        ]
        category = "Party Meals"
    elif option == 5:
        data_entries = [
            "1. Budget Yumburger - ₱35",
            "2. Jr. Burger Steak - ₱55",
            "3. Jr. Jolly Spaghetti - ₱50",
            "4. Fries & Coke Float - ₱75",
            "5. Yumburger & Pineapple Juice - ₱70",
            "6. Jolli-Hotdog - ₱60",
            "7. Tuna Pie & Coffee - ₱80",
            "8. Steak & Peach Mango Pie - ₱99",
            "9. Rice & Extra Gravy Bowl - ₱30",
            "10. Iced Barako & Yumburger - ₱85"
        ]
        category = "Jolli-Saver Meals"

    print(f"\n--- {category} ---")
    for entry in data_entries:
        print(entry)
    print("-" * 50)
    return data_entries, category


def add_to_cart(cart, item_name, price, quantity):
    """Add item to cart"""
    for item in cart:
        if item["name"] == item_name:
            item["quantity"] += quantity
            return
    cart.append({"name": item_name, "price": price, "quantity": quantity})


def checkout(cart):
    """Handle checkout process"""
    if not cart:
        print("\nYour cart is empty. Nothing to checkout.")
        return

    total = sum(item["price"] * item["quantity"] for item in cart)

    print("\n" + "-" * 60)
    print("                    JOLLI-BAE RESTAURANT              ")
    print("                   Contact: (02) 8123-4567            ")
    print("                  Email: jolli-bae@email.com          ")
    print("-" * 60)
    print("                      ORDER RECEIPT                   ")
    print("-" * 60)

    for idx, item in enumerate(cart, 1):
        subtotal = item["price"] * item["quantity"]
        print(f"{idx}. {item['name']}")
        print(f"   ₱{item['price']} × {item['quantity']} = ₱{subtotal}")

    print("-" * 60)
    print(f"TOTAL AMOUNT DUE: ₱{total}")
    print("-" * 60)
    print("\n        Thank you for your order at Jolli-Bae!        ")
    print("              We appreciate your business!            ")
    print("           Visit us again soon. Enjoy your meal!      ")
    print("-" * 60 + "\n")

    cart.clear()


def display_cart(cart):
    """Display cart contents"""
    if not cart:
        print("\nYour cart is empty.")
        return "main"

    print("\n" + "-" * 60)
    print("                      SHOPPING CART                  ")
    print("-" * 60)
    total = 0
    for idx, item in enumerate(cart, 1):
        subtotal = item["price"] * item["quantity"]
        total += subtotal
        print(f"{idx}. {item['name']}")
        print(f"   Price: ₱{item['price']} × {item['quantity']} = ₱{subtotal}")
    print("-" * 60)
    print(f"TOTAL: ₱{total}")
    print("-" * 60)

    while True:
        print("\n1. Remove item")
        print("2. Modify quantity")
        print("3. Checkout")
        print("4. Back to menu")
        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            try:
                item_num = int(input("Enter item number to remove: "))
                if 1 <= item_num <= len(cart):
                    removed = cart.pop(item_num - 1)
                    print(f"Removed {removed['name']} from cart.")
                    return "main"
                else:
                    print("Invalid item number.")
            except ValueError:
                print("Invalid input.")

        elif choice == "2":
            try:
                item_num = int(input("Enter item number to modify: "))
                if 1 <= item_num <= len(cart):
                    new_qty = int(input("Enter new quantity: "))
                    if new_qty > 0:
                        cart[item_num - 1]["quantity"] = new_qty
                        print("Quantity updated.")
                        return "main"
                    else:
                        print("Quantity must be positive.")
                else:
                    print("Invalid item number.")
            except ValueError:
                print("Invalid input.")

        elif choice == "3":
            checkout(cart)
            # Post-checkout navigation prompt
            print("-" * 50)
            print("         Where would you like to go next?         ")
            print("-" * 50)
            print("1. Return to Main Menu")
            print("2. Return to Role Selection")
            print("3. Exit")
            print("-" * 50)
            while True:
                post_choice = input("Enter your choice (1-3): ")
                if post_choice == "1":
                    return "main"
                elif post_choice == "2":
                    return "role"
                elif post_choice == "3":
                    return "exit"
                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")

        elif choice == "4":
            return "main"

        else:
            print("Invalid choice.")


def display_role_menu():
    print("\n")
    print("              Select Your Role              ")
    print("-" * 50)
    print("1. Customer")
    print("2. Admin Staff")
    print("3. Exit")
    print("-" * 50)
    print("Enter your choice (1-3): ", end="")


def customer_menu():
    """Handle customer menu selection"""
    cart = []

    while True:
        display_main_menu()

        while True:
            try:
                choice = int(input())
                if 1 <= choice <= 7:
                    break
                else:
                    print("Invalid input. Please enter a number between 1 and 7: ", end="")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 7: ", end="")

        if 1 <= choice <= 5:
            data_entries, category = display_data(choice)

            while True:
                item_choice = input("\nEnter item number to add (or 0 to go back): ")
                try:
                    item_num = int(item_choice)
                    if item_num == 0:
                        break
                    if 1 <= item_num <= len(data_entries):
                        quantity = int(input("Enter quantity: "))
                        if quantity > 0:
                            item_line = data_entries[item_num - 1]
                            item_name = item_line.rsplit(" - ₱", 1)[0]   # ← updated
                            price = int(item_line.rsplit(" - ₱", 1)[1])  # ← updated
                            add_to_cart(cart, item_name, price, quantity)
                            print(f"Added {quantity}x {item_name} to cart!")
                        else:
                            print("Quantity must be positive.")
                    else:
                        print("Invalid item number.")
                except ValueError:
                    print("Invalid input.")

        elif choice == 6:
            nav = display_cart(cart)
            if nav == "role":
                return "role"
            elif nav == "exit":
                return "exit"

        elif choice == 7:
            return "role"


def main():
    print("\n" + "-" * 51)
    print("             Welcome to Jolli-Bae            ")
    print("-" * 51)

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

        if role_choice == 1:
            nav = customer_menu()
            if nav == "exit":
                print("\nThank you for using the system. Goodbye!")
                break

        elif role_choice == 2:
            print("\n--- Admin Staff Menu ---")
            print("Admin Staff access granted.")
            print("Cuyson na bahala.")
            continue

        elif role_choice == 3:
            print("\nThank you for using the system. Goodbye!")
            break


if __name__ == "__main__":
    main()