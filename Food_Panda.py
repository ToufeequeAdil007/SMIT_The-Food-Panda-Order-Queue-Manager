import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import random

class Order:
    """Order class to represent each order"""
    def __init__(self, order_id, items, is_vip=False):
        self.order_id = order_id
        self.items = items
        self.is_vip = is_vip
        self.timestamp = datetime.now()
    
    def __str__(self):
        vip_indicator = " ⭐" if self.is_vip else ""
        return f"Order #{self.order_id}{vip_indicator}: {self.items}"

class OrderQueueManager:
    """Manages the order queue with priority handling"""
    def __init__(self):
        self.queue = []
        self.next_order_id = 1001  # Starting order ID
    
    def add_order(self, items, is_vip=False):
        """Add an order to the queue with VIP priority"""
        order = Order(self.next_order_id, items, is_vip)
        self.next_order_id += 1
        
        if not is_vip:
            # Normal orders go to the end
            self.queue.append(order)
        else:
            # VIP orders go before all normal orders
            # Find the position after the last VIP order
            insert_index = 0
            for i, existing_order in enumerate(self.queue):
                if not existing_order.is_vip:
                    insert_index = i
                    break
                insert_index = i + 1
            self.queue.insert(insert_index, order)
        
        return order
    
    def process_next_order(self):
        """Process the order at the front of the queue"""
        if not self.queue:
            return None
        
        return self.queue.pop(0)
    
    def get_queue(self):
        """Return the current queue"""
        return self.queue.copy()
    
    def is_empty(self):
        """Check if queue is empty"""
        return len(self.queue) == 0
    
    def clear_queue(self):
        """Clear the entire queue"""
        self.queue.clear()

