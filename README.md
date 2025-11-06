# Smart CV Assistant - مساعد السيرة الذاتية الذكي

This is a desktop application designed to help users create professional CVs with the assistance of AI.

هذا تطبيق مكتبي مصمم لمساعدة المستخدمين على إنشاء سيرة ذاتية احترافية بمساعدة الذكاء الاصطناعي.

---

## English

### What the project does

Smart CV Assistant is a desktop application that simplifies the process of creating a professional Curriculum Vitae (CV). It provides a user-friendly interface to input personal information, work experience, education, skills, and other relevant sections. The key feature is its integration with AI (like OpenAI's models) to help generate, refine, and translate CV content, making it easier for users to craft compelling descriptions for their roles and accomplishments. The final CV can be exported as a `.docx` file using various templates.

### Why the project is useful

*   **AI-Powered Content:** Get help from AI to write professional and effective descriptions for your experiences and skills.
*   **Easy to Use:** A simple graphical user interface (GUI) makes it easy to manage different sections of your CV.
*   **Customizable Sections:** Users can add, remove, and reorder CV sections to fit their needs.
*   **Template-Based:** Choose from different templates to generate a polished and professional-looking CV document.
*   **Local Data Storage:** All your information is saved locally on your machine, ensuring privacy and easy access for future updates.

### How users can get started with the project

1.  **Prerequisites:**
    *   Python 3.x
    *   Make sure you have `pip` installed.

2.  **Installation:**
    *   Clone the repository to your local machine:
        ```bash
        git clone https://github.com/suhailelhag/Smart-CV-Assistant.git
        cd Smart-CV-Assistant
        ```
    *   It is recommended to create a virtual environment:
        ```bash
        python -m venv venv
        source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
        ```
    *   Install the required dependencies:
        ```bash
        pip install -r requirements.txt
        ```

3.  **Running the Application:**
    *   Execute the main script to launch the GUI:
        ```bash
        python main.py
        ```

4.  **Configuration:**
    *   Run the application for the first time.
    *   Navigate to the "AI Settings" tab.
    *   Enter your API key for your chosen AI provider (e.g., OpenAI).

### Where users can get help with your project

If you encounter any bugs or have suggestions for new features, please open an issue on the project's GitHub repository:
`https://github.com/suhailelhag/Smart-CV-Assistant/issues`

### Building from Source (Creating an .exe file)

If you want to create a standalone executable file for Windows, you can use `pyinstaller`.

1.  **Install PyInstaller:**
    ```bash
    pip install pyinstaller
    ```

2.  **Run the build command:**
    This command will bundle the application into a single executable file, including the necessary icons and image assets.
    ```bash
    pyinstaller --onefile --windowed --name "Smart CV Assistant" --icon "icon/icon.ico" --add-data "icon;icon" --add-data "images;images" main.py
    ```

3.  **(Optional) Compress the executable with UPX:**
    To reduce the size of the final `.exe` file, you can use UPX. First, download UPX and place it in a known directory. Then, add the `--upx-dir` flag to the command, pointing to the UPX location.
    
    *Note: Replace the path with the actual path to your UPX directory.*
    ```bash
    pyinstaller --onefile --windowed --name "Smart CV Assistant" --icon "icon/icon.ico" --add-data "icon;icon" --add-data "images;images" --upx-dir="path/to/your/upx-folder" main.py
    ```

### Who maintains and contributes to the project

This project is currently maintained by Suhail. Contributions are welcome!

---

## عربي

### عن المشروع

مساعد السيرة الذاتية الذكي هو تطبيق لسطح المكتب يسهل عملية إنشاء سيرة ذاتية احترافية. يوفر واجهة مستخدم رسومية لإدخال المعلومات الشخصية، الخبرات العملية، التعليم، المهارات، والأقسام الأخرى ذات الصلة. الميزة الرئيسية هي تكامله مع الذكاء الاصطناعي (مثل نماذج OpenAI) للمساعدة في إنشاء وتحسين وترجمة محتوى السيرة الذاتية، مما يسهل على المستخدمين صياغة أوصاف مقنعة لأدوارهم وإنجازاتهم. يمكن تصدير السيرة الذاتية النهائية كملف `.docx` باستخدام قوالب متنوعة.

### فائدة المشروع

*   **محتوى مدعوم بالذكاء الاصطناعي:** احصل على مساعدة من الذكاء الاصطناعي لكتابة أوصاف احترافية وفعالة لخبراتك ومهاراتك.
*   **سهل الاستخدام:** واجهة رسومية بسيطة تسهل إدارة أقسام سيرتك الذاتية المختلفة.
*   **أقسام قابلة للتخصيص:** يمكن للمستخدمين إضافة وإزالة وإعادة ترتيب أقسام السيرة الذاتية لتناسب احتياجاتهم.
*   **يعتمد على القوالب:** اختر من بين قوالب مختلفة لإنشاء سيرة ذاتية مصقولة وذات مظهر احترافي.
*   **تخزين محلي للبيانات:** يتم حفظ جميع معلوماتك محليًا على جهازك، مما يضمن الخصوصية وسهولة الوصول للتحديثات المستقبلية.

### كيف تبدأ باستخدام المشروع

1.  **المتطلبات الأساسية:**
    *   Python 3.x
    *   تأكد من تثبيت `pip`.

2.  **التثبيت:**
    *   انسخ المستودع إلى جهازك المحلي:
        ```bash
        git clone https://github.com/suhailelhag/Smart-CV-Assistant.git
        cd Smart-CV-Assistant
        ```
    *   يوصى بإنشاء بيئة افتراضية:
        ```bash
        python -m venv venv
        source venv/bin/activate  # على نظام ويندوز، استخدم `venv\Scripts\activate`
        ```
    *   قم بتثبيت المكتبات المطلوبة:
        ```bash
        pip install -r requirements.txt
        ```

3.  **تشغيل التطبيق:**
    *   نفذ السكربت الرئيسي لتشغيل الواجهة الرسومية:
        ```bash
        python main.py
        ```

4.  **الإعداد:**
    *   قم بتشغيل التطبيق لأول مرة.
    *   انتقل إلى تبويب "إعدادات الذكاء الاصطناعي".
    *   أدخل مفتاح API الخاص بمزود خدمة الذكاء الاصطناعي الذي اخترته (مثل OpenAI).

### أين يمكن الحصول على المساعدة

إذا واجهت أي أخطاء أو كانت لديك اقتراحات لميزات جديدة، يرجى فتح "issue" على مستودع المشروع في GitHub:
`https://github.com/suhailelhag/Smart-CV-Assistant/issues`

### بناء ملف تنفيذي (إنشاء ملف .exe)

إذا كنت ترغب في إنشاء ملف تنفيذي مستقل لنظام ويندوز، يمكنك استخدام `pyinstaller`.

1.  **تثبيت PyInstaller:**
    ```bash
    pip install pyinstaller
    ```

2.  **تنفيذ أمر البناء:**
    سيقوم هذا الأمر بتجميع التطبيق في ملف تنفيذي واحد، مع تضمين الأيقونات وملفات الصور اللازمة.
    ```bash
    pyinstaller --onefile --windowed --name "Smart CV Assistant" --icon "icon/icon.ico" --add-data "icon;icon" --add-data "images;images" main.py
    ```

3.  **(اختياري) ضغط الملف التنفيذي باستخدام UPX:**
    لتقليل حجم ملف `.exe` النهائي، يمكنك استخدام UPX. أولاً، قم بتنزيل UPX وضعه في مجلد معروف. بعد ذلك، أضف علامة `--upx-dir` إلى الأمر مع تحديد مسار مجلد UPX.

    *ملاحظة: استبدل المسار بالمسار الفعلي لمجلد UPX لديك.*
    ```bash
    pyinstaller --onefile --windowed --name "Smart CV Assistant" --icon "icon/icon.ico" --add-data "icon;icon" --add-data "images;images" --upx-dir="path/to/your/upx-folder" main.py
    ```

### من يقوم بصيانة المشروع والمساهمة فيه

يتم صيانة هذا المشروع حاليًا بواسطة سهيل. المساهمات مرحب بها!