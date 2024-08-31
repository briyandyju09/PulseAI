import tkinter as tk
from tkinter import messagebox
import json
import os

class PreferenceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sustain")
        self.preferences = {
            "Diabetic": tk.BooleanVar(),
            "Gluten-Free": tk.BooleanVar(),
            "Islamic": tk.BooleanVar(),
            "Religious Restriction": tk.BooleanVar(),
            "Vegan": tk.BooleanVar(),
            "Vegetarian": tk.BooleanVar(),
            "Non-Alcoholic": tk.BooleanVar(),
            "Lactose Intolerant": tk.BooleanVar()
        }
        self.load_preferences()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Select Your Dietary Preferences:", font=("Arial", 16)).pack(pady=10)
        for pref, var in self.preferences.items():
            tk.Checkbutton(self.root, text=pref, variable=var).pack(anchor="w")
        tk.Button(self.root, text="Submit", command=self.submit).pack(pady=10)
        tk.Button(self.root, text="Show Selected Preferences", command=self.show_preferences).pack(pady=5)

    def submit(self):
        selected_prefs = {pref: var.get() for pref, var in self.preferences.items() if var.get()}
        if not selected_prefs:
            messagebox.showwarning("No Selection", "Please select at least one preference.")
            return
        self.save_preferences(selected_prefs)
        recommendations = self.get_recommendations(selected_prefs)
        messagebox.showinfo("Preferences Saved", f"Your preferences have been saved.\nRecommendations:\n{recommendations}")
        self.root.destroy()

    def show_preferences(self):
        selected_prefs = [pref for pref, var in self.preferences.items() if var.get()]
        if not selected_prefs:
            messagebox.showwarning("No Selection", "No preferences selected yet.")
        else:
            messagebox.showinfo("Selected Preferences", "\n".join(selected_prefs))

    def load_preferences(self):
        if os.path.exists("preferences.json"):
            with open("preferences.json", "r") as file:
                saved_prefs = json.load(file)
                for pref, value in saved_prefs.items():
                    if pref in self.preferences:
                        self.preferences[pref].set(value)

    def save_preferences(self, selected_prefs):
        with open("preferences.json", "w") as file:
            json.dump(selected_prefs, file)

    def get_recommendations(self, selected_prefs):
        recommendations = []
        if "Vegan" in selected_prefs:
            recommendations.append("Try plant-based recipes.")
        if "Gluten-Free" in selected_prefs:
            recommendations.append("Explore gluten-free products.")
        if "Diabetic" in selected_prefs:
            recommendations.append("Check out low-sugar options.")
        if "Islamic" in selected_prefs:
            recommendations.append("Look for Halal-certified items.")
        if "Non-Alcoholic" in selected_prefs:
            recommendations.append("Discover non-alcoholic beverages.")
        if "Vegetarian" in selected_prefs:
            recommendations.append("Consider vegetarian meals.")
        if "Lactose Intolerant" in selected_prefs:
            recommendations.append("Find lactose-free alternatives.")
        if "Religious Restriction" in selected_prefs:
            recommendations.append("Respect dietary laws specific to your religion.")
        return "\n".join(recommendations)

def main():
    root = tk.Tk()
    app = PreferenceApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
