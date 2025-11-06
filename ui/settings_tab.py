# ui/settings_tab.py

import tkinter as tk
from tkinter import ttk
import re
from language import language_manager, _
from settings_manager import settings_manager


class SettingsTab:
    def __init__(self, parent_tab, controller):
        """
        Creates all components inside the "Job Description & Settings" tab.
        - parent_tab: The parent frame (tab) where these components will be placed.
        - controller: The object responsible for application logic.
        """
        self.parent = parent_tab
        self.controller = controller
        self.list_section_entries = []
        self.text_has_focus = False  # Variable to track focus on job description section

        # Load saved section names
        self.saved_section_names = settings_manager.load_settings('section_names', {
            'profile': 'Profile Summary'
        })

        # Register for language change notifications
        language_manager.add_observer(self.update_language)

        self.create_widgets()

    def create_widgets(self):
        # --- الإطار الرئيسي مع هوامش داخلية ---
        container = ttk.Frame(self.parent, padding=10)
        container.pack(fill="both", expand=True)


        def on_container_resize(event):
            width = event.width
            padding_size = max(5, min(width // 20, 30))
            container['padding'] = padding_size

        container.bind('<Configure>', on_container_resize)


        # إنشاء Canvas مع Scrollbar للمحتوى القابل للتمرير
        self.canvas = tk.Canvas(container, borderwidth=0, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # إنشاء النافذة مع ملء العرض الكامل
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # ربط تغيير حجم Canvas لتحديث عرض المحتوى
        self.canvas.bind('<Configure>', self._on_canvas_configure)

        # تخطيط Canvas و Scrollbar
        self.canvas.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self.scrollbar.pack(side="right", fill="y")

        # ربط عجلة الماوس بالتمرير
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.scrollable_frame.bind("<MouseWheel>", self._on_mousewheel)

        # --- المحتوى داخل الإطار القابل للتمرير ---
        
        # --- Job Description Section ---
        self.job_frame = ttk.LabelFrame(self.scrollable_frame, text=_("job_description_frame"), padding=15)
        self.job_frame.pack(padx=10, pady=10, fill="x")
        self.job_frame.columnconfigure(0, weight=1)

        self.job_desc_text = tk.Text(self.job_frame, wrap="word", height=8, borderwidth=0, highlightthickness=1)
        self.job_desc_text.grid(row=0, column=0, sticky="ew")

        job_scrollbar = ttk.Scrollbar(self.job_frame, orient="vertical", command=self.job_desc_text.yview)
        job_scrollbar.grid(row=0, column=1, sticky="ns")
        self.job_desc_text.config(yscrollcommand=job_scrollbar.set)

        # ربط أحداث التركيز والماوس لقسم الوصف الوظيفي
        self.job_desc_text.bind("<FocusIn>", self._on_text_focus_in)
        self.job_desc_text.bind("<FocusOut>", self._on_text_focus_out)
        self.job_desc_text.bind("<Enter>", self._on_text_enter)
        self.job_desc_text.bind("<Leave>", self._on_text_leave)
        self.job_desc_text.bind("<MouseWheel>", self._on_text_mousewheel)

        # --- AI Settings Section (Basic) ---
        self.ai_frame = ttk.LabelFrame(self.scrollable_frame, text=_("ai_settings_frame"), padding=15)
        self.ai_frame.pack(padx=10, pady=10, fill="x")
        self.ai_frame.columnconfigure(1, weight=1)

        # Excluded words (kept in main settings)
        self.excluded_label = ttk.Label(self.ai_frame, text=_("excluded_words"))
        self.excluded_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.excluded_entry = ttk.Entry(self.ai_frame, width=50)
        self.excluded_entry.grid(row=0, column=1, columnspan=2, padx=5, sticky="ew")

        # --- Section Name Customization ---
        self.customization_frame = ttk.LabelFrame(self.scrollable_frame, text=_("section_customization"), padding=15)
        self.customization_frame.pack(padx=10, pady=10, fill="x")
        self.customization_frame.columnconfigure(1, weight=1)

        self.profile_label = ttk.Label(self.customization_frame, text=_("profile_section_title"))
        self.profile_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.profile_section_entry = ttk.Entry(self.customization_frame, width=40)
        self.profile_section_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.profile_section_entry.insert(0, self.saved_section_names.get('profile', 'Profile Summary'))
        self.profile_section_entry.bind("<FocusOut>", self._on_section_change)
        self.profile_section_entry.bind("<KeyRelease>", self._on_section_change)

        self.sections_container = ttk.Frame(self.customization_frame)
        self.sections_container.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10)
        self.sections_container.columnconfigure(1, weight=1)

        # Load saved sections or add default ones
        self._load_saved_sections()

        self.add_section_button = ttk.Button(self.customization_frame, text=_("add_new_section"), command=self._add_list_section_row)
        self.add_section_button.grid(row=2, column=1, pady=10, sticky="e")

    def _on_mousewheel(self, event):
        """التعامل مع تمرير عجلة الماوس للصفحة الرئيسية"""
        # إذا كان التركيز على قسم الوصف الوظيفي، لا تتعامل مع الحدث
        if not self.text_has_focus:
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _on_canvas_configure(self, event):
        """تحديث عرض المحتوى عند تغيير حجم Canvas"""
        # تحديث عرض scrollable_frame ليطابق عرض Canvas
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)

    def _on_text_focus_in(self, event):
        """عند التركيز على قسم الوصف الوظيفي"""
        self.text_has_focus = True

    def _on_text_focus_out(self, event):
        """عند فقدان التركيز من قسم الوصف الوظيفي"""
        self.text_has_focus = False

    def _on_text_enter(self, event):
        """عند دخول الماوس إلى قسم الوصف الوظيفي"""
        self.text_has_focus = True

    def _on_text_leave(self, event):
        """عند خروج الماوس من قسم الوصف الوظيفي"""
        # التحقق من أن المؤشر ليس في منطقة النص قبل إزالة التركيز
        if not self.job_desc_text.focus_get() == self.job_desc_text:
            self.text_has_focus = False

    def _on_text_mousewheel(self, event):
        """التعامل مع عجلة الماوس داخل قسم الوصف الوظيفي"""
        # التمرير داخل النص
        self.job_desc_text.yview_scroll(int(-1*(event.delta/120)), "units")
        # منع انتشار الحدث للعناصر الأخرى
        return "break"

    def _load_saved_sections(self):
        """Load saved sections or add default ones."""
        sections_added = False

        # Add saved sections (excluding 'profile' which is handled separately)
        for key, value in self.saved_section_names.items():
            if key != 'profile' and value:
                self._add_list_section_row(value)
                sections_added = True

        # If no sections were loaded, add default ones
        if not sections_added:
            self._add_list_section_row("Skills")
            self._add_list_section_row("Interests")


    def _on_section_change(self, event):
        """حفظ أسماء الأقسام عند تغيير أي حقل"""
        self.save_section_names()

    def _add_list_section_row(self, default_text=""):
        row_frame = ttk.Frame(self.sections_container)
        row_frame.pack(fill="x", pady=3)
        row_frame.columnconfigure(1, weight=1)

        section_label = ttk.Label(row_frame, text=_("section_title"))
        section_label.grid(row=0, column=0, padx=(0, 10), sticky="w")

        entry = ttk.Entry(row_frame, width=38)
        entry.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        entry.bind("<FocusOut>", self._on_section_change)
        entry.bind("<KeyRelease>", self._on_section_change)
        if default_text:
            entry.insert(0, default_text)

        delete_button = ttk.Button(row_frame, text="➖", width=3, style="Danger.TButton", command=lambda: self._delete_list_section_row(row_frame, entry))
        delete_button.grid(row=0, column=2, sticky="e")

        self.list_section_entries.append(entry)

        # Store reference for language updates
        if not hasattr(self, 'section_labels'):
            self.section_labels = []
        self.section_labels.append(section_label)


    def _delete_list_section_row(self, row_frame, entry):
        if entry in self.list_section_entries:
            self.list_section_entries.remove(entry)
        row_frame.destroy()
        # Save section names after deletion
        self.save_section_names()

    def save_section_names(self):
        """Save section names to settings."""
        sections = {
            'profile': self.profile_section_entry.get() or "Profile Summary"
        }

        for entry in self.list_section_entries:
            value = entry.get().strip()
            if value:
                key = re.sub(r'\s+', '_', value.lower())
                key = re.sub(r'[^a-z0-9_]', '', key)
                sections[key] = value

        settings_manager.save_settings('section_names', sections)




    def get_data(self):
        sections = {
            'profile': self.profile_section_entry.get() or "Profile Summary"
        }

        for entry in self.list_section_entries:
            value = entry.get().strip()
            if value:
                key = re.sub(r'\s+', '_', value.lower())
                key = re.sub(r'[^a-z0-9_]', '', key)
                sections[key] = value

        # Get AI settings from the AI settings tab
        ai_data = {}
        if hasattr(self.controller, 'ai_settings_tab'):
            ai_data = self.controller.ai_settings_tab.get_data()

        return {
            'job_desc': self.job_desc_text.get("1.0", tk.END).strip(),
            'api_key': ai_data.get('api_key', ''),
            'model': ai_data.get('model', 'gpt-4o'),
            'excluded_terms': [t.strip() for t in self.excluded_entry.get().split(',') if t.strip()],
            'provider': ai_data.get('provider', 'openai'),
            'http_referer': ai_data.get('http_referer') if ai_data.get('provider') == "openrouter" else None,
            'x_title': ai_data.get('x_title') if ai_data.get('provider') == "openrouter" else None,
            'section_names': sections
        }

    def update_language(self):
        """Update all UI text when language changes."""
        # Update frame titles
        self.job_frame.config(text=_("job_description_frame"))
        self.ai_frame.config(text=_("ai_settings_frame"))
        self.customization_frame.config(text=_("section_customization"))

        # Update AI settings labels
        self.excluded_label.config(text=_("excluded_words"))

        # Update customization labels
        self.profile_label.config(text=_("profile_section_title"))
        self.add_section_button.config(text=_("add_new_section"))

        # Update section labels
        if hasattr(self, 'section_labels'):
            for label in self.section_labels:
                label.config(text=_("section_title"))