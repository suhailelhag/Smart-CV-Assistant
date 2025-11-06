# ui/user_info_tab.py

import tkinter as tk
from tkinter import ttk, messagebox
from . import dialogs
from language import language_manager, _
from settings_manager import settings_manager

class UserInfoTab:
    def __init__(self, parent_tab, controller):
        """
        Creates all components inside the "Personal Information & Experience" tab.
        - parent_tab: The parent frame (tab) where these components will be placed.
        - controller: The object responsible for application logic.
        """
        self.parent = parent_tab
        self.controller = controller
        self.listboxes = {} # To store listboxes and facilitate access

        # Register for language change notifications
        language_manager.add_observer(self.update_language)

        # Load saved data
        self.load_saved_data()

        self.create_widgets()

        # Load data into widgets after creation
        self.populate_widgets_with_saved_data()

    def create_widgets(self):
        main_frame = ttk.Frame(self.parent, padding=10)
        main_frame.pack(fill="both", expand=True)
        main_frame.columnconfigure(1, weight=3)
        main_frame.columnconfigure(0, weight=2)

        # --- Left frame: for personal information and education ---
        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="ns")

        self.personal_frame = ttk.LabelFrame(left_frame, text=_("personal_info_frame"), padding=15)
        self.personal_frame.pack(fill="x", pady=5)
        self.personal_frame.columnconfigure(1, weight=1)

        # Store field labels for language updates
        self.field_labels = {}
        field_keys = ["full_name", "job_title", "email", "linkedin", "phone", "location"]
        field_attrs = ["name_entry", "title_entry", "email_entry", "linkedin_entry", "phone_entry", "location_entry"]

        for i, (key, attr) in enumerate(zip(field_keys, field_attrs)):
            label = ttk.Label(self.personal_frame, text=_(key))
            label.grid(row=i, column=0, sticky='w', padx=5, pady=5)
            self.field_labels[key] = label

            entry = ttk.Entry(self.personal_frame, width=40)
            entry.grid(row=i, column=1, sticky='ew', padx=5)
            entry.bind("<FocusOut>", self._on_personal_field_change)
            entry.bind("<KeyRelease>", self._on_personal_field_change)
            setattr(self, attr, entry)

        self.edu_frame = ttk.LabelFrame(left_frame, text=_("education_frame"), padding=15)
        self.edu_frame.pack(fill="x", pady=10)
        self.edu_frame.columnconfigure(1, weight=1)

        self.university_label = ttk.Label(self.edu_frame, text=_("university"))
        self.university_label.grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.university_entry = ttk.Entry(self.edu_frame, width=40)
        self.university_entry.grid(row=0, column=1, sticky='ew', padx=5)
        self.university_entry.bind("<FocusOut>", self._on_personal_field_change)
        self.university_entry.bind("<KeyRelease>", self._on_personal_field_change)

        self.degree_label = ttk.Label(self.edu_frame, text=_("degree"))
        self.degree_label.grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.degree_entry = ttk.Entry(self.edu_frame, width=40)
        self.degree_entry.grid(row=1, column=1, sticky='ew', padx=5)
        self.degree_entry.bind("<FocusOut>", self._on_personal_field_change)
        self.degree_entry.bind("<KeyRelease>", self._on_personal_field_change)

        # --- Right frame: for experiences, certifications and languages ---
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=0, column=1, padx=(10, 0), pady=5, sticky="nsew")

        lists_frame = ttk.Frame(right_frame)
        lists_frame.pack(fill="both", expand=True)
        lists_frame.rowconfigure(0, weight=1)
        lists_frame.rowconfigure(1, weight=1)
        lists_frame.rowconfigure(2, weight=1)
        lists_frame.columnconfigure(0, weight=1)

        self.create_list_management_ui(lists_frame, "work_experience", "experiences", row=0)
        self.create_list_management_ui(lists_frame, "certifications", "certifications", row=1)
        self.create_list_management_ui(lists_frame, "languages", "languages", row=2)

    def create_list_management_ui(self, parent, title_key, key, row=0):
        frame = ttk.LabelFrame(parent, text=_(title_key), padding=10)
        frame.grid(row=row, column=0, sticky="nsew", padx=5, pady=5)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        list_container = ttk.Frame(frame)
        list_container.pack(fill='x', expand=True)
        list_container.columnconfigure(0, weight=1)

        listbox = tk.Listbox(list_container, height=4, borderwidth=0, highlightthickness=0)
        listbox.grid(row=0, column=0, sticky='nsew')
        self.listboxes[key] = listbox

        scrollbar = ttk.Scrollbar(list_container, orient='vertical', command=listbox.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        listbox['yscrollcommand'] = scrollbar.set

        listbox.bind("<Double-1>", lambda event, k=key: self.edit_item(k))

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=(10, 0))

        add_btn = ttk.Button(btn_frame, text=_("add_button"))
        add_btn.config(command=lambda k=key, b=add_btn: self.add_item(k, b))
        add_btn.pack(side="left", expand=True, fill="x", padx=(0, 5))

        del_btn = ttk.Button(btn_frame, text=_("delete_button"), command=lambda k=key: self.delete_item(k))
        del_btn.pack(side="left", expand=True, fill="x", padx=(5, 0))

        # Store references for language updates
        if not hasattr(self, 'list_frames'):
            self.list_frames = {}

        self.list_frames[key] = {
            'frame': frame,
            'title_key': title_key,
            'add_btn': add_btn,
            'del_btn': del_btn
        }

    def refresh_listbox(self, key):
        listbox = self.listboxes[key]
        data_list = self.controller.user_data[key]
        
        listbox.delete(0, tk.END)
        for item in data_list:
            if key == "experiences":
                display_text = f"{item['position']} في {item['company']}"
            elif key == "certifications":
                display_text = f"{item['name']} - {item['authority']}"
            elif key == "languages":
                # Convert proficiency level from English to current language for display
                proficiency_map = language_manager.get_proficiency_reverse_map()
                if language_manager.get_current_language() == "ar":
                    proficiency_display = proficiency_map.get(item['proficiency'], item['proficiency'])
                else:
                    proficiency_display = item['proficiency']
                display_text = f"{item['name']} ({proficiency_display})"
            listbox.insert(tk.END, display_text)

    def add_item(self, key, button_widget):
        if key == "experiences": dialogs.experience_dialog(self.parent, self.controller, button_widget=button_widget)
        elif key == "certifications": dialogs.certification_dialog(self.parent, self.controller, button_widget=button_widget)
        elif key == "languages": dialogs.language_dialog(self.parent, self.controller, button_widget=button_widget)

        # Save data after adding item
        self.save_user_lists()

    def edit_item(self, key):
        listbox = self.listboxes[key]
        selected_indices = listbox.curselection()
        if not selected_indices: return
        index = selected_indices[0]

        if key == "experiences": dialogs.experience_dialog(self.parent, self.controller, index)
        elif key == "certifications": dialogs.certification_dialog(self.parent, self.controller, index)
        elif key == "languages": dialogs.language_dialog(self.parent, self.controller, index)

        # Save data after editing item
        self.save_user_lists()

    def delete_item(self, key):
        listbox = self.listboxes[key]
        selected_indices = listbox.curselection()
        if not selected_indices:
            messagebox.showwarning(_("warning"), _("select_item_to_delete"), parent=self.parent)
            return

        self.controller.delete_item(key, selected_indices[0])

        # Save data after deleting item
        self.save_user_lists()

    def get_data(self):
        """Collects data from input fields in this tab."""
        return {
            'name': self.name_entry.get(),
            'title': self.title_entry.get(),
            'email': self.email_entry.get(),
            'linkedin': self.linkedin_entry.get(),
            'phone': self.phone_entry.get(),
            'location': self.location_entry.get(),
            'university': self.university_entry.get(),
            'degree': self.degree_entry.get()
        }

    def update_language(self):
        """Update all UI text when language changes."""
        # Update frame titles
        self.personal_frame.config(text=_("personal_info_frame"))
        self.edu_frame.config(text=_("education_frame"))

        # Update field labels
        for key, label in self.field_labels.items():
            label.config(text=_(key))

        # Update education labels
        self.university_label.config(text=_("university"))
        self.degree_label.config(text=_("degree"))

        # Update list management frames
        if hasattr(self, 'list_frames'):
            for key, frame_info in self.list_frames.items():
                frame_info['frame'].config(text=_(frame_info['title_key']))
                frame_info['add_btn'].config(text=_("add_button"))
                frame_info['del_btn'].config(text=_("delete_button"))

        # Refresh listboxes to update language-dependent content
        for key in self.listboxes.keys():
            self.refresh_listbox(key)

    def _on_personal_field_change(self, event):
        """حفظ البيانات الشخصية عند تغيير أي حقل"""
        self.save_personal_info()

    def load_saved_data(self):
        """Load saved personal information data."""
        # Load personal info
        self.saved_personal_info = settings_manager.load_settings('personal_info', {
            'name': '', 'title': '', 'email': '', 'linkedin': '', 'phone': '', 'location': '',
            'university': '', 'degree': ''
        })

        # Load experiences, certifications, and languages
        self.saved_experiences = settings_manager.load_settings('user_experiences', [])
        self.saved_certifications = settings_manager.load_settings('user_certifications', [])
        self.saved_languages = settings_manager.load_settings('user_languages', [])

    def populate_widgets_with_saved_data(self):
        """Populate widgets with saved data after they are created."""
        # Populate personal info fields
        for key, value in self.saved_personal_info.items():
            if hasattr(self, f'{key}_entry') and value:
                entry = getattr(self, f'{key}_entry')
                entry.delete(0, tk.END)
                entry.insert(0, value)

        # Update controller data
        self.controller.user_data.update({
            'experiences': self.saved_experiences,
            'certifications': self.saved_certifications,
            'languages': self.saved_languages
        })

        # Refresh listboxes to show saved data
        for key in ['experiences', 'certifications', 'languages']:
            if key in self.listboxes:
                self.refresh_listbox(key)

    def save_personal_info(self):
        """Save personal information data."""
        personal_data = self.get_personal_data()
        settings_manager.save_settings('personal_info', personal_data)

    def save_user_lists(self):
        """Save user lists (experiences, certifications, languages)."""
        settings_manager.save_settings('user_experiences', self.controller.user_data.get('experiences', []))
        settings_manager.save_settings('user_certifications', self.controller.user_data.get('certifications', []))
        settings_manager.save_settings('user_languages', self.controller.user_data.get('languages', []))

    def get_personal_data(self):
        """Get current personal information from form fields."""
        return {
            'name': getattr(self, 'name_entry', tk.Entry()).get(),
            'title': getattr(self, 'title_entry', tk.Entry()).get(),
            'email': getattr(self, 'email_entry', tk.Entry()).get(),
            'linkedin': getattr(self, 'linkedin_entry', tk.Entry()).get(),
            'phone': getattr(self, 'phone_entry', tk.Entry()).get(),
            'location': getattr(self, 'location_entry', tk.Entry()).get(),
            'university': getattr(self, 'university_entry', tk.Entry()).get(),
            'degree': getattr(self, 'degree_entry', tk.Entry()).get()
        }
