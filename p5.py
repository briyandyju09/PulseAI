import requests
import openai


openai.api_key = 'your_openai_api_key'

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
    while True:
        query = input("Enter the food item you want to search for (or type 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        product_data = search_product(query)
        print_product_details(product_data)

if __name__ == "__main__":
    main()
