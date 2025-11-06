# ui/ai_settings_tab.py

import tkinter as tk
from tkinter import ttk
from language import language_manager, _
from settings_manager import settings_manager

class AISettingsTab:
    def __init__(self, parent_tab, controller):
        """
        Creates all components inside the "AI Settings" tab.
        - parent_tab: The parent frame (tab) where these components will be placed.
        - controller: The object responsible for application logic.
        """
        self.parent = parent_tab
        self.controller = controller

        # استخدام مدير الإعدادات المركزي
        self.settings_key = 'ai_providers'

        # Separate storage for each provider's settings
        self.provider_settings = {
            'openai': {
                'api_key': '',
                'model': 'gpt-4o',
                'http_referer': '',
                'x_title': ''
            },
            'openrouter': {
                'api_key': '',
                'model': 'gpt-4o',
                'http_referer': '',
                'x_title': ''
            }
        }

        # Track the current provider to know which one to save when switching
        self.current_provider = "openai"

        # Load saved settings
        self.load_settings_from_file()

        # Register for language change notifications
        language_manager.add_observer(self.update_language)

        self.create_widgets()
        self.load_saved_preferences()
        
    def create_widgets(self):
        # --- الإطار الرئيسي مع هوامش داخلية ---
        container = ttk.Frame(self.parent, padding=20)
        container.pack(fill="both", expand=True)
        
        # --- AI Settings Content ---
        self.ai_frame = ttk.LabelFrame(container, text=_("ai_settings_frame"), padding=20)
        self.ai_frame.pack(fill="x", pady=(0, 20))
        self.ai_frame.columnconfigure(1, weight=1)

        # Service provider
        provider_frame = ttk.Frame(self.ai_frame)
        provider_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 15))
        self.api_provider = tk.StringVar(value="openai")
        self.provider_label = ttk.Label(provider_frame, text=_("service_provider"))
        self.provider_label.pack(side="left", padx=(0, 15))
        ttk.Radiobutton(provider_frame, text="OpenAI", variable=self.api_provider, value="openai", command=lambda: self.toggle_openrouter_fields(True)).pack(side="left", padx=(0, 10))
        ttk.Radiobutton(provider_frame, text="OpenRouter", variable=self.api_provider, value="openrouter", command=lambda: self.toggle_openrouter_fields(True)).pack(side="left")

        # Input fields
        self.api_key_label = ttk.Label(self.ai_frame, text=_("api_key"))
        self.api_key_label.grid(row=1, column=0, padx=(0, 10), pady=8, sticky="w")
        self.api_key_entry = ttk.Entry(self.ai_frame, width=50, show="*")
        self.api_key_entry.grid(row=1, column=1, columnspan=2, padx=(0, 0), pady=8, sticky="ew")
        self.api_key_entry.bind("<FocusOut>", self._on_field_change)
        self.api_key_entry.bind("<KeyRelease>", self._on_field_change)

        self.model_label = ttk.Label(self.ai_frame, text=_("model_name"))
        self.model_label.grid(row=2, column=0, padx=(0, 10), pady=8, sticky="w")
        self.model_entry = ttk.Entry(self.ai_frame, width=50)
        self.model_entry.grid(row=2, column=1, columnspan=2, padx=(0, 0), pady=8, sticky="ew")
        self.model_entry.bind("<FocusOut>", self._on_field_change)
        self.model_entry.bind("<KeyRelease>", self._on_field_change)

        self.http_referer_label = ttk.Label(self.ai_frame, text=_("website_referer"))
        self.http_referer_entry = ttk.Entry(self.ai_frame, width=50)
        self.http_referer_entry.bind("<FocusOut>", self._on_field_change)
        self.http_referer_entry.bind("<KeyRelease>", self._on_field_change)

        self.x_title_label = ttk.Label(self.ai_frame, text=_("website_title"))
        self.x_title_entry = ttk.Entry(self.ai_frame, width=50)
        self.x_title_entry.bind("<FocusOut>", self._on_field_change)
        self.x_title_entry.bind("<KeyRelease>", self._on_field_change)

        self.http_referer_label.grid(row=3, column=0, padx=(0, 10), pady=8, sticky="w")
        self.http_referer_entry.grid(row=3, column=1, columnspan=2, padx=(0, 0), pady=8, sticky="ew")
        self.x_title_label.grid(row=4, column=0, padx=(0, 10), pady=8, sticky="w")
        self.x_title_entry.grid(row=4, column=1, columnspan=2, padx=(0, 0), pady=8, sticky="ew")

        # Initialize OpenRouter fields visibility (without saving)
        self.toggle_openrouter_fields(False)

        # Add some space at the bottom
        bottom_spacer = ttk.Frame(container)
        bottom_spacer.pack(fill="both", expand=True)

    def _on_field_change(self, event):
        """حفظ البيانات عند تغيير أي حقل"""
        # Only save if we have a current provider set
        if hasattr(self, 'current_provider'):
            self.save_current_provider_data()
            # Also save to file immediately for real-time persistence
            self.save_settings_to_file()
        
    def toggle_openrouter_fields(self, save_preference=True):
        """Show/hide OpenRouter specific fields based on provider selection and save/load data."""
        # Get the new provider
        new_provider = self.api_provider.get()

        # Save data for the previous provider (before switching)
        if hasattr(self, 'current_provider') and self.current_provider != new_provider:
            self.save_provider_data(self.current_provider)

        # Update current provider
        self.current_provider = new_provider
        is_openrouter = new_provider == "openrouter"

        # Save provider preference only if requested (avoid saving during initial load)
        if save_preference:
            self.save_provider_preference()

        # Show/hide OpenRouter specific fields
        widgets_to_toggle = [
            self.http_referer_label, self.http_referer_entry,
            self.x_title_label, self.x_title_entry
        ]
        for widget in widgets_to_toggle:
            if is_openrouter:
                widget.grid()
            else:
                widget.grid_remove()

        # Load data for the new provider
        self.load_provider_data(new_provider)

    def save_current_provider_data(self):
        """Save current form data to the current provider's storage."""
        self.save_provider_data(self.current_provider)

    def save_provider_data(self, provider):
        """Save current form data to the specified provider's storage."""
        if provider in self.provider_settings:
            self.provider_settings[provider]['api_key'] = self.api_key_entry.get()
            self.provider_settings[provider]['model'] = self.model_entry.get()
            self.provider_settings[provider]['http_referer'] = self.http_referer_entry.get()
            self.provider_settings[provider]['x_title'] = self.x_title_entry.get()

            # Save to file after updating data
            self.save_settings_to_file()

    def load_provider_data(self, provider):
        """Load data from provider's storage to the form."""
        if provider in self.provider_settings:
            settings = self.provider_settings[provider]

            # Clear and set API key
            self.api_key_entry.delete(0, tk.END)
            self.api_key_entry.insert(0, settings.get('api_key', ''))

            # Clear and set model
            self.model_entry.delete(0, tk.END)
            self.model_entry.insert(0, settings.get('model', 'gpt-4o'))

            # Clear and set OpenRouter fields
            self.http_referer_entry.delete(0, tk.END)
            self.http_referer_entry.insert(0, settings.get('http_referer', ''))

            self.x_title_entry.delete(0, tk.END)
            self.x_title_entry.insert(0, settings.get('x_title', ''))

    def load_saved_preferences(self):
        """Load saved preferences and apply them to the form."""
        # Load saved provider preference
        self.load_provider_preference()

        # Set provider in the UI
        self.api_provider.set(self.current_provider)

        # Load data for the current provider
        self.load_provider_data(self.current_provider)

        # Update OpenRouter fields visibility (without saving since we just loaded)
        is_openrouter = self.current_provider == "openrouter"
        widgets_to_toggle = [
            self.http_referer_label, self.http_referer_entry,
            self.x_title_label, self.x_title_entry
        ]
        for widget in widgets_to_toggle:
            if is_openrouter:
                widget.grid()
            else:
                widget.grid_remove()

    def get_data(self):
        """Get current settings from the form."""
        # Save current data before returning
        self.save_current_provider_data()
        # Also save to file to ensure persistence
        self.save_settings_to_file()

        current_provider = self.api_provider.get()
        return {
            'api_key': self.api_key_entry.get(),
            'model': self.model_entry.get(),
            'provider': current_provider,
            'http_referer': self.http_referer_entry.get() if current_provider == "openrouter" else None,
            'x_title': self.x_title_entry.get() if current_provider == "openrouter" else None,
        }
        
    def update_language(self):
        """Update all UI text when language changes."""
        self.ai_frame.config(text=_("ai_settings_frame"))
        self.provider_label.config(text=_("service_provider"))
        self.api_key_label.config(text=_("api_key"))
        self.model_label.config(text=_("model_name"))
        self.http_referer_label.config(text=_("website_referer"))
        self.x_title_label.config(text=_("website_title"))

    def save_settings_to_file(self):
        """Save provider settings using settings manager."""
        settings_manager.save_settings(self.settings_key, self.provider_settings)

    def load_settings_from_file(self):
        """Load provider settings using settings manager."""
        saved_settings = settings_manager.load_settings(self.settings_key, self.provider_settings)

        # Update provider settings with saved data
        for provider in self.provider_settings:
            if provider in saved_settings:
                self.provider_settings[provider].update(saved_settings[provider])

    def save_provider_preference(self):
        """Save current provider preference."""
        preferences = settings_manager.load_settings('app_preferences', {})
        preferences['selected_ai_provider'] = self.current_provider
        settings_manager.save_settings('app_preferences', preferences)

    def load_provider_preference(self):
        """Load saved provider preference."""
        preferences = settings_manager.load_settings('app_preferences', {})
        saved_provider = preferences.get('selected_ai_provider', 'openai')
        if saved_provider in self.provider_settings:
            self.current_provider = saved_provider
        else:
            self.current_provider = 'openai'
