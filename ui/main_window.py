# ui/main_window.py

import tkinter as tk
from tkinter import ttk
from .user_info_tab import UserInfoTab
from .settings_tab import SettingsTab
from .ai_settings_tab import AISettingsTab
from .template_tab import TemplateTab
from language import language_manager, _
from path_utils import resource_path

class MainWindow:
    def __init__(self, root, controller):
        """
        Creates the main application window.
        - root: The Tkinter root window.
        - controller: The object responsible for application logic.
        """
        self.root = root
        self.controller = controller
        self.root.title(_("app_title"))
        self.root.geometry("900x750")
        self.root.minsize(800, 600)  # Minimum window size

        # Window appearance settings
        self.root.resizable(True, True)  # Allow resizing

        # Set window icon if available (optional)
        try:
            # Use the icon from the 'icon' folder
            self.root.iconbitmap(resource_path("icon/icon.ico"))
        except:
            pass

        # --- Design improvements ---
        style = ttk.Style(self.root)
        style.theme_use('clam') # Choose modern theme

        # Style customization
        style.configure("TButton", padding=6, relief="flat", font=('Helvetica', 10))
        style.configure("Accent.TButton", foreground="white", background="#0078D7") # Accent button

        # Register for language change notifications
        language_manager.add_observer(self.update_language)

        self.setup_ui()

    def setup_ui(self):
        """
        Sets up the main UI components like tabs and main button.
        """
        # Main content frame for better margins
        main_content_frame = ttk.Frame(self.root, padding=15)
        main_content_frame.pack(fill="both", expand=True)

        # --- Top frame for buttons ---
        top_frame = ttk.Frame(main_content_frame, padding=(0, 0, 0, 10))
        top_frame.pack(side="top", fill="x")

        # Container to center buttons
        button_container = ttk.Frame(top_frame)
        button_container.pack()

        self.generate_button = ttk.Button(
            button_container,
            text=_("generate_cv_button"),
            command=self.controller.generate_cv,
            style="Accent.TButton" # Apply accent style
        )
        self.generate_button.pack(side="left", padx=10)

        self.reorder_button = ttk.Button(
            button_container,
            text=_("reorder_sections_button"),
            command=lambda: self.controller.open_reorder_dialog(self.reorder_button)
        )
        self.reorder_button.pack(side="left", padx=10)

        # Reset button
        self.reset_button = ttk.Button(
            button_container,
            text=_("reset_button"),
            command=lambda: self.controller.open_reset_dialog(self.reset_button),
            style="Danger.TButton"
        )
        self.reset_button.pack(side="left", padx=10)

        # About button
        self.about_button = ttk.Button(
            button_container,
            text=_("about_button"),
            command=self.controller.open_about_window
        )
        self.about_button.pack(side="left", padx=10)

        # Language switcher button
        self.language_button = ttk.Button(
            button_container,
            text=_("language_switch_button"),
            command=self.toggle_language
        )
        self.language_button.pack(side="left", padx=10)

        self.notebook = ttk.Notebook(main_content_frame)
        self.notebook.pack(fill="both", expand=True)

        self.tab1_frame = ttk.Frame(self.notebook, padding=10)
        self.tab2_frame = ttk.Frame(self.notebook, padding=10)
        self.tab3_frame = ttk.Frame(self.notebook, padding=10)
        self.tab4_frame = ttk.Frame(self.notebook, padding=10)

        self.notebook.add(self.tab1_frame, text=_('tab_personal_info'))
        self.notebook.add(self.tab2_frame, text=_('tab_job_settings'))
        self.notebook.add(self.tab4_frame, text=_('tab_templates'))
        self.notebook.add(self.tab3_frame, text=_('tab_ai_settings')) # AI settings is now last

        self.user_info_tab = UserInfoTab(self.tab1_frame, self.controller)
        self.settings_tab = SettingsTab(self.tab2_frame, self.controller)
        self.ai_settings_tab = AISettingsTab(self.tab3_frame, self.controller)
        self.template_tab = TemplateTab(self.tab4_frame, self.controller)

    def toggle_language(self):
        """Toggle between Arabic and English languages."""
        language_manager.toggle_language()

    def update_language(self):
        """Update all UI text when language changes."""
        # Update window title
        self.root.title(_("app_title"))

        # Update button texts
        self.generate_button.config(text=_("generate_cv_button"))
        self.reorder_button.config(text=_("reorder_sections_button"))
        self.reset_button.config(text=_("reset_button"))
        self.about_button.config(text=_("about_button"))
        self.language_button.config(text=_("language_switch_button"))

        # Update tab texts
        self.notebook.tab(self.tab1_frame, text=_('tab_personal_info'))
        self.notebook.tab(self.tab2_frame, text=_('tab_job_settings'))
        self.notebook.tab(self.tab4_frame, text=_('tab_templates'))
        self.notebook.tab(self.tab3_frame, text=_('tab_ai_settings'))

        # The individual tabs will update themselves through their own observers