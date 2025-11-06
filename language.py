# language.py

import json
import os

class LanguageManager:
    """
    Manages language translations and switching between Arabic and English.
    Provides a centralized system for all UI text translations.
    """
    
    def __init__(self):
        self.current_language = "ar"  # Default to Arabic
        self.translations = self._load_translations()
        self.observers = []  # List of callbacks to notify when language changes

        # Load saved language preference
        self._load_saved_language()
    
    def _load_translations(self):
        """Load all translations for both languages."""
        return {
            "ar": {
                # Main Window
                "app_title": "مساعد السيرة الذاتية الذكي",
                "generate_cv_button": "🚀 إنشاء السيرة الذاتية الآن",
                "reorder_sections_button": "ترتيب الأقسام",
                "tab_personal_info": "المعلومات الشخصية والخبرات",
                "tab_job_settings": "الوصف الوظيفي والإعدادات",
                "tab_templates": "قوالب السيرة الذاتية",
                "tab_ai_settings": "إعدادات الذكاء الاصطناعي",
                "language_switch_button": "English",
                "about_button": "حول البرنامج",
                
                # Personal Info Tab
                "personal_info_frame": "المعلومات الشخصية",
                "full_name": "الاسم الكامل:",
                "job_title": "المسمى الوظيفي:",
                "email": "البريد الإلكتروني:",
                "linkedin": "رابط LinkedIn:",
                "phone": "رقم الهاتف:",
                "location": "مكان الإقامة:",
                "education_frame": "التعليم",
                "university": "الجامعة:",
                "degree": "الدرجة العلمية:",
                "work_experience": "الخبرات العملية",
                "certifications": "الشهادات والدورات",
                "languages": "اللغات",
                "add_button": "إضافة",
                "edit_button": "تعديل",
                "delete_button": "حذف",
                
                # Settings Tab
                "job_description_frame": "الوصف الوظيفي (Job Description)",
                "ai_settings_frame": "إعدادات الذكاء الاصطناعي",
                "open_ai_settings": "فتح إعدادات الذكاء الاصطناعي",
                "ai_settings_window_title": "إعدادات الذكاء الاصطناعي",
                "service_provider": "مزود الخدمة:",
                "api_key": "مفتاح API:",
                "model_name": "اسم النموذج (Model):",
                "website_referer": "رابط موقعك (Referer):",
                "website_title": "اسم موقعك (Title):",
                "excluded_words": "كلمات مستبعدة (بفاصلة):",
                "save": "حفظ",
                "cancel": "إلغاء",

                # Reset Dialog
                "reset": "إعادة تعيين",
                "reset_dialog_title": "إعادة تعيين البيانات",
                "reset_dialog_description": "اختر العناصر التي تريد إعادة تعيينها إلى القيم الافتراضية",
                "reset_options": "خيارات إعادة التعيين",
                "reset_all": "إعادة تعيين جميع البيانات",
                "individual_options": "خيارات فردية",
                "reset_personal_info": "المعلومات الشخصية والتعليم",
                "reset_experiences": "الخبرات العملية",
                "reset_certifications": "الشهادات",
                "reset_languages": "اللغات",
                "reset_section_names": "أسماء الأقسام المخصصة",
                "reset_section_order": "ترتيب الأقسام",
                "reset_ai_providers": "إعدادات مزودي الذكاء الاصطناعي",
                "reset_app_preferences": "تفضيلات التطبيق",
                "reset_language_preference": "إعادة تعيين اللغة إلى العربية",
                "reset_provider_preference": "إعادة تعيين مزود الخدمة إلى OpenAI",
                "reset_no_selection_warning": "يرجى اختيار عنصر واحد على الأقل لإعادة تعيينه",
                "reset_confirmation": "هل أنت متأكد من إعادة تعيين العناصر التالية؟",
                "confirm_reset": "تأكيد إعادة التعيين",
                "reset_success": "تم إعادة تعيين البيانات المحددة بنجاح",
                "reset_button": "إعادة تعيين البيانات",
                "section_customization": "تخصيص أسماء الأقسام",
                "profile_section_title": "عنوان قسم الملخص:",
                "section_title": "عنوان القسم:",
                "add_new_section": "➕ إضافة قسم جديد",

                # Template Tab
                "template_selection_frame": "اختيار قالب السيرة الذاتية",
                "template_modern_name": "التصميم الحديث",
                "template_modern_desc": "تصميم عصري وأنيق، مثالي للمجالات الإبداعية والتكنولوجية.",
                "template_professional_name": "التصميم الاحترافي",
                "template_professional_desc": "تصميم كلاسيكي وواضح، مناسب للتقديمات الرسمية والشركات الكبرى.",
                "template_preview": "معاينة القالب",
                
                # Dialogs
                "add_certification": "إضافة شهادة",
                "edit_certification": "تعديل شهادة",
                "certification_name": "اسم الشهادة:",
                "issuing_authority": "الجهة المانحة:",
                "add_language": "إضافة لغة",
                "edit_language": "تعديل لغة",
                "language": "اللغة:",
                "proficiency_level": "مستوى الإتقان:",
                "add_experience": "إضافة خبرة",
                "edit_experience": "تعديل خبرة",
                "job_position": "المسمى الوظيفي",
                "company_name": "اسم الشركة",
                "duration": "المدة",
                "tasks_comma_separated": "المهام (بفاصلة)",
                "save_button": "حفظ",
                "cancel_button": "إلغاء",
                
                # Proficiency Levels
                "beginner": "مبتدئ",
                "intermediate": "متوسط",
                "advanced": "متقدم",
                "native": "لغة أم",
                
                # Reorder Dialog
                "reorder_dialog_title": "تخصيص ترتيب الأقسام",
                "reorder_instructions": "استخدم الأسهم لترتيب الأقسام:",
                "move_up": "▲ للأعلى",
                "move_down": "▼ للأسفل",
                "save_order": "حفظ الترتيب",
                
                # Messages
                "error": "خطأ",
                "success": "نجاح",
                "warning": "تنبيه",
                "working": "جاري العمل",
                "fill_all_fields": "يرجى ملء جميع الحقول.",
                "fill_required_fields": "يرجى ملء الحقول الأساسية: الاسم، مفتاح API، النموذج، والوصف الوظيفي.",
                "position_company_required": "المسمى الوظيفي واسم الشركة حقول إلزامية.",
                "select_item_to_delete": "يرجى تحديد عنصر لحذفه.",
                "analyzing_job_description": "جاري تحليل الوصف الوظيفي... قد يستغرق الأمر بعض الوقت.",
                "api_error": "خطأ من الـ API",
                "api_client_error": "حدث خطأ عند تهيئة العميل: {error}",
                "write_error": "خطأ في الكتابة",
                "save_failed": "فشل حفظ الملف: {error}",
                "cv_created_successfully": "تم إنشاء السيرة الذاتية في:\n{path}",
                "sections_order_saved": "تم حفظ ترتيب الأقسام بنجاح.",
                "completed_successfully": "اكتمل بنجاح",
                
                # About Window
                "about_window_title": "حول",
                "version_info": "Version {version}",
                "developed_by": "Developed by: {name}",

                # Section Names (for CV generation)
                "experience_section": "Experience",
                "education_section": "Education",
                "certifications_section": "Certifications",
                "languages_section": "Languages"
            },
            "en": {
                # Main Window
                "app_title": "Smart CV Assistant",
                "generate_cv_button": "🚀 Generate CV Now",
                "reorder_sections_button": "Reorder Sections",
                "tab_personal_info": "Personal Information & Experience",
                "tab_job_settings": "Job Description & Settings",
                "tab_templates": "CV Templates",
                "tab_ai_settings": "AI Settings",
                "language_switch_button": "العربية",
                "about_button": "About",
                
                # Personal Info Tab
                "personal_info_frame": "Personal Information",
                "full_name": "Full Name:",
                "job_title": "Job Title:",
                "email": "Email:",
                "linkedin": "LinkedIn URL:",
                "phone": "Phone Number:",
                "location": "Location:",
                "education_frame": "Education",
                "university": "University:",
                "degree": "Degree:",
                "work_experience": "Work Experience",
                "certifications": "Certifications & Courses",
                "languages": "Languages",
                "add_button": "Add",
                "edit_button": "Edit",
                "delete_button": "Delete",
                
                # Settings Tab
                "job_description_frame": "Job Description",
                "ai_settings_frame": "AI Settings",
                "open_ai_settings": "Open AI Settings",
                "ai_settings_window_title": "AI Settings",
                "service_provider": "Service Provider:",
                "api_key": "API Key:",
                "model_name": "Model Name:",
                "website_referer": "Website Referer:",
                "website_title": "Website Title:",
                "excluded_words": "Excluded Words (comma-separated):",
                "save": "Save",
                "cancel": "Cancel",

                # Reset Dialog
                "reset": "Reset",
                "reset_dialog_title": "Reset Data",
                "reset_dialog_description": "Choose the items you want to reset to default values",
                "reset_options": "Reset Options",
                "reset_all": "Reset All Data",
                "individual_options": "Individual Options",
                "reset_personal_info": "Personal Information & Education",
                "reset_experiences": "Work Experiences",
                "reset_certifications": "Certifications",
                "reset_languages": "Languages",
                "reset_section_names": "Custom Section Names",
                "reset_section_order": "Section Order",
                "reset_ai_providers": "AI Provider Settings",
                "reset_app_preferences": "App Preferences",
                "reset_language_preference": "Reset Language to Arabic",
                "reset_provider_preference": "Reset Provider to OpenAI",
                "reset_no_selection_warning": "Please select at least one item to reset",
                "reset_confirmation": "Are you sure you want to reset the following items?",
                "confirm_reset": "Confirm Reset",
                "reset_success": "Selected data has been reset successfully",
                "reset_button": "Reset Data",
                "section_customization": "Section Name Customization",
                "profile_section_title": "Profile Section Title:",
                "section_title": "Section Title:",
                "add_new_section": "➕ Add New Section",

                # Template Tab
                "template_selection_frame": "CV Template Selection",
                "template_modern_name": "Modern Design",
                "template_modern_desc": "A modern and elegant design, ideal for creative and tech fields.",
                "template_professional_name": "Professional Design",
                "template_professional_desc": "A classic and clear design, suitable for formal applications and large corporations.",
                "template_preview": "Template Preview",
                
                # Dialogs
                "add_certification": "Add Certification",
                "edit_certification": "Edit Certification",
                "certification_name": "Certification Name:",
                "issuing_authority": "Issuing Authority:",
                "add_language": "Add Language",
                "edit_language": "Edit Language",
                "language": "Language:",
                "proficiency_level": "Proficiency Level:",
                "add_experience": "Add Experience",
                "edit_experience": "Edit Experience",
                "job_position": "Job Position",
                "company_name": "Company Name",
                "duration": "Duration",
                "tasks_comma_separated": "Tasks (comma-separated)",
                "save_button": "Save",
                "cancel_button": "Cancel",
                
                # Proficiency Levels
                "beginner": "Beginner",
                "intermediate": "Intermediate",
                "advanced": "Advanced",
                "native": "Native",
                
                # Reorder Dialog
                "reorder_dialog_title": "Customize Section Order",
                "reorder_instructions": "Use arrows to reorder sections:",
                "move_up": "▲ Move Up",
                "move_down": "▼ Move Down",
                "save_order": "Save Order",
                
                # Messages
                "error": "Error",
                "success": "Success",
                "warning": "Warning",
                "working": "Working",
                "fill_all_fields": "Please fill all fields.",
                "fill_required_fields": "Please fill the required fields: Name, API Key, Model, and Job Description.",
                "position_company_required": "Job position and company name are required fields.",
                "select_item_to_delete": "Please select an item to delete.",
                "analyzing_job_description": "Analyzing job description... This may take some time.",
                "api_error": "API Error",
                "api_client_error": "Error initializing client: {error}",
                "write_error": "Write Error",
                "save_failed": "Failed to save file: {error}",
                "cv_created_successfully": "CV created successfully at:\n{path}",
                "sections_order_saved": "Section order saved successfully.",
                "completed_successfully": "Completed Successfully",
                
                # About Window
                "about_window_title": "About",
                "version_info": "Version {version}",
                "developed_by": "Developed by: {name}",

                # Section Names (for CV generation)
                "experience_section": "Experience",
                "education_section": "Education",
                "certifications_section": "Certifications",
                "languages_section": "Languages"
            }
        }
    
    def get_text(self, key, **kwargs):
        """
        Get translated text for the current language.
        
        Args:
            key: The translation key
            **kwargs: Format parameters for the text
            
        Returns:
            Translated text string
        """
        text = self.translations.get(self.current_language, {}).get(key, key)
        if kwargs:
            try:
                return text.format(**kwargs)
            except (KeyError, ValueError):
                return text
        return text
    
    def set_language(self, language_code):
        """
        Set the current language and notify observers.

        Args:
            language_code: 'ar' for Arabic, 'en' for English
        """
        if language_code in self.translations:
            self.current_language = language_code
            self._save_language_preference()
            self._notify_observers()
    
    def toggle_language(self):
        """Toggle between Arabic and English."""
        new_language = "en" if self.current_language == "ar" else "ar"
        self.set_language(new_language)
    
    def get_current_language(self):
        """Get the current language code."""
        return self.current_language
    
    def is_rtl(self):
        """Check if current language is right-to-left."""
        return self.current_language == "ar"
    
    def add_observer(self, callback):
        """
        Add an observer to be notified when language changes.
        
        Args:
            callback: Function to call when language changes
        """
        if callback not in self.observers:
            self.observers.append(callback)
    
    def remove_observer(self, callback):
        """
        Remove an observer.
        
        Args:
            callback: Function to remove from observers
        """
        if callback in self.observers:
            self.observers.remove(callback)
    
    def _notify_observers(self):
        """Notify all observers that language has changed."""
        for callback in self.observers:
            try:
                callback()
            except Exception as e:
                print(f"Error notifying language observer: {e}")

    def get_proficiency_levels(self):
        """Get proficiency levels for the current language."""
        return [
            self.get_text("beginner"),
            self.get_text("intermediate"),
            self.get_text("advanced"),
            self.get_text("native")
        ]

    def get_proficiency_translation_map(self):
        """Get mapping between Arabic and English proficiency levels."""
        return {
            "مبتدئ": "Beginner",
            "متوسط": "Intermediate",
            "متقدم": "Advanced",
            "لغة أم": "Native"
        }

    def get_proficiency_reverse_map(self):
        """Get mapping from English to Arabic proficiency levels."""
        translation_map = self.get_proficiency_translation_map()
        return {v: k for k, v in translation_map.items()}

    def _save_language_preference(self):
        """Save current language preference to settings."""
        try:
            # Import here to avoid circular import
            from settings_manager import settings_manager
            settings_manager.save_settings('app_preferences', {
                'language': self.current_language
            })
        except Exception as e:
            print(f"Error saving language preference: {e}")

    def _load_saved_language(self):
        """Load saved language preference from settings."""
        try:
            # Import here to avoid circular import
            from settings_manager import settings_manager
            preferences = settings_manager.load_settings('app_preferences', {})
            saved_language = preferences.get('language', 'ar')
            if saved_language in self.translations:
                self.current_language = saved_language
        except Exception as e:
            print(f"Error loading language preference: {e}")
            # Keep default language if error occurs


# Global language manager instance
language_manager = LanguageManager()

# Convenience function for getting translated text
def _(key, **kwargs):
    """
    Convenience function for getting translated text.

    Args:
        key: Translation key
        **kwargs: Format parameters

    Returns:
        Translated text
    """
    return language_manager.get_text(key, **kwargs)