class FoodPandaGUI:
    """GUI for the Food Panda Order Queue Manager"""
    def __init__(self, root):
        self.root = root
        self.root.title("Food Panda Order Queue Manager")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f5f5f5")
        
        # Initialize queue manager
        self.queue_manager = OrderQueueManager()
        
        # Set up the GUI
        self.setup_styles()
        self.create_widgets()
        self.update_queue_display()
        
        # Start with process button disabled
        self.update_process_button_state()
        
        # Track VIP notifications to avoid repeated alerts
        self.last_vip_notified = None
    
    def setup_styles(self):
        """Configure styles for the GUI"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        self.bg_color = "#f5f5f5"
        self.primary_color = "#e74c3c"  # Food Panda red
        self.secondary_color = "#2c3e50"  # Dark blue
        self.vip_color = "#f39c12"  # Gold for VIP
        self.normal_color = "#3498db"  # Blue for normal
        self.success_color = "#2ecc71"  # Green for success
        
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg=self.primary_color)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            header_frame,
            text="🍔 Food Panda Order Queue Manager",
            font=("Helvetica", 24, "bold"),
            fg="white",
            bg=self.primary_color,
            pady=15
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Real-time Kitchen Order Processing System",
            font=("Helvetica", 12),
            fg="white",
            bg=self.primary_color,
            pady=5
        )
        subtitle_label.pack()
        
        # Create two main columns
        container = tk.Frame(main_frame, bg=self.bg_color)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Left column - Order Input
        left_frame = tk.Frame(container, bg=self.bg_color)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Right column - Queue Display
        right_frame = tk.Frame(container, bg=self.bg_color)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Order Input Section
        input_frame = tk.LabelFrame(
            left_frame,
            text="New Order Details",
            font=("Helvetica", 14, "bold"),
            bg=self.bg_color,
            fg=self.secondary_color,
            padx=20,
            pady=20
        )
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Order ID (auto-generated, display only)
        id_frame = tk.Frame(input_frame, bg=self.bg_color)
        id_frame.pack(fill=tk.X, pady=5)
        
        id_label = tk.Label(
            id_frame,
            text="Order ID:",
            font=("Helvetica", 12),
            bg=self.bg_color,
            fg=self.secondary_color,
            width=15,
            anchor=tk.W
        )
        id_label.pack(side=tk.LEFT)
        
        self.id_display = tk.Label(
            id_frame,
            text="1001",
            font=("Helvetica", 12, "bold"),
            bg=self.bg_color,
            fg=self.primary_color
        )
        self.id_display.pack(side=tk.LEFT)
        
        # Items input
        items_frame = tk.Frame(input_frame, bg=self.bg_color)
        items_frame.pack(fill=tk.X, pady=10)
        
        items_label = tk.Label(
            items_frame,
            text="Order Items:",
            font=("Helvetica", 12),
            bg=self.bg_color,
            fg=self.secondary_color,
            width=15,
            anchor=tk.W
        )
        items_label.pack(side=tk.LEFT)
        
        self.items_entry = tk.Text(
            items_frame,
            height=4,
            width=30,
            font=("Helvetica", 11),
            bg="white",
            relief=tk.SOLID,
            borderwidth=1
        )
        self.items_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Add some sample items as placeholder
        self.items_entry.insert("1.0", "e.g., Burger, Fries, Coke")
        self.items_entry.bind("<FocusIn>", self.clear_placeholder)
        
        # VIP selection
        vip_frame = tk.Frame(input_frame, bg=self.bg_color)
        vip_frame.pack(fill=tk.X, pady=10)
        
        self.is_vip = tk.BooleanVar()
        vip_check = tk.Checkbutton(
            vip_frame,
            text="VIP Order ⭐",
            variable=self.is_vip,
            font=("Helvetica", 12, "bold"),
            bg=self.bg_color,
            fg=self.vip_color,
            selectcolor=self.bg_color,
            activebackground=self.bg_color,
            command=self.on_vip_toggle
        )
        vip_check.pack(side=tk.LEFT)
        
        # Button frame
        button_frame = tk.Frame(input_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Add Order Button
        self.add_button = tk.Button(
            button_frame,
            text="Add Order to Queue",
            command=self.add_order,
            font=("Helvetica", 12, "bold"),
            bg=self.normal_color,
            fg="white",
            activebackground=self.normal_color,
            activeforeground="white",
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        self.add_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear Button
        clear_button = tk.Button(
            button_frame,
            text="Clear Form",
            command=self.clear_form,
            font=("Helvetica", 12),
            bg="#95a5a6",
            fg="white",
            activebackground="#7f8c8d",
            activeforeground="white",
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        clear_button.pack(side=tk.LEFT)
        
        # Statistics Section
        stats_frame = tk.LabelFrame(
            left_frame,
            text="Queue Statistics",
            font=("Helvetica", 14, "bold"),
            bg=self.bg_color,
            fg=self.secondary_color,
            padx=20,
            pady=15
        )
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Stats labels
        self.total_orders_label = tk.Label(
            stats_frame,
            text="Total Orders in Queue: 0",
            font=("Helvetica", 12),
            bg=self.bg_color,
            fg=self.secondary_color
        )
        self.total_orders_label.pack(anchor=tk.W, pady=5)
        
        self.vip_orders_label = tk.Label(
            stats_frame,
            text="VIP Orders: 0",
            font=("Helvetica", 12),
            bg=self.bg_color,
            fg=self.vip_color
        )
        self.vip_orders_label.pack(anchor=tk.W, pady=5)
        
        self.normal_orders_label = tk.Label(
            stats_frame,
            text="Normal Orders: 0",
            font=("Helvetica", 12),
            bg=self.bg_color,
            fg=self.normal_color
        )
        self.normal_orders_label.pack(anchor=tk.W, pady=5)
        
        # Quick Add Sample Orders Section
        sample_frame = tk.LabelFrame(
            left_frame,
            text="Quick Add Sample Orders",
            font=("Helvetica", 14, "bold"),
            bg=self.bg_color,
            fg=self.secondary_color,
            padx=20,
            pady=15
        )
        sample_frame.pack(fill=tk.X)
        
        sample_button_frame = tk.Frame(sample_frame, bg=self.bg_color)
        sample_button_frame.pack(fill=tk.X)
        
        # Sample order buttons
        sample_orders = [
            ("Add Normal Order", False, self.normal_color),
            ("Add VIP Order", True, self.vip_color)
        ]
        
        for text, is_vip, color in sample_orders:
            btn = tk.Button(
                sample_button_frame,
                text=text,
                command=lambda v=is_vip: self.add_sample_order(v),
                font=("Helvetica", 11),
                bg=color,
                fg="white",
                activebackground=color,
                activeforeground="white",
                relief=tk.FLAT,
                padx=15,
                pady=8
            )
            btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Queue Display Section
        queue_display_frame = tk.LabelFrame(
            right_frame,
            text="Order Queue",
            font=("Helvetica", 14, "bold"),
            bg=self.bg_color,
            fg=self.secondary_color,
            padx=20,
            pady=20
        )
        queue_display_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create a treeview for the queue display
        columns = ("order_id", "items", "priority", "timestamp")
        self.queue_tree = ttk.Treeview(
            queue_display_frame,
            columns=columns,
            show="headings",
            height=15,
            selectmode="browse"
        )
        
        # Define headings
        self.queue_tree.heading("order_id", text="Order ID")
        self.queue_tree.heading("items", text="Items")
        self.queue_tree.heading("priority", text="Priority")
        self.queue_tree.heading("timestamp", text="Time Added")
        
        # Define columns
        self.queue_tree.column("order_id", width=100, anchor=tk.CENTER)
        self.queue_tree.column("items", width=250, anchor=tk.W)
        self.queue_tree.column("priority", width=100, anchor=tk.CENTER)
        self.queue_tree.column("timestamp", width=150, anchor=tk.CENTER)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            queue_display_frame,
            orient=tk.VERTICAL,
            command=self.queue_tree.yview
        )
        self.queue_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.queue_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure tags for VIP and normal orders
        self.queue_tree.tag_configure("vip", background="#fff9e6", foreground=self.vip_color)
        self.queue_tree.tag_configure("normal", background="white", foreground=self.normal_color)
        
        # Process Order Section
        process_frame = tk.Frame(right_frame, bg=self.bg_color)
        process_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Process Next Order Button
        self.process_button = tk.Button(
            process_frame,
            text="Process Next Order",
            command=self.process_next_order,
            font=("Helvetica", 14, "bold"),
            bg=self.success_color,
            fg="white",
            activebackground=self.success_color,
            activeforeground="white",
            relief=tk.FLAT,
            padx=30,
            pady=12,
            state=tk.DISABLED
        )
        self.process_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear Queue Button
        clear_queue_button = tk.Button(
            process_frame,
            text="Clear All Orders",
            command=self.clear_all_orders,
            font=("Helvetica", 12),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            activeforeground="white",
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        clear_queue_button.pack(side=tk.LEFT)
        
        # Status Bar
        self.status_bar = tk.Label(
            main_frame,
            text="Ready to accept orders",
            font=("Helvetica", 10),
            bg=self.secondary_color,
            fg="white",
            anchor=tk.W,
            padx=10,
            pady=5
        )
        self.status_bar.pack(fill=tk.X, pady=(20, 0))
    
    def on_vip_toggle(self):
        """Update button color when VIP toggle changes"""
        if self.is_vip.get():
            self.add_button.config(bg=self.vip_color)
        else:
            self.add_button.config(bg=self.normal_color)
    
    def clear_placeholder(self, event):
        """Clear the placeholder text when entry is focused"""
        if self.items_entry.get("1.0", "end-1c") == "e.g., Burger, Fries, Coke":
            self.items_entry.delete("1.0", tk.END)
    
    def add_order(self):
        """Add a new order to the queue"""
        # Get items from text widget
        items = self.items_entry.get("1.0", "end-1c").strip()
        
        # Validate input
        if not items or items == "e.g., Burger, Fries, Coke":
            messagebox.showwarning("Input Error", "Please enter order items.")
            return
        
        # Add order to queue
        is_vip = self.is_vip.get()
        order = self.queue_manager.add_order(items, is_vip)
        
        # Update display
        self.update_queue_display()
        self.update_process_button_state()
        self.update_statistics()
        
        # Update status
        self.status_bar.config(
            text=f"Order #{order.order_id} added to queue. {'⭐ VIP priority!' if is_vip else ''}"
        )
        
        # Show VIP notification
        if is_vip and order.order_id != self.last_vip_notified:
            messagebox.showinfo("VIP Order Added", 
                              f"VIP Order #{order.order_id} has been added to the front of the queue!")
            self.last_vip_notified = order.order_id
        
        # Reset form
        self.clear_form()
        
        # Update next order ID display
        self.id_display.config(text=str(self.queue_manager.next_order_id))
    
    def add_sample_order(self, is_vip):
        """Add a sample order for testing"""
        # Sample food items
        sample_items = [
            "Cheeseburger, French Fries, Coke",
            "Pepperoni Pizza, Garlic Bread, Sprite",
            "Chicken Biryani, Raita, Salad",
            "Vegetable Spring Rolls, Fried Rice, Tea",
            "Caesar Salad, Garlic Bread, Iced Tea",
            "Grilled Salmon, Mashed Potatoes, Lemonade",
            "Veggie Burger, Sweet Potato Fries, Milkshake",
            "Spaghetti Carbonara, Garlic Bread, Red Wine"
        ]
        
        # Randomly select items
        items = random.choice(sample_items)
        
        # Set items in the text widget
        self.items_entry.delete("1.0", tk.END)
        self.items_entry.insert("1.0", items)
        
        # Set VIP status
        self.is_vip.set(is_vip)
        self.on_vip_toggle()
        
        # Add the order
        self.add_order()
    
    def process_next_order(self):
        """Process the next order in the queue"""
        if self.queue_manager.is_empty():
            messagebox.showinfo("Queue Empty", "No orders to process.")
            return
        
        # Get the next order
        order = self.queue_manager.process_next_order()
        
        # Update display
        self.update_queue_display()
        self.update_process_button_state()
        self.update_statistics()
        
        # Show processing message
        vip_indicator = "⭐ VIP " if order.is_vip else ""
        messagebox.showinfo(
            "Order Processed", 
            f"{vip_indicator}Order #{order.order_id} processed:\n\n{order.items}"
        )
        
        # Update status
        self.status_bar.config(
            text=f"Order #{order.order_id} processed. {vip_indicator}Ready for next order."
        )
    
    def clear_form(self):
        """Clear the input form"""
        self.items_entry.delete("1.0", tk.END)
        self.items_entry.insert("1.0", "e.g., Burger, Fries, Coke")
        self.is_vip.set(False)
        self.on_vip_toggle()
    
    def clear_all_orders(self):
        """Clear all orders from the queue"""
        if self.queue_manager.is_empty():
            messagebox.showinfo("Queue Empty", "Order queue is already empty.")
            return
        
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all orders from the queue?"):
            self.queue_manager.clear_queue()
            self.update_queue_display()
            self.update_process_button_state()
            self.update_statistics()
            self.status_bar.config(text="All orders cleared from queue.")
    
    def update_queue_display(self):
        """Update the queue display treeview"""
        # Clear current display
        for item in self.queue_tree.get_children():
            self.queue_tree.delete(item)
        
        # Add orders to display
        for order in self.queue_manager.get_queue():
            # Format timestamp
            time_str = order.timestamp.strftime("%H:%M:%S")
            
            # Insert into tree with appropriate tag
            tag = "vip" if order.is_vip else "normal"
            priority = "⭐ VIP" if order.is_vip else "Normal"
            
            self.queue_tree.insert(
                "", tk.END,
                values=(order.order_id, order.items, priority, time_str),
                tags=(tag,)
            )
    
    def update_process_button_state(self):
        """Enable or disable the process button based on queue state"""
        if self.queue_manager.is_empty():
            self.process_button.config(state=tk.DISABLED)
        else:
            self.process_button.config(state=tk.NORMAL)
    
    def update_statistics(self):
        """Update queue statistics"""
        queue = self.queue_manager.get_queue()
        total = len(queue)
        vip_count = sum(1 for order in queue if order.is_vip)
        normal_count = total - vip_count
        
        self.total_orders_label.config(text=f"Total Orders in Queue: {total}")
        self.vip_orders_label.config(text=f"VIP Orders: {vip_count}")
        self.normal_orders_label.config(text=f"Normal Orders: {normal_count}")

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = FoodPandaGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()