# ui/template_tab.py

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from language import language_manager, _
from settings_manager import settings_manager
from path_utils import resource_path

class TemplateTab:
    def __init__(self, parent_tab, controller):
        """
        Creates all components inside the "Templates" tab.
        - parent_tab: The parent frame (tab) where these components will be placed.
        - controller: The object responsible for application logic.
        """
        self.parent = parent_tab
        self.controller = controller
        self.selected_template = tk.StringVar()
        
        # Lists to hold PhotoImage objects to prevent garbage collection
        self.modern_photos = []
        self.professional_photos = []
        self.enlarged_photo = None # To hold the enlarged photo object

        self.load_template_preference()
        language_manager.add_observer(self.update_language)
        self.create_widgets()

    def create_widgets(self):
        """Creates and arranges all widgets in the tab using a more efficient grid layout."""
        container = ttk.Frame(self.parent, padding=20)
        container.pack(fill="both", expand=True)

        self.template_frame = ttk.LabelFrame(container, text=_("template_selection_frame"), padding=15)
        self.template_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Configure the grid columns to have equal weight, allowing them to expand
        self.template_frame.grid_columnconfigure(0, weight=1)
        self.template_frame.grid_columnconfigure(1, weight=1)

        # --- Template 1: Modern ---
        self.modern_title, self.modern_desc = self._create_template_widget(
            parent=self.template_frame,
            title_key="template_modern_name",
            desc_key="template_modern_desc",
            image_paths=["images/Template 1-1.jpg", "images/Template 1-2.jpg"],
            photo_list=self.modern_photos,
            value="modern",
            col=0
        )

        # --- Template 2: Professional ---
        self.professional_title, self.professional_desc = self._create_template_widget(
            parent=self.template_frame,
            title_key="template_professional_name",
            desc_key="template_professional_desc",
            image_paths=["images/Template 2-1.jpg", "images/Template 2-2.jpg"],
            photo_list=self.professional_photos,
            value="professional",
            col=1
        )

    def _create_template_widget(self, parent, title_key, desc_key, image_paths, photo_list, value, col):
        """
        Helper function to create a single template selection widget.
        This avoids code duplication and simplifies adding new templates.
        """
        # --- Main frame for the template option ---
        option_frame = ttk.Frame(parent, padding=10, relief="solid", borderwidth=1)
        option_frame.grid(row=0, column=col, padx=10, pady=5, sticky="nsew")

        # --- Radio Button ---
        radio_button = ttk.Radiobutton(
            option_frame,
            variable=self.selected_template,
            value=value,
            command=self.save_template_preference
        )
        radio_button.pack(side="left", padx=(0, 15), anchor="n")

        # --- Frame for all other details (text and images) ---
        details_frame = ttk.Frame(option_frame)
        details_frame.pack(side="left", fill="x", expand=True)

        # --- Text content ---
        title_label = ttk.Label(details_frame, text=_(title_key), font=("Helvetica", 11, "bold"))
        title_label.pack(anchor="w")
        desc_label = ttk.Label(details_frame, text=_(desc_key), wraplength=400, justify="left")
        desc_label.pack(anchor="w", pady=(2, 10))

        # --- Image previews ---
        image_container = ttk.Frame(details_frame)
        image_container.pack()

        for path in image_paths:
            try:
                # ✅ تعديل هنا لاستخدام resource_path
                full_path = resource_path(path)
                if os.path.exists(full_path):
                    img = Image.open(full_path).resize((100, 141), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    photo_list.append(photo)
                    
                    # Create a label for the image and make it clickable
                    img_label = ttk.Label(image_container, image=photo, cursor="hand2")
                    img_label.pack(side="left", padx=5)
                    img_label.bind("<Button-1>", lambda e, p=path: self._show_enlarged_image(p))

            except Exception as e:
                print(f"Could not load template image '{path}': {e}")
        
        # Return labels that need to be updated when the language changes
        return title_label, desc_label

    def _show_enlarged_image(self, image_path):
        """
        Opens a new window to display the full-size image.
        This version explicitly sets the window size based on the image dimensions
        and resizes the image if it's larger than the screen.
        """
        try:
            top = tk.Toplevel(self.parent)
            top.withdraw() # <-- الخطوة 1: إخفاء النافذة فوراً عند إنشائها
            top.title(_("template_preview"))
            top.resizable(False, False)
            top.transient(self.parent)
            top.grab_set()
            try:
                # Set window icon
                top.iconbitmap(resource_path("icon/icon.ico"))
            except tk.TclError:
                pass  # Ignore if icon not found

            # ✅ تعديل هنا لاستخدام resource_path
            img_full = Image.open(resource_path(image_path))

            # --- NEW AND IMPROVED FIX ---

            # 1. Get screen dimensions to calculate max allowed size for the preview
            screen_width = top.winfo_screenwidth()
            screen_height = top.winfo_screenheight()
            # Set max preview size to 90% of the screen dimension
            max_width = int(screen_width * 0.9)
            max_height = int(screen_height * 0.9)

            # 2. Get original image dimensions
            img_width, img_height = img_full.size

            # 3. If the image is larger than the allowed max size, resize it
            if img_width > max_width or img_height > max_height:
                # Calculate the scaling ratio to fit within the max dimensions
                ratio = min(max_width / img_width, max_height / img_height)
                new_width = int(img_width * ratio)
                new_height = int(img_height * ratio)
                # Resize the image using Pillow's high-quality resampling filter
                img_full = img_full.resize((new_width, new_height), Image.Resampling.LANCZOS)
                # Update the dimensions to the new resized dimensions
                img_width, img_height = new_width, new_height
            
            # 4. Create the PhotoImage object from the (potentially resized) Pillow image
            self.enlarged_photo = ImageTk.PhotoImage(img_full)

            img_label = ttk.Label(top, image=self.enlarged_photo)
            img_label.pack()
            
            # Bind events to close the window
            img_label.bind("<Button-1>", lambda e: top.destroy())
            top.bind("<Key>", lambda e: top.destroy())
            top.bind("<FocusOut>", lambda e: top.destroy())

            # 5. Calculate the centered position on the screen
            center_x = int((screen_width / 2) - (img_width / 2))
            center_y = int((screen_height / 2) - (img_height / 2))

            # 6. Set the window's geometry using the exact image dimensions
            top.geometry(f'{img_width}x{img_height}+{center_x}+{center_y}')

            top.deiconify() # <-- الخطوة 2: إظهار النافذة في مكانها ومقاسها النهائي

            # --- END OF FIX ---

        except Exception as e:
            print(f"Could not open enlarged image '{image_path}': {e}")

    def get_selected_template(self):
        """Returns the key of the selected template."""
        return self.selected_template.get()

    def save_template_preference(self):
        """Save current template preference to settings."""
        try:
            preferences = settings_manager.load_settings('app_preferences', {})
            preferences['selected_template'] = self.get_selected_template()
            settings_manager.save_settings('app_preferences', preferences)
        except Exception as e:
            print(f"Error saving template preference: {e}")

    def load_template_preference(self):
        """Load saved template preference from settings."""
        try:
            preferences = settings_manager.load_settings('app_preferences', {})
            saved_template = preferences.get('selected_template', 'modern') # Default to 'modern'
            self.selected_template.set(saved_template)
        except Exception as e:
            print(f"Error loading template preference: {e}")
            self.selected_template.set('modern')

    def update_language(self):
        """Update all UI text when language changes."""
        self.template_frame.config(text=_("template_selection_frame"))
        self.modern_title.config(text=_("template_modern_name"))
        self.modern_desc.config(text=_("template_modern_desc"))
        self.professional_title.config(text=_("template_professional_name"))
        self.professional_desc.config(text=_("template_professional_desc"))
