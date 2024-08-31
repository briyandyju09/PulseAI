import requests
import openai
import csv
import os


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

def print_product_details(product_data):
    if product_data and 'product' in product_data:
        product = product_data['product']
        print("Product Name:", product.get('product_name', 'Not Available'))
        print("Brand:", product.get('brands', 'Not Available'))
        print("Quantity:", product.get('quantity', 'Not Available'))
        print("Ingredients:", product.get('ingredients_text', 'Not Available'))
        print("Categories:", product.get('categories', 'Not Available'))
        print("Labels:", product.get('labels', 'Not Available'))
        print("Nutritional Information (100g):")
        if 'nutriments' in product:
            nutriments = product['nutriments']
            print("Calories (kcal):", nutriments.get('energy-kcal', 'Not Available'))
            print("Fat (g):", nutriments.get('fat', 'Not Available'))
            print("Saturated Fat (g):", nutriments.get('saturated-fat', 'Not Available'))
            print("Carbohydrates (g):", nutriments.get('carbohydrates', 'Not Available'))
            print("Sugars (g):", nutriments.get('sugars', 'Not Available'))
            print("Fiber (g):", nutriments.get('fiber', 'Not Available'))
            print("Proteins (g):", nutriments.get('proteins', 'Not Available'))
            print("Salt (g):", nutriments.get('salt', 'Not Available'))
        else:
            print("Nutritional Information: Not Available")
        
        ingredients = product.get('ingredients_text', 'Not Available')
        if ingredients != 'Not Available':
            restriction_analysis = analyze_ingredients(ingredients)
            print("Dietary Restrictions Analysis:", restriction_analysis)
    else:
        print("Product not found or no data available.")

def main():
    print("Open Food Facts Product Search with Dietary Restrictions Analysis")
    searched_products = load_search_history()
    while True:
        query = input("Enter the food item you want to search for (or type 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        if query in searched_products:
            print("Product has already been searched.")
        else:
            product_data = search_product(query)
            print_product_details(product_data)
            save_search_history(query)
            searched_products.add(query)

if __name__ == "__main__":
    main()
