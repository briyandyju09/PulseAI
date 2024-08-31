import requests
import openai
import csv
import os
import tkinter as tk
from tkinter import messagebox, scrolledtext

openai.api_key = 'your_openai_api_key'
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
    base_url = "https://world.openfoodfacts.org/api/v0/product/"
    response = requests.get(f"{base_url}{product_name}.json")
    if response.status_code == 200:
        return response.json()
    else:
        return None

def analyze_ingredients(ingredients):
    prompt = f"Analyze the following list of ingredients and determine if there are any dietary restrictions or allergies associated with them:\n{ingredients}\n\nAnswer in a concise manner."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        temperature=0.7
    )
    return response.choices[0].text.strip()

def format_product_details(product_data):
    if product_data and 'product' in product_data:
        product = product_data['product']
        details = [
            f"Product Name: {product.get('product_name', 'Not Available')}",
            f"Brand: {product.get('brands', 'Not Available')}",
            f"Quantity: {product.get('quantity', 'Not Available')}",
            f"Ingredients: {product.get('ingredients_text', 'Not Available')}",
            f"Categories: {product.get('categories', 'Not Available')}",
            f"Labels: {product.get('labels', 'Not Available')}"
        ]
        if 'nutriments' in product:
            nutriments = product['nutriments']
            details.extend([
                f"Calories (kcal): {nutriments.get('energy-kcal', 'Not Available')}",
                f"Fat (g): {nutriments.get('fat', 'Not Available')}",
                f"Saturated Fat (g): {nutriments.get('saturated-fat', 'Not Available')}",
                f"Carbohydrates (g): {nutriments.get('carbohydrates', 'Not Available')}",
                f"Sugars (g): {nutriments.get('sugars', 'Not Available')}",
                f"Fiber (g): {nutriments.get('fiber', 'Not Available')}",
                f"Proteins (g): {nutriments.get('proteins', 'Not Available')}",
                f"Salt (g): {nutriments.get('salt', 'Not Available')}"
            ])
        else:
            details.append("Nutritional Information: Not Available")
        
        ingredients = product.get('ingredients_text', 'Not Available')
        if ingredients != 'Not Available':
            restriction_analysis = analyze_ingredients(ingredients)
            details.append(f"Dietary Restrictions Analysis: {restriction_analysis}")
        else:
            details.append("Dietary Restrictions Analysis: Not Available")
    else:
        details = ["Product not found or no data available."]
    return '\n'.join(details)

class ProductSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Product Search and Dietary Analysis")
        self.searched_products = load_search_history()

        self.create_widgets()

    def create_widgets(self):
        self.search_label = tk.Label(self.root, text="Enter product name:")
        self.search_label.pack(pady=5)

        self.search_entry = tk.Entry(self.root, width=50)
        self.search_entry.pack(pady=5)

        self.search_button = tk.Button(self.root, text="Search", command=self.search_product)
        self.search_button.pack(pady=5)

        self.result_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=20)
        self.result_text.pack(pady=5)

    def search_product(self):
        product_name = self.search_entry.get().strip()
        if product_name:
            if product_name in self.searched_products:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "Product has already been searched.")
            else:
                product_data = search_product(product_name)
                result = format_product_details(product_data)
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, result)
                save_search_history(product_name)
                self.searched_products.add(product_name)
        else:
            messagebox.showwarning("Input Error", "Please enter a product name.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductSearchApp(root)
    root.mainloop()
