import tkinter as tk
from tkinter import messagebox

class MenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Menu Application")
        
        # Order dictionary to track items and their quantities globally
        self.current_order = {}

        # Frame for the navigation menu
        self.nav_frame = tk.Frame(root)
        self.nav_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Navigation buttons
        self.veg_button = tk.Button(self.nav_frame, text="Veg", command=self.show_veg_page)
        self.veg_button.pack(side=tk.LEFT, padx=5)
        
        self.non_veg_button = tk.Button(self.nav_frame, text="Non-Veg", command=self.show_non_veg_page)
        self.non_veg_button.pack(side=tk.LEFT, padx=5)
        
        self.dessert_button = tk.Button(self.nav_frame, text="Desserts", command=self.show_desserts_page)
        self.dessert_button.pack(side=tk.LEFT, padx=5)
        
        # Frame for pages
        self.page_frame = tk.Frame(root)
        self.page_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=5)
        
        # Footer section with order summary
        self.footer_frame = tk.Frame(root, height=100, bg="lightgray")
        self.footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.add_button = tk.Button(self.footer_frame, text="Add to Order", command=self.update_order_display)
        self.add_button.pack(side=tk.TOP, pady=5)
        
        self.place_order_button = tk.Button(self.footer_frame, text="Place Order", command=self.place_order)
        self.place_order_button.pack(side=tk.TOP, pady=5)
        
        self.order_label = tk.Label(self.footer_frame, text="Current Order: ")
        self.order_label.pack(side=tk.TOP, anchor=tk.W, pady=5)
        
        self.order_list_label = tk.Label(self.footer_frame, text="", anchor=tk.W, wraplength=400)
        self.order_list_label.pack(side=tk.TOP, fill=tk.X)
        
        self.total_label = tk.Label(self.footer_frame, text="Total: $0.00", anchor=tk.W)
        self.total_label.pack(side=tk.TOP, fill=tk.X)
        
        # Display the Veg page by default
        self.show_veg_page()

    def clear_page(self):
        """Clears the content of the page_frame"""
        for widget in self.page_frame.winfo_children():
            widget.destroy()

    def show_veg_page(self):
        """Displays the Veg menu"""
        self.clear_page()
        self.create_page("Veg", [
            ("Starters", [("Paneer Tikka", 5), ("Veg Pakora", 4), ("Samosa", 2)]),
            ("Chinese", [("Veg Noodles", 7), ("Manchurian", 6), ("Spring Rolls", 3)]),
        ])
    
    def show_non_veg_page(self):
        """Displays the Non-Veg menu"""
        self.clear_page()
        self.create_page("Non-Veg", [
            ("Starters", [("Chicken Wings", 8), ("Fish Fry", 7), ("Seekh Kebab", 9)]),
            ("Main Dishes", [("Chicken Curry", 12), ("Mutton Biryani", 15), ("Grilled Fish", 14)]),
        ])
    
    def show_desserts_page(self):
        """Displays the Desserts menu"""
        self.clear_page()
        self.create_page("Desserts", [
            ("Desserts", [("Chocolate Cake", 7), ("Ice Cream", 5), ("Pudding", 4)]),
        ])
    
    def create_page(self, title, categories):
        """Creates a page based on categories and items"""
        title_label = tk.Label(self.page_frame, text=title, font=("Arial", 20))
        title_label.pack(side=tk.TOP, pady=5)
        
        for category, items in categories:
            category_frame = tk.LabelFrame(self.page_frame, text=category, padx=5, pady=5)
            category_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            
            for item_name, price in items:
                item_frame = tk.Frame(category_frame)
                item_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
                
                item_label = tk.Label(item_frame, text=item_name, width=25, anchor=tk.W)
                item_label.pack(side=tk.LEFT)
                
                price_label = tk.Label(item_frame, text=f"${price}", width=8, anchor=tk.W)
                price_label.pack(side=tk.LEFT)
                
                qty_var = tk.IntVar(value=0)
                qty_label = tk.Label(item_frame, text="Qty: ")
                qty_label.pack(side=tk.LEFT)
                
                minus_button = tk.Button(item_frame, text="-", command=lambda qty_var=qty_var, name=item_name, price=price: self.update_qty(qty_var, name, price, -1))
                minus_button.pack(side=tk.LEFT)
                
                qty_entry = tk.Entry(item_frame, textvariable=qty_var, width=5)
                qty_entry.pack(side=tk.LEFT)
                
                plus_button = tk.Button(item_frame, text="+", command=lambda qty_var=qty_var, name=item_name, price=price: self.update_qty(qty_var, name, price, 1))
                plus_button.pack(side=tk.LEFT)

    def update_qty(self, qty_var, name, price, change):
        """Updates the quantity of an item and modifies the order"""
        new_qty = qty_var.get() + change
        if new_qty >= 0:
            qty_var.set(new_qty)
            if new_qty > 0:
                self.current_order[name] = (price, new_qty)
            else:
                self.current_order.pop(name, None)

    def update_order_display(self):
        """Updates the display of the current order"""
        order_list = []
        total_price = 0
        for name, (price, qty) in self.current_order.items():
            total_cost = qty * price
            order_list.append(f"{qty}x {name} @ ${price} = ${total_cost}")
            total_price += total_cost

        self.order_list_label.config(text="\n".join(order_list))
        self.total_label.config(text=f"Total: ${total_price:.2f}")

    def place_order(self):
        """Displays the final order details and a thank-you message"""
        if not self.current_order:
            tk.messagebox.showinfo("Order", "Your order is empty! Please add items to your order.")
            return

        order_details = []
        total_price = 0
        for name, (price, qty) in self.current_order.items():
            total_cost = qty * price
            order_details.append(f"{qty}x {name} @ ${price} = ${total_cost}")
            total_price += total_cost

        order_summary = "\n".join(order_details)
        message = f"Your Order:\n\n{order_summary}\n\nTotal: ${total_price:.2f}\n\nThank you. Order placed. Go back to menu to update order."
        tk.messagebox.showinfo("Order Placed", message)

if __name__ == "__main__":
    root = tk.Tk()
    app = MenuApp(root)
    root.mainloop()
