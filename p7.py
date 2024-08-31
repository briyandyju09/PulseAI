import requests
import openai
import csv
import os
from textual import App, Widget, Header, Footer, Button, Input, Static
from textual.widgets import DataTable

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

class ProductSearchApp(App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.searched_products = load_search_history()
        self.results = []

    async def on_mount(self):
        self.header = Header()
        self.footer = Footer()
        self.search_input = Input(placeholder="Enter product name...")
        self.search_button = Button(label="Search", on_click=self.on_search)
        self.results_table = DataTable(header=["Field", "Value"], rows=[])

        await self.view.dock(self.header, edge="top")
        await self.view.dock(self.footer, edge="bottom")
        await self.view.dock(self.search_input, edge="top", size=3)
        await self.view.dock(self.search_button, edge="top", size=3)
        await self.view.dock(self.results_table, edge="top")

    async def on_search(self, event):
        product_name = self.search_input.value.strip()
        if product_name:
            if product_name in self.searched_products:
                self.results_table.update(rows=[["Product", "Already Searched"]])
            else:
                product_data = search_product(product_name)
                self.update_results(product_data)
                save_search_history(product_name)
                self.searched_products.add(product_name)
        self.search_input.value = ""

    def update_results(self, product_data):
        if product_data and 'product' in product_data:
            product = product_data['product']
            rows = [
                ["Product Name", product.get('product_name', 'Not Available')],
                ["Brand", product.get('brands', 'Not Available')],
                ["Quantity", product.get('quantity', 'Not Available')],
                ["Ingredients", product.get('ingredients_text', 'Not Available')],
                ["Categories", product.get('categories', 'Not Available')],
                ["Labels", product.get('labels', 'Not Available')],
            ]
            if 'nutriments' in product:
                nutriments = product['nutriments']
                rows.extend([
                    ["Calories (kcal)", nutriments.get('energy-kcal', 'Not Available')],
                    ["Fat (g)", nutriments.get('fat', 'Not Available')],
                    ["Saturated Fat (g)", nutriments.get('saturated-fat', 'Not Available')],
                    ["Carbohydrates (g)", nutriments.get('carbohydrates', 'Not Available')],
                    ["Sugars (g)", nutriments.get('sugars', 'Not Available')],
                    ["Fiber (g)", nutriments.get('fiber', 'Not Available')],
                    ["Proteins (g)", nutriments.get('proteins', 'Not Available')],
                    ["Salt (g)", nutriments.get('salt', 'Not Available')]
                ])
            else:
                rows.append(["Nutritional Information", "Not Available"])
            
            ingredients = product.get('ingredients_text', 'Not Available')
            if ingredients != 'Not Available':
                restriction_analysis = analyze_ingredients(ingredients)
                rows.append(["Dietary Restrictions Analysis", restriction_analysis])
            else:
                rows.append(["Dietary Restrictions Analysis", "Not Available"])
        else:
            rows = [["Product", "Not Found or No Data Available"]]
        
        self.results_table.update(rows=rows)

if __name__ == "__main__":
    ProductSearchApp.run()
