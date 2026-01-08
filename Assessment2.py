from tkinter import *
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO

class MealApp:
    def __init__(self, root):
        self.root = root
        self.root.title("The Meal Application")
        self.root.geometry("1000x700")
        self.root.config(bg="#f5f5f5")
        
        # Variables to store data
        self.current_meals = []
        self.categories = []
        self.areas = []
        self.ingredients = []
        
        # Setup the GUI
        self.create_widgets()
    
    def create_widgets(self):
        # Top title
        title = Label(self.root, text="DISH DISCOVERY", 
                        font=("Arial", 22, "bold"), bg="#f5f5f5")
        title.pack(pady=15)
        
        # Search frame
        search_frame = LabelFrame(self.root, font=("Arial", 11, "bold"), bg="white")
        search_frame.pack(padx=10, pady=5, fill=X)
        
        # Radio buttons for search type
        radio_frame = Frame(search_frame, bg="white")
        radio_frame.pack(pady=5)
        
        Label(radio_frame, text="Filter by:", bg="white").pack(side=LEFT, padx=5)
        
        self.search_type = StringVar(value="name")
        
        Radiobutton(radio_frame, text="Name", variable=self.search_type, value="name", bg="white").pack(side=LEFT)
        Radiobutton(radio_frame, text="Ingredient", variable=self.search_type, value="ingredient", bg="white").pack(side=LEFT)
        Radiobutton(radio_frame, text="Category", variable=self.search_type, value="category", bg="white").pack(side=LEFT)
        Radiobutton(radio_frame, text="Area", variable=self.search_type, value="area", bg="white").pack(side=LEFT)
        
        # Search entry and buttons
        entry_frame = Frame(search_frame, bg="white")
        entry_frame.pack(pady=5)
        
        Label(entry_frame, text="Enter search:", bg="white").pack(side=LEFT, padx=5)
        
        self.search_entry = Entry(entry_frame, width=35, font=("Arial", 10))
        self.search_entry.pack(side=LEFT, padx=5)
        self.search_entry.bind('<Return>', lambda e: self.search_meals())
        
        Button(entry_frame, text="Search", command=self.search_meals, fg="black", width=10).pack(side=LEFT, padx=3)
        Button(entry_frame, text="Random", command=self.get_random, fg="black", width=10).pack(side=LEFT, padx=3)
        Button(entry_frame, text="Clear", command=self.clear_all, fg="black", width=10).pack(side=LEFT, padx=3)
        
        # Browse buttons
        browse_frame = Frame(search_frame, bg="white")
        browse_frame.pack(pady=5)
        
        Label(browse_frame, text="Browse:", bg="white").pack(side=LEFT, padx=5)
        
        Button(browse_frame, text="Categories", command=self.browse_categories, fg="black", width=12).pack(side=LEFT, padx=2)
        Button(browse_frame, text="Areas", command=self.browse_areas, fg="black", width=12).pack(side=LEFT, padx=2)
        Button(browse_frame, text="Ingredients", command=self.browse_ingredients, fg="black", width=12).pack(side=LEFT, padx=2)
        
        # Main content area
        content_frame = Frame(self.root, bg="#f5f5f5")
        content_frame.pack(padx=10, pady=5, fill=BOTH, expand=True)
        
        # Left side - results list
        left_frame = Frame(content_frame, bg="white")
        left_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5))
        
        Label(left_frame, text="Results:", font=("Arial", 11, "bold"), bg="white").pack(pady=5)
        
        # Listbox with scrollbar
        list_scroll = Scrollbar(left_frame)
        list_scroll.pack(side=RIGHT, fill=Y)
        
        self.results_listbox = Listbox(left_frame, font=("Arial", 10), yscrollcommand=list_scroll.set)
        self.results_listbox.pack(fill=BOTH, expand=True, padx=5, pady=5)
        list_scroll.config(command=self.results_listbox.yview)
        
        self.results_listbox.bind('<<ListboxSelect>>', self.show_details)
        
        # Right side - details
        right_frame = Frame(content_frame, bg="white", width=450)
        right_frame.pack(side=RIGHT, fill=BOTH, padx=(5, 0))
        right_frame.pack_propagate(False)
        
        Label(right_frame, text="Details:", font=("Arial", 11, "bold"), bg="white").pack(pady=5)
        
        # Image display
        self.image_label = Label(right_frame, bg="white", text="Select a meal to view")
        self.image_label.pack(pady=10)
        
        # Details text area
        text_scroll = Scrollbar(right_frame)
        text_scroll.pack(side=RIGHT, fill=Y)
        
        self.details_text = Text(right_frame, wrap=WORD, font=("Arial", 9), yscrollcommand=text_scroll.set)
        self.details_text.pack(fill=BOTH, expand=True, padx=5, pady=5)
        text_scroll.config(command=self.details_text.yview)
        
        # Status bar at bottom
        self.status_label = Label(self.root, text="Ready", anchor=W, bg="#e0e0e0", font=("Arial", 9))
        self.status_label.pack(side=BOTTOM, fill=X)
    
    # Search meals function
    def search_meals(self):
        query = self.search_entry.get().strip()
        
        if not query:
            messagebox.showwarning("Empty Search", "Please enter something to search!")
            return
        
        search_type = self.search_type.get()
        
        # Build the API URL based on search type
        if search_type == "name":
            url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={query}"
        elif search_type == "ingredient":
            url = f"https://www.themealdb.com/api/json/v1/1/filter.php?i={query}"
        elif search_type == "category":
            url = f"https://www.themealdb.com/api/json/v1/1/filter.php?c={query}"
        elif search_type == "area":
            url = f"https://www.themealdb.com/api/json/v1/1/filter.php?a={query}"
        
        self.status_label.config(text="Searching...")
        self.root.update()
        
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data['meals']:
                self.current_meals = data['meals']
                self.display_results()
                self.status_label.config(text=f"Found {len(self.current_meals)} results")
            else:
                self.current_meals = []
                self.results_listbox.delete(0, END)
                self.status_label.config(text="No results found")
                messagebox.showinfo("No Results", "No meals found for your search")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search: {str(e)}")
            self.status_label.config(text="Error occurred")
    
    # Display search results in listbox
    def display_results(self):
        self.results_listbox.delete(0, END)
        
        for meal in self.current_meals:
            self.results_listbox.insert(END, meal['strMeal'])
    
    # Show meal details when selected
    def show_details(self, event):
        selection = self.results_listbox.curselection()
        
        if not selection:
            return
        
        index = selection[0]
        meal = self.current_meals[index]
        
        # Get full meal details if needed
        if 'strInstructions' not in meal:
            meal_id = meal['idMeal']
            url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"
            
            try:
                response = requests.get(url, timeout=10)
                data = response.json()
                meal = data['meals'][0]
            except:
                pass
        
        # Clear previous details
        self.details_text.delete(1.0, END)
        
        # Display meal information
        self.details_text.insert(END, f"{meal['strMeal']}\n\n", "title")
        self.details_text.tag_config("title", font=("Arial", 13, "bold"))
        
        self.details_text.insert(END, f"Category: {meal.get('strCategory', 'N/A')}\n")
        self.details_text.insert(END, f"Area: {meal.get('strArea', 'N/A')}\n")
        
        if meal.get('strTags'):
            self.details_text.insert(END, f"Tags: {meal['strTags']}\n")
        
        self.details_text.insert(END, "\n")
        
        # Show ingredients
        self.details_text.insert(END, "Ingredients:\n", "bold")
        self.details_text.tag_config("bold", font=("Arial", 10, "bold"))
        
        for i in range(1, 21):
            ingredient = meal.get(f'strIngredient{i}')
            measure = meal.get(f'strMeasure{i}')
            
            if ingredient and ingredient.strip():
                self.details_text.insert(END, f"  • {measure} {ingredient}\n")
        
        # Show instructions
        if meal.get('strInstructions'):
            self.details_text.insert(END, f"\nInstructions:\n", "bold")
            self.details_text.insert(END, f"{meal['strInstructions']}\n\n")
        
        # Show source link
        if meal.get('strSource'):
            self.details_text.insert(END, f"Source: {meal['strSource']}\n")
        
        # Load and show image
        if meal.get('strMealThumb'):
            self.load_image(meal['strMealThumb'])
    
    # Load meal image
    def load_image(self, image_url):
        try:
            response = requests.get(image_url, timeout=10)
            img_data = response.content
            
            img = Image.open(BytesIO(img_data))
            img = img.resize((220, 220))
            
            photo = ImageTk.PhotoImage(img)
            
            self.image_label.config(image=photo, text="")
            self.image_label.image = photo
        
        except Exception as e:
            self.image_label.config(image='', text="Image not available")
    
    # Get random meal
    def get_random(self):
        url = "https://www.themealdb.com/api/json/v1/1/random.php"
        
        self.status_label.config(text="Getting random meal...")
        self.root.update()
        
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            
            self.current_meals = data['meals']
            self.display_results()
            
            # Auto-select and show details
            self.results_listbox.selection_set(0)
            self.show_details(None)
            
            self.status_label.config(text="Random meal loaded!")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get random meal: {str(e)}")
            self.status_label.config(text="Error occurred")
    
    # Browse categories
    def browse_categories(self):
        url = "https://www.themealdb.com/api/json/v1/1/categories.php"
        
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data['categories']:
                self.categories = data['categories']
                self.show_browse_window("Categories", self.categories, 'strCategory', 'category')
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load categories: {str(e)}")
    
    # Browse areas
    def browse_areas(self):
        url = "https://www.themealdb.com/api/json/v1/1/list.php?a=list"
        
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data['meals']:
                self.areas = data['meals']
                self.show_browse_window("Areas", self.areas, 'strArea', 'area')
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load areas: {str(e)}")
    
    # Browse ingredients
    def browse_ingredients(self):
        url = "https://www.themealdb.com/api/json/v1/1/list.php?i=list"
        
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data['meals']:
                self.ingredients = data['meals'][:100]  # First 100 ingredients
                self.show_browse_window("Ingredients", self.ingredients, 'strIngredient', 'ingredient')
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load ingredients: {str(e)}")
    
    # Show browse window
    def show_browse_window(self, title, items, key, search_type):
        window = Toplevel(self.root)
        window.title(f"Browse {title}")
        window.geometry("450x550")
        window.config(bg="white")
        
        Label(window, text=f"Select {title[:-1]}:", font=("Arial", 12, "bold"), bg="white").pack(pady=10)
        
        # Listbox to show items
        scroll = Scrollbar(window)
        scroll.pack(side=RIGHT, fill=Y)
        
        listbox = Listbox(window, font=("Arial", 10), yscrollcommand=scroll.set)
        listbox.pack(fill=BOTH, expand=True, padx=10, pady=10)
        scroll.config(command=listbox.yview)
        
        # Populate listbox
        for item in items:
            listbox.insert(END, item[key])
        
        # Select button
        def select_item():
            selection = listbox.curselection()
            if selection:
                selected = listbox.get(selection[0])
                self.search_type.set(search_type)
                self.search_entry.delete(0, END)
                self.search_entry.insert(0, selected)
                window.destroy()
                self.search_meals()
        
        listbox.bind('<Double-Button-1>', lambda e: select_item())
        
        Button(window, text="Select", command=select_item, bg="#4CAF50", fg="white", width=15).pack(pady=10)
    
    # Clear everything
    def clear_all(self):
        self.search_entry.delete(0, END)
        self.results_listbox.delete(0, END)
        self.details_text.delete(1.0, END)
        self.image_label.config(image='', text="Select a meal to view")
        self.current_meals = []
        self.status_label.config(text="Cleared")

# Main program
if __name__ == "__main__":
    root = Tk()
    app = MealApp(root)
    root.mainloop()