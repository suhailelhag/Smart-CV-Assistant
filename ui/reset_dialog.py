# ui/reset_dialog.py
# نافذة حوار إعادة التعيين المتقدمة

import tkinter as tk
from tkinter import ttk, messagebox
from language import language_manager, _
from path_utils import resource_path

class ResetDialog:
    """نافذة حوار لاختيار العناصر المراد إعادة تعيينها"""
    
    def __init__(self, parent, button_widget):
        self.parent = parent
        self.result = None
        
        # إنشاء النافذة
        self.window = tk.Toplevel(parent)
        self.window.withdraw()  # <-- إخفاء النافذة فوراً هنا
        self.window.title(_("reset_dialog_title"))
        try:
            # أضف هذا السطر هنا
            self.window.iconbitmap(resource_path("icon/icon.ico"))
        except tk.TclError:
            pass
        self.window.geometry("500x600")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()
        
        # وضع النافذة تحت الزر
        self.position_window(button_widget)
        
        # متغيرات الاختيار
        self.reset_options = {
            'personal_info': tk.BooleanVar(),
            'experiences': tk.BooleanVar(),
            'certifications': tk.BooleanVar(),
            'languages': tk.BooleanVar(),
            'section_names': tk.BooleanVar(),
            'section_order': tk.BooleanVar(),
            'ai_providers': tk.BooleanVar(),
            'app_preferences': tk.BooleanVar(),  # خيار رئيسي
            'language_preference': tk.BooleanVar(),  # خيار فرعي
            'provider_preference': tk.BooleanVar(),  # خيار فرعي
            'all': tk.BooleanVar()
        }
        
        self.create_widgets()
        
        # ربط إغلاق النافذة
        self.window.protocol("WM_DELETE_WINDOW", self.on_cancel)
        
    def position_window(self, button_widget):
        """Positions the dialog window below the specified button."""
        self.window.update_idletasks()  # Update window to get correct dimensions

        button_x = button_widget.winfo_rootx()
        button_y = button_widget.winfo_rooty()
        button_height = button_widget.winfo_height()

        # Position the dialog below the button
        x = button_x
        y = button_y + button_height + 5  # 5 pixels of padding

        self.window.geometry(f"+{x}+{y}")
        self.window.deiconify() # <-- إظهار النافذة هنا بعد تحديد مكانها

        
    def create_widgets(self):
        # الإطار الرئيسي
        main_frame = ttk.Frame(self.window, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # العنوان والوصف
        title_label = ttk.Label(main_frame, text=_("reset_dialog_title"), 
                               font=("Arial", 12, "bold"))
        title_label.pack(pady=(0, 10))
        
        desc_label = ttk.Label(main_frame, text=_("reset_dialog_description"), 
                              wraplength=450, justify="center")
        desc_label.pack(pady=(0, 20))
        
        # إطار الخيارات
        options_frame = ttk.LabelFrame(main_frame, text=_("reset_options"), padding=15)
        options_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # خيار إعادة تعيين الكل
        self.all_checkbox = ttk.Checkbutton(
            options_frame, 
            text=_("reset_all"), 
            variable=self.reset_options['all'],
            command=self.on_all_changed
        )
        self.all_checkbox.pack(anchor="w", pady=(0, 15))
        
        # فاصل
        separator = ttk.Separator(options_frame, orient="horizontal")
        separator.pack(fill="x", pady=(0, 15))
        
        # خيارات فردية
        individual_frame = ttk.LabelFrame(options_frame, text=_("individual_options"), padding=10)
        individual_frame.pack(fill="both", expand=True)
        
        # المعلومات الشخصية
        personal_frame = ttk.Frame(individual_frame)
        personal_frame.pack(fill="x", pady=2)
        
        self.personal_checkbox = ttk.Checkbutton(
            personal_frame,
            text=_("reset_personal_info"),
            variable=self.reset_options['personal_info'],
            command=self.on_individual_changed
        )
        self.personal_checkbox.pack(side="left")
        
        # الخبرات
        exp_frame = ttk.Frame(individual_frame)
        exp_frame.pack(fill="x", pady=2)
        
        self.exp_checkbox = ttk.Checkbutton(
            exp_frame,
            text=_("reset_experiences"),
            variable=self.reset_options['experiences'],
            command=self.on_individual_changed
        )
        self.exp_checkbox.pack(side="left")
        
        # الشهادات
        cert_frame = ttk.Frame(individual_frame)
        cert_frame.pack(fill="x", pady=2)
        
        self.cert_checkbox = ttk.Checkbutton(
            cert_frame,
            text=_("reset_certifications"),
            variable=self.reset_options['certifications'],
            command=self.on_individual_changed
        )
        self.cert_checkbox.pack(side="left")
        
        # اللغات
        lang_frame = ttk.Frame(individual_frame)
        lang_frame.pack(fill="x", pady=2)
        
        self.lang_checkbox = ttk.Checkbutton(
            lang_frame,
            text=_("reset_languages"),
            variable=self.reset_options['languages'],
            command=self.on_individual_changed
        )
        self.lang_checkbox.pack(side="left")
        
        # أسماء الأقسام
        sections_frame = ttk.Frame(individual_frame)
        sections_frame.pack(fill="x", pady=2)
        
        self.sections_checkbox = ttk.Checkbutton(
            sections_frame,
            text=_("reset_section_names"),
            variable=self.reset_options['section_names'],
            command=self.on_individual_changed
        )
        self.sections_checkbox.pack(side="left")
        
        # ترتيب الأقسام
        order_frame = ttk.Frame(individual_frame)
        order_frame.pack(fill="x", pady=2)
        
        self.order_checkbox = ttk.Checkbutton(
            order_frame,
            text=_("reset_section_order"),
            variable=self.reset_options['section_order'],
            command=self.on_individual_changed
        )
        self.order_checkbox.pack(side="left")
        
        # إعدادات مزودي الذكاء الاصطناعي
        ai_frame = ttk.Frame(individual_frame)
        ai_frame.pack(fill="x", pady=2)
        
        self.ai_checkbox = ttk.Checkbutton(
            ai_frame,
            text=_("reset_ai_providers"),
            variable=self.reset_options['ai_providers'],
            command=self.on_individual_changed
        )
        self.ai_checkbox.pack(side="left")
        
        # تفضيلات التطبيق (خيار رئيسي)
        prefs_main_frame = ttk.Frame(individual_frame)
        prefs_main_frame.pack(fill="x", pady=2)

        self.prefs_checkbox = ttk.Checkbutton(
            prefs_main_frame,
            text=_("reset_app_preferences"),
            variable=self.reset_options['app_preferences'],
            command=self.on_app_preferences_changed
        )
        self.prefs_checkbox.pack(side="left")

        # إطار الخيارات الفرعية لتفضيلات التطبيق
        self.prefs_sub_frame = ttk.Frame(individual_frame)
        self.prefs_sub_frame.pack(fill="x", padx=(20, 0), pady=(2, 5))

        # خيار اللغة (فرعي)
        lang_pref_frame = ttk.Frame(self.prefs_sub_frame)
        lang_pref_frame.pack(fill="x", pady=1)

        self.lang_pref_checkbox = ttk.Checkbutton(
            lang_pref_frame,
            text=_("reset_language_preference"),
            variable=self.reset_options['language_preference'],
            command=self.on_sub_preference_changed
        )
        self.lang_pref_checkbox.pack(side="left")

        # خيار مزود الخدمة (فرعي)
        provider_pref_frame = ttk.Frame(self.prefs_sub_frame)
        provider_pref_frame.pack(fill="x", pady=1)

        self.provider_pref_checkbox = ttk.Checkbutton(
            provider_pref_frame,
            text=_("reset_provider_preference"),
            variable=self.reset_options['provider_preference'],
            command=self.on_sub_preference_changed
        )
        self.provider_pref_checkbox.pack(side="left")
        
        # إطار الأزرار
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill="x")
        
        # زر الإلغاء
        self.cancel_button = ttk.Button(buttons_frame, text=_("cancel"), command=self.on_cancel)
        self.cancel_button.pack(side="right", padx=(10, 0))
        
        # زر إعادة التعيين
        self.reset_button = ttk.Button(buttons_frame, text=_("reset"), command=self.on_reset, 
                                      style="Accent.TButton")
        self.reset_button.pack(side="right")
        
    def on_all_changed(self):
        """عند تغيير خيار 'إعادة تعيين الكل'"""
        all_selected = self.reset_options['all'].get()

        # تعيين جميع الخيارات الفردية
        for key in self.reset_options:
            if key != 'all':
                self.reset_options[key].set(all_selected)

        # تحديث حالة الخيارات الفرعية
        self.update_sub_preferences_state()
                
    def on_individual_changed(self):
        """عند تغيير أي خيار فردي"""
        # التحقق من تحديد جميع الخيارات الفردية (باستثناء الخيارات الفرعية)
        main_options = [key for key in self.reset_options.keys()
                       if key not in ['all', 'language_preference', 'provider_preference']]

        all_individual_selected = all(
            self.reset_options[key].get()
            for key in main_options
        )

        # تحديث خيار 'إعادة تعيين الكل'
        self.reset_options['all'].set(all_individual_selected)

    def on_app_preferences_changed(self):
        """عند تغيير خيار تفضيلات التطبيق الرئيسي"""
        app_prefs_selected = self.reset_options['app_preferences'].get()

        # تعيين الخيارات الفرعية حسب الخيار الرئيسي
        self.reset_options['language_preference'].set(app_prefs_selected)
        self.reset_options['provider_preference'].set(app_prefs_selected)

        # تحديث حالة الخيارات الفرعية
        self.update_sub_preferences_state()

        # تحديث خيار "إعادة تعيين الكل"
        self.on_individual_changed()

    def on_sub_preference_changed(self):
        """عند تغيير أي خيار فرعي لتفضيلات التطبيق"""
        # التحقق من حالة الخيارات الفرعية
        lang_selected = self.reset_options['language_preference'].get()
        provider_selected = self.reset_options['provider_preference'].get()

        # تحديث الخيار الرئيسي حسب الخيارات الفرعية
        if lang_selected and provider_selected:
            # إذا كانت جميع الخيارات الفرعية محددة، حدد الخيار الرئيسي
            self.reset_options['app_preferences'].set(True)
        elif not lang_selected and not provider_selected:
            # إذا لم تكن أي خيارات فرعية محددة، ألغ تحديد الخيار الرئيسي
            self.reset_options['app_preferences'].set(False)
        # إذا كان بعض الخيارات محدد، اترك الخيار الرئيسي كما هو

        # تحديث خيار "إعادة تعيين الكل"
        self.on_individual_changed()

    def update_sub_preferences_state(self):
        """تحديث حالة تفعيل/تعطيل الخيارات الفرعية"""
        # يمكن دائماً تعديل الخيارات الفرعية
        self.lang_pref_checkbox.config(state="normal")
        self.provider_pref_checkbox.config(state="normal")
        
    def on_reset(self):
        """عند الضغط على زر إعادة التعيين"""
        # التحقق من تحديد خيار واحد على الأقل
        any_selected = any(self.reset_options[key].get() for key in self.reset_options)
        
        if not any_selected:
            messagebox.showwarning(
                _("warning"), 
                _("reset_no_selection_warning"), 
                parent=self.window
            )
            return
            
        # تأكيد العملية
        selected_items = []
        for key, var in self.reset_options.items():
            if var.get() and key not in ['all', 'app_preferences']:
                selected_items.append(_(f"reset_{key}"))
            elif key == 'app_preferences' and var.get():
                # إذا كان الخيار الرئيسي محدد، أضف الخيارات الفرعية المحددة
                if self.reset_options['language_preference'].get():
                    selected_items.append(_("reset_language_preference"))
                if self.reset_options['provider_preference'].get():
                    selected_items.append(_("reset_provider_preference"))
        
        confirmation_text = _("reset_confirmation") + "\n\n" + "\n".join(f"• {item}" for item in selected_items)
        
        if messagebox.askyesno(
            _("confirm_reset"), 
            confirmation_text, 
            parent=self.window
        ):
            # إرجاع النتيجة (استبعاد الخيار الرئيسي للتفضيلات وإبقاء الفرعية)
            self.result = {}
            for key, var in self.reset_options.items():
                if key not in ['all', 'app_preferences']:
                    self.result[key] = var.get()

            self.window.destroy()
            
    def on_cancel(self):
        """عند الضغط على زر الإلغاء أو إغلاق النافذة"""
        self.result = None
        self.window.destroy()
