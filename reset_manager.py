# reset_manager.py
# مدير إعادة التعيين للبيانات والإعدادات

import os
from settings_manager import settings_manager
from language import language_manager

class ResetManager:
    """مدير إعادة تعيين البيانات والإعدادات"""
    
    def __init__(self, app_controller):
        self.app_controller = app_controller
        
    def reset_selected_data(self, reset_options):
        """إعادة تعيين البيانات المحددة"""
        reset_count = 0
        
        try:
            # إعادة تعيين المعلومات الشخصية
            if reset_options.get('personal_info', False):
                self._reset_personal_info()
                reset_count += 1
                
            # إعادة تعيين الخبرات
            if reset_options.get('experiences', False):
                self._reset_experiences()
                reset_count += 1
                
            # إعادة تعيين الشهادات
            if reset_options.get('certifications', False):
                self._reset_certifications()
                reset_count += 1
                
            # إعادة تعيين اللغات
            if reset_options.get('languages', False):
                self._reset_languages()
                reset_count += 1
                
            # إعادة تعيين أسماء الأقسام
            if reset_options.get('section_names', False):
                self._reset_section_names()
                reset_count += 1
                
            # إعادة تعيين ترتيب الأقسام
            if reset_options.get('section_order', False):
                self._reset_section_order()
                reset_count += 1
                
            # إعادة تعيين إعدادات مزودي الذكاء الاصطناعي
            if reset_options.get('ai_providers', False):
                self._reset_ai_providers()
                reset_count += 1

            # إعادة تعيين تفضيل اللغة
            if reset_options.get('language_preference', False):
                self._reset_language_preference()
                reset_count += 1

            # إعادة تعيين تفضيل مزود الخدمة
            if reset_options.get('provider_preference', False):
                self._reset_provider_preference()
                reset_count += 1
                
            # تحديث الواجهة
            self._refresh_ui()
            
            return True, reset_count
            
        except Exception as e:
            print(f"Error during reset: {e}")
            return False, 0
    
    def _reset_personal_info(self):
        """إعادة تعيين المعلومات الشخصية"""
        # حذف ملف المعلومات الشخصية
        settings_manager.delete_settings('personal_info')
        
        # مسح الحقول في الواجهة
        if hasattr(self.app_controller, 'main_view') and hasattr(self.app_controller.main_view, 'user_info_tab'):
            user_tab = self.app_controller.main_view.user_info_tab
            
            # مسح حقول المعلومات الشخصية
            personal_fields = ['name', 'title', 'email', 'linkedin', 'phone', 'location', 'university', 'degree']
            for field in personal_fields:
                if hasattr(user_tab, f'{field}_entry'):
                    entry = getattr(user_tab, f'{field}_entry')
                    entry.delete(0, 'end')
    
    def _reset_experiences(self):
        """إعادة تعيين الخبرات"""
        # حذف ملف الخبرات
        settings_manager.delete_settings('user_experiences')
        
        # مسح البيانات من الكونترولر
        self.app_controller.user_data['experiences'] = []
        
        # تحديث الواجهة
        if hasattr(self.app_controller, 'main_view') and hasattr(self.app_controller.main_view, 'user_info_tab'):
            user_tab = self.app_controller.main_view.user_info_tab
            if 'experiences' in user_tab.listboxes:
                user_tab.refresh_listbox('experiences')
    
    def _reset_certifications(self):
        """إعادة تعيين الشهادات"""
        # حذف ملف الشهادات
        settings_manager.delete_settings('user_certifications')
        
        # مسح البيانات من الكونترولر
        self.app_controller.user_data['certifications'] = []
        
        # تحديث الواجهة
        if hasattr(self.app_controller, 'main_view') and hasattr(self.app_controller.main_view, 'user_info_tab'):
            user_tab = self.app_controller.main_view.user_info_tab
            if 'certifications' in user_tab.listboxes:
                user_tab.refresh_listbox('certifications')
    
    def _reset_languages(self):
        """إعادة تعيين اللغات"""
        # حذف ملف اللغات
        settings_manager.delete_settings('user_languages')
        
        # مسح البيانات من الكونترولر
        self.app_controller.user_data['languages'] = []
        
        # تحديث الواجهة
        if hasattr(self.app_controller, 'main_view') and hasattr(self.app_controller.main_view, 'user_info_tab'):
            user_tab = self.app_controller.main_view.user_info_tab
            if 'languages' in user_tab.listboxes:
                user_tab.refresh_listbox('languages')
    
    def _reset_section_names(self):
        """إعادة تعيين أسماء الأقسام"""
        # حذف ملف أسماء الأقسام
        settings_manager.delete_settings('section_names')
        
        # إعادة تعيين الأقسام في الواجهة
        if hasattr(self.app_controller, 'main_view') and hasattr(self.app_controller.main_view, 'settings_tab'):
            settings_tab = self.app_controller.main_view.settings_tab
            
            # إعادة تعيين حقل Profile
            if hasattr(settings_tab, 'profile_section_entry'):
                settings_tab.profile_section_entry.delete(0, 'end')
                settings_tab.profile_section_entry.insert(0, "Profile Summary")
            
            # مسح الأقسام الإضافية
            if hasattr(settings_tab, 'list_section_entries'):
                # حذف جميع الأقسام الحالية
                for entry in settings_tab.list_section_entries[:]:
                    entry.master.destroy()
                settings_tab.list_section_entries.clear()
                
                # إضافة الأقسام الافتراضية
                settings_tab._add_list_section_row("Skills")
                settings_tab._add_list_section_row("Interests")
    
    def _reset_section_order(self):
        """إعادة تعيين ترتيب الأقسام"""
        # حذف ملف ترتيب الأقسام
        settings_manager.delete_settings('section_order')
        
        # إعادة تعيين الترتيب الافتراضي
        default_order = [
            'profile', 'experiences', 'skills', 'interests', 'education', 'certifications', 'languages'
        ]
        self.app_controller.section_order = default_order
    
    def _reset_ai_providers(self):
        """إعادة تعيين إعدادات مزودي الذكاء الاصطناعي"""
        # حذف ملف إعدادات مزودي الذكاء الاصطناعي
        settings_manager.delete_settings('ai_providers')
        
        # إعادة تعيين الإعدادات في الواجهة
        if hasattr(self.app_controller, 'ai_settings_tab'):
            ai_tab = self.app_controller.ai_settings_tab
            
            # إعادة تعيين إعدادات المزودين
            ai_tab.provider_settings = {
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
            
            # إعادة تعيين المزود الحالي إلى OpenAI
            ai_tab.current_provider = 'openai'
            ai_tab.api_provider.set('openai')
            
            # تحديث الواجهة
            ai_tab.load_provider_data('openai')
            ai_tab.toggle_openrouter_fields(False)
    
    def _reset_language_preference(self):
        """إعادة تعيين تفضيل اللغة فقط"""
        # الحصول على التفضيلات الحالية
        preferences = settings_manager.load_settings('app_preferences', {})

        # إعادة تعيين اللغة إلى العربية
        language_manager.set_language('ar')

        # تحديث ملف التفضيلات (إزالة إعداد اللغة فقط)
        if 'language' in preferences:
            del preferences['language']
            settings_manager.save_settings('app_preferences', preferences)

    def _reset_provider_preference(self):
        """إعادة تعيين تفضيل مزود الخدمة فقط"""
        # الحصول على التفضيلات الحالية
        preferences = settings_manager.load_settings('app_preferences', {})

        # إعادة تعيين مزود الخدمة المختار إلى OpenAI
        if hasattr(self.app_controller, 'ai_settings_tab'):
            ai_tab = self.app_controller.ai_settings_tab
            ai_tab.current_provider = 'openai'
            ai_tab.api_provider.set('openai')
            ai_tab.toggle_openrouter_fields(False)

        # تحديث ملف التفضيلات (إزالة إعداد مزود الخدمة فقط)
        if 'selected_ai_provider' in preferences:
            del preferences['selected_ai_provider']
            settings_manager.save_settings('app_preferences', preferences)
    
    def _refresh_ui(self):
        """تحديث الواجهة بعد إعادة التعيين"""
        try:
            # تحديث تبويبة المعلومات الشخصية
            if hasattr(self.app_controller, 'main_view') and hasattr(self.app_controller.main_view, 'user_info_tab'):
                user_tab = self.app_controller.main_view.user_info_tab
                # تحديث جميع القوائم
                for key in ['experiences', 'certifications', 'languages']:
                    if key in user_tab.listboxes:
                        user_tab.refresh_listbox(key)
            
            # تحديث تبويبة الإعدادات
            if hasattr(self.app_controller, 'main_view') and hasattr(self.app_controller.main_view, 'settings_tab'):
                # لا حاجة لتحديث خاص، التحديث تم في الدوال المختصة
                pass
                
            # تحديث تبويبة إعدادات الذكاء الاصطناعي
            if hasattr(self.app_controller, 'ai_settings_tab'):
                # التحديث تم في الدوال المختصة
                pass
                
        except Exception as e:
            print(f"Error refreshing UI: {e}")
    
    def get_reset_summary(self, reset_options):
        """الحصول على ملخص العناصر المراد إعادة تعيينها"""
        summary = []
        
        if reset_options.get('personal_info', False):
            summary.append("المعلومات الشخصية والتعليم")
        if reset_options.get('experiences', False):
            summary.append("الخبرات العملية")
        if reset_options.get('certifications', False):
            summary.append("الشهادات")
        if reset_options.get('languages', False):
            summary.append("اللغات")
        if reset_options.get('section_names', False):
            summary.append("أسماء الأقسام المخصصة")
        if reset_options.get('section_order', False):
            summary.append("ترتيب الأقسام")
        if reset_options.get('ai_providers', False):
            summary.append("إعدادات مزودي الذكاء الاصطناعي")
        if reset_options.get('language_preference', False):
            summary.append("تفضيل اللغة")
        if reset_options.get('provider_preference', False):
            summary.append("تفضيل مزود الخدمة")
            
        return summary
