import requests
import pandas as pd
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import os


spoonacular_api_key = 'your_spoonacular_api_key'
history_file = 'searched_products.csv'

def load_search_history():
    if os.path.exists(history_file):
        with open(history_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            return set(row[0] for row in reader)
    return set()

def save_search_history(product_name):
    with open(history_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([product_name])

def search_product(product_name):
    base_url = f"https://api.spoonacular.com/food/products/search"
    params = {
        'query': product_name,
        'apiKey': spoonacular_api_key
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def analyze_ingredients(ingredients):
    base_url = f"https://api.spoonacular.com/food/ingredients/search"
    params = {
        'query': ingredients,
        'apiKey': spoonacular_api_key
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def format_product_details(product_data):
    if product_data and 'products' in product_data:
        products = product_data['products']
        details = []
        for product in products:
            details.append(f"Product Name: {product.get('name', 'Not Available')}")
            details.append(f"Brand: {product.get('brand', 'Not Available')}")
            details.append(f"Description: {product.get('description', 'Not Available')}")
            details.append(f"Price: {product.get('price', 'Not Available')}")
            details.append(f"Image URL: {product.get('imageUrl', 'Not Available')}")
            details.append('-' * 50)
        return '\n'.join(details)
    else:
        return "Product not found or no data available."

class ProductSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Product Search and Dietary Analysis")
        self.searched_products = load_search_history()

        self.create_widgets()

    def create_widgets(self):
        self.tab_control = ttk.Notebook(self.root)

        self.search_tab = ttk.Frame(self.tab_control)
        self.results_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.search_tab, text='Search Product')
        self.tab_control.add(self.results_tab, text='Results')

        self.tab_control.pack(expand=1, fill='both')

        self.create_search_tab()
        self.create_results_tab()

    def create_search_tab(self):
        self.search_label = tk.Label(self.search_tab, text="Enter product name:")
        self.search_label.pack(pady=5)

        self.search_entry = tk.Entry(self.search_tab, width=50)
        self.search_entry.pack(pady=5)

        self.search_button = tk.Button(self.search_tab, text="Search", command=self.search_product)
        self.search_button.pack(pady=5)

    def create_results_tab(self):
        self.results_text = scrolledtext.ScrolledText(self.results_tab, wrap=tk.WORD, width=80, height=20)
        self.results_text.pack(pady=5, padx=5)

    def search_product(self):
        product_name = self.search_entry.get().strip()
        if product_name:
            if product_name in self.searched_products:
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, "Product has already been searched.")
            else:
                product_data = search_product(product_name)
                result = format_product_details(product_data)
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, result)
                save_search_history(product_name)
                self.searched_products.add(product_name)
        else:
            messagebox.showwarning("Input Error", "Please enter a product name.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductSearchApp(root)
    root.mainloop()
