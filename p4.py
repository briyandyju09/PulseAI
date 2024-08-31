import requests

def search_product(product_name):
    base_url = "https://world.openfoodfacts.org/api/v0/product/"
    response = requests.get(f"{base_url}{product_name}.json")
    if response.status_code == 200:
        return response.json()
    else:
        return None

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
    else:
        print("Product not found or no data available.")

def main():
    print("Open Food Facts Product Search")
    while True:
        query = input("Enter the food item you want to search for (or type 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        product_data = search_product(query)
        print_product_details(product_data)

if __name__ == "__main__":
    main()
