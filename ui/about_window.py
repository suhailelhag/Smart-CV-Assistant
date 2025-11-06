# ui/about_window.py

import tkinter as tk
from tkinter import ttk
import webbrowser  # <-- تم استيراد مكتبة متصفح الويب
from PIL import Image, ImageTk
from language import _
from path_utils import resource_path

class AboutWindow(tk.Toplevel):
    """
    A window to display application and developer information.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.withdraw()  # Hide window until it's ready

        self.title(_("about_window_title"))
        try:
            self.iconbitmap(resource_path("icon/icon.ico"))
        except tk.TclError:
            pass  # Ignore if icon not found

        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)

        # --- Main container ---
        container = ttk.Frame(self, padding=25)
        container.pack(expand=True, fill="both")

        # --- Logo ---
        try:
            img = Image.open(resource_path("icon/icon.ico")).resize((64, 64), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(img)
            logo_label = ttk.Label(container, image=self.logo_photo)
            logo_label.pack(pady=(0, 15))
        except Exception as e:
            print(f"Could not load logo: {e}")

        # --- Information Labels ---
        ttk.Label(container, text="Smart CV Assistant", font=("Helvetica", 16, "bold")).pack()
        ttk.Label(container, text=_("version_info", version="1.0.0")).pack(pady=(0, 15))

        ttk.Label(container, text=_("developed_by", name="Suhail Elhag")).pack()
        ttk.Label(container, text="Email: suhailalhag@hotmail.com").pack()
        
        # --- LinkedIn Section (Modified) ---
        # 1. Create a frame to hold the label and the link side-by-side
        linkedin_frame = ttk.Frame(container)
        linkedin_frame.pack(pady=(0, 20))

        # 2. Add the static text "Linkedin: " and store the widget in a variable
        static_label = ttk.Label(linkedin_frame, text="Linkedin: ")
        static_label.pack(side="left")

        # 3. Add the clickable link
        link_text = "linkedin.com/in/suhail-elhag"
        link_url = "https://linkedin.com/in/suhail-elhag"
        
        link_label = ttk.Label(linkedin_frame, text=link_text, foreground="blue", cursor="hand2")
        
        # 4. *** NEW: Ensure the link font is identical to the static label's font ***
        link_label.configure(font=static_label.cget("font"))
        
        link_label.pack(side="left")

        # 5. Bind the click event to open the URL
        link_label.bind("<Button-1>", lambda e: webbrowser.open_new(link_url))
        
        # --- End of LinkedIn Section ---

        ttk.Label(container, text="© 2025 All rights reserved", font=("Helvetica", 8)).pack()

        # --- Center the window ---
        self.center_window()

        # Close on click or key press
        self.bind("<Button-1>", lambda e: self.destroy())
        self.bind("<Key>", lambda e: self.destroy())

    def center_window(self):
        """Center the dialog on the screen."""
        self.update_idletasks()

        # Get window and screen dimensions
        window_width = self.winfo_reqwidth()
        window_height = self.winfo_reqheight()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate center position
        center_x = (screen_width - window_width) // 2
        center_y = (screen_height - window_height) // 2

        # Set window position and make it visible
        self.geometry(f"+{center_x}+{center_y}")
        self.deiconify()

        # Ensure window is focused
        self.lift()
        self.focus_force()