# PulseAI

> A Tkinter desktop app for making dietary-aware food choices — search products and analyse ingredients through the Spoonacular API.

## Stack

- **Language:** Python 3
- **GUI:** Tkinter / ttk
- **Data & HTTP:** `requests`, `pandas`
- **External API:** [Spoonacular](https://spoonacular.com/food-api)
- **Storage:** local JSON (preferences) and CSV (search history)

## Description

Pulse helps users make eco-friendly and ethical food choices. You set your dietary
preferences (Diabetic, Gluten-Free, Vegan, Halal, and more), then search real food products
and analyse their ingredients so you can decide what fits your diet. Product data and
ingredient analysis are pulled live from the Spoonacular API.

> **Note:** this is an evolving prototype. The files `p1.py` … `p9.py` are successive
> iterations of the app; **`p9.py` is the latest and most complete** (tabbed product search
> with persistent history). The earlier scripts are the preference-selector prototypes kept
> for history.

## Features

- Dietary-preference selection with local persistence (`preferences.json`).
- Live food-product search via the Spoonacular API.
- Ingredient analysis for searched products.
- Tabbed Tkinter UI (search + results) in the current build (`p9.py`).
- Search history saved to `searched_products.csv`, with duplicate detection.

## How to Build / Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Get a free API key from [Spoonacular](https://spoonacular.com/food-api) and set it in
   `p9.py` (replace the `spoonacular_api_key` placeholder).
3. Run the latest build:
   ```bash
   python p9.py
   ```

## License

Released under the [MIT License](LICENSE).
