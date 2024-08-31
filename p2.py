import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os

class SustainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pulse")
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
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        title_label = ttk.Label(main_frame, text="Select Your Dietary Preferences:", font=("Helvetica", 14))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        self.checkbuttons = {}
        row = 1
        for pref, var in self.preferences.items():
            cb = ttk.Checkbutton(main_frame, text=pref, variable=var)
            cb.grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
            self.checkbuttons[pref] = cb
            row += 1
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=10)

        submit_button = ttk.Button(button_frame, text="Submit", command=self.submit)
        submit_button.grid(row=0, column=0, padx=5)

        reset_button = ttk.Button(button_frame, text="Reset", command=self.reset)
        reset_button.grid(row=0, column=1, padx=5)
        
        self.result_text = tk.Text(main_frame, height=8, width=50, wrap=tk.WORD)
        self.result_text.grid(row=row+1, column=0, columnspan=2, pady=10)
        
    def submit(self):
        selected_prefs = {pref: var.get() for pref, var in self.preferences.items() if var.get()}
        if not selected_prefs:
            messagebox.showwarning("No Selection", "Please select at least one preference.")
            return
        
        self.save_preferences(selected_prefs)
        recommendations = self.get_recommendations(selected_prefs)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, recommendations)

    def reset(self):
        for var in self.preferences.values():
            var.set(False)
        self.result_text.delete(1.0, tk.END)
        self.save_preferences({})

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
            recommendations.append("Explore innovative plant-based foods.")
        if "Gluten-Free" in selected_prefs:
            recommendations.append("Discover new gluten-free brands.")
        if "Diabetic" in selected_prefs:
            recommendations.append("Find advanced low-glycemic products.")
        if "Islamic" in selected_prefs:
            recommendations.append("Seek out certified Halal goods.")
        if "Non-Alcoholic" in selected_prefs:
            recommendations.append("Try the latest non-alcoholic beverages.")
        if "Vegetarian" in selected_prefs:
            recommendations.append("Consider cutting-edge vegetarian options.")
        if "Lactose Intolerant" in selected_prefs:
            recommendations.append("Explore innovative lactose-free alternatives.")
        if "Religious Restriction" in selected_prefs:
            recommendations.append("Respect dietary restrictions with thoughtful choices.")
        return "\n".join(recommendations)

def main():
    root = tk.Tk()
    app = SustainApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
