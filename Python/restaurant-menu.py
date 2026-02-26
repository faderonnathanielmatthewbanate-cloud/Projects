class MenuItem:
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category
    
    def __str__(self):
        return f"{self.name} - ${self.price:.2f}"


class RestaurantMenu:
    def __init__(self):
        self.items = {
            "Chicken": [
                MenuItem("Fried Chicken 1pc", 3.50, "Chicken"),
                MenuItem("Fried Chicken 2pc", 5.99, "Chicken"),
                MenuItem("Spicy Chicken Sandwich", 4.99, "Chicken"),
            ],
            "Burgers": [
                MenuItem("Classic Burger", 4.99, "Burgers"),
                MenuItem("Cheese Burger", 5.49, "Burgers"),
                MenuItem("Deluxe Burger", 6.99, "Burgers"),
            ],
            "Sides": [
                MenuItem("French Fries", 2.49, "Sides"),
                MenuItem("Coleslaw", 2.99, "Sides"),
                MenuItem("Rice", 1.99, "Sides"),
            ],
            "Beverages": [
                MenuItem("Soft Drink", 2.49, "Beverages"),
                MenuItem("Iced Tea", 2.49, "Beverages"),
                MenuItem("Coffee", 2.99, "Beverages"),
            ],
        }
        self.cart = []
    
    def display_menu(self):
        print("\n===== WELCOME TO JOY'S RESTAURANT =====\n")
        for category, items in self.items.items():
            print(f"\n{category.upper()}:")
            for idx, item in enumerate(items, 1):
                print(f"  {idx}. {item}")
    
    def add_to_cart(self, category, item_num):
        if category in self.items and 0 < item_num <= len(self.items[category]):
            item = self.items[category][item_num - 1]
            self.cart.append(item)
            print(f"✓ Added {item.name} to cart")
            return True
        print("✗ Invalid selection")
        return False
    
    def view_cart(self):
        if not self.cart:
            print("\nYour cart is empty")
            return
        print("\n===== YOUR CART =====")
        total = 0
        for idx, item in enumerate(self.cart, 1):
            print(f"{idx}. {item}")
            total += item.price
        print(f"\nTotal: ${total:.2f}")
    
    def checkout(self):
        if not self.cart:
            print("Cart is empty")
            return
        total = sum(item.price for item in self.cart)
        print(f"\n===== CHECKOUT =====")
        print(f"Total Amount: ${total:.2f}")
        print("Thank you for your order! Please proceed to payment.")
        self.cart = []
    
    def run(self):
        while True:
            self.display_menu()
            print("\n\nOptions: [1] Add Item [2] View Cart [3] Checkout [4] Exit")
            choice = input("Enter choice: ").strip()
            
            if choice == "1":
                category = input("Enter category (Chicken/Burgers/Sides/Beverages): ").strip()
                try:
                    item_num = int(input("Enter item number: "))
                    self.add_to_cart(category, item_num)
                except ValueError:
                    print("Invalid input")
            elif choice == "2":
                self.view_cart()
            elif choice == "3":
                self.checkout()
            elif choice == "4":
                print("Thank you for visiting! Goodbye!")
                break
            else:
                print("Invalid choice")


if __name__ == "__main__":
    restaurant = RestaurantMenu()
    restaurant.run()

