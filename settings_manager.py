# settings_manager.py
# مدير الإعدادات المركزي للبرنامج

import json
import os
import sys
from typing import Dict, Any, Optional

class SettingsManager:
    """مدير الإعدادات المركزي لحفظ وتحميل جميع إعدادات البرنامج"""

    def __init__(self, app_name: str = "SmartCVAssistant"):
        """
        يقوم المنشئ بتعيين مسار الإعدادات بناءً على نظام التشغيل لضمان صلاحيات الكتابة.
        app_name: اسم فريد للتطبيق لإنشاء مجلد خاص به.
        """
        self.settings_dir = self._get_user_data_dir(app_name)
        
        self.files = {
            'ai_providers': 'ai_provider_settings.json',
            'personal_info': 'personal_info.json',
            'section_names': 'section_names.json',
            'section_order': 'section_order.json',
            'user_experiences': 'user_experiences.json',
            'user_certifications': 'user_certifications.json',
            'user_languages': 'user_languages.json',
            'app_preferences': 'app_preferences.json'
        }
        
        self._create_settings_directory()

    def _get_user_data_dir(self, app_name: str) -> str:
        """
        الحصول على المسار القياسي لحفظ بيانات التطبيق غير المتجولة (Non-roaming).
        """
        # لنظام ويندوز، المسار هو %LOCALAPPDATA% للبيانات التي لا يجب مزامنتها عبر الشبكة
        if sys.platform == 'win32':
            # --- التغيير الرئيسي هنا ---
            # استخدام LOCALAPPDATA بدلاً من APPDATA
            path = os.getenv('LOCALAPPDATA')
        # لنظام ماك، المسار القياسي هو ~/Library/Application Support وهو لا يتجول افتراضيًا
        elif sys.platform == 'darwin':
            path = os.path.join(os.path.expanduser('~'), 'Library', 'Application Support')
        # لأنظمة لينكس، المسار هو ~/.local/share للبيانات
        else:
            path = os.path.join(os.path.expanduser('~'), '.local', 'share')

        if not path:
            path = os.path.expanduser('~')
        
        return os.path.join(path, app_name)
    
    def _create_settings_directory(self):
        """إنشاء مجلد الإعدادات إذا لم يكن موجوداً"""
        try:
            os.makedirs(self.settings_dir, exist_ok=True)
        except OSError as e:
            print(f"Could not create settings directory due to an OS error: {e}")
    
    def _get_file_path(self, file_key: str) -> str:
        """الحصول على المسار الكامل لملف الإعدادات"""
        if file_key not in self.files:
            raise ValueError(f"Unknown settings file key: {file_key}")
        return os.path.join(self.settings_dir, self.files[file_key])
    
    def save_settings(self, file_key: str, data: Dict[str, Any]) -> bool:
        """حفظ الإعدادات في الملف المحدد"""
        try:
            file_path = self._get_file_path(file_key)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except (IOError, ValueError, TypeError) as e:
            print(f"Error saving settings to {file_key}: {e}")
            return False
    
    def load_settings(self, file_key: str, default_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """تحميل الإعدادات من الملف المحدد"""
        default = default_data if default_data is not None else {}
        try:
            file_path = self._get_file_path(file_key)
            if not os.path.exists(file_path):
                return default
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError, ValueError) as e:
            print(f"Error loading settings from {file_key}, returning default: {e}")
            return default
    
    # ... باقي الدوال تبقى كما هي ...

    def delete_settings(self, file_key: str) -> bool:
        """حذف ملف الإعدادات المحدد"""
        try:
            file_path = self._get_file_path(file_key)
            if os.path.exists(file_path):
                os.remove(file_path)
            return True
        except (IOError, ValueError) as e:
            print(f"Error deleting settings file {file_key}: {e}")
            return False

    def file_exists(self, file_key: str) -> bool:
        """التحقق من وجود ملف الإعدادات"""
        try:
            file_path = self._get_file_path(file_key)
            return os.path.exists(file_path)
        except ValueError:
            return False

    def get_all_settings_files(self) -> Dict[str, str]:
        """الحصول على قائمة بجميع ملفات الإعدادات ومساراتها"""
        return {key: self._get_file_path(key) for key in self.files.keys()}

    def backup_all_settings(self, backup_dir: str = "backup") -> bool:
        """إنشاء نسخة احتياطية من جميع الإعدادات"""
        try:
            import shutil
            from datetime import datetime

            if not os.path.exists(self.settings_dir):
                print("Settings directory does not exist. Nothing to back up.")
                return False

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(backup_dir, f"settings_backup_{timestamp}")
            
            shutil.copytree(self.settings_dir, backup_path)
            return True
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False


# --- طريقة الاستخدام ---
# إنشاء مثيل مشترك من مدير الإعدادات
settings_manager = SettingsManager(app_name="SmartCVAssistant")

