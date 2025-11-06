# main.py

import tkinter as tk
from app_controller import AppController

if __name__ == "__main__":
    # إنشاء النافذة الرئيسية للتطبيق
    root = tk.Tk()
    # إخفاء النافذة فوراً لمنع الوميض
    root.withdraw()
    # إنشاء نسخة من وحدة التحكم الرئيسية، والتي ستقوم بدورها بإنشاء الواجهة
    app = AppController(root)
    
    # لم نعد بحاجة إلى استدعاء root.mainloop() هنا لأن وحدة التحكم
    # تقوم بذلك في نهاية الـ __init__ الخاص بها.