# ui/dialogs.py

import tkinter as tk
from tkinter import ttk, messagebox
from language import language_manager, _
from path_utils import resource_path

def position_dialog_beside_button(dialog_window, button_widget, dialog_key=None):
    # dialog_window.withdraw()  <-- قم بإزالة أو تعطيل هذا السطر
    dialog_window.update_idletasks()

    button_x = button_widget.winfo_rootx()
    button_y = button_widget.winfo_rooty()
    dialog_width = dialog_window.winfo_width()
    dialog_height = dialog_window.winfo_height()
    button_height = button_widget.winfo_height()

    # Position the dialog to the left of the button with a 10px margin
    x = button_x - dialog_width - 10

    # Special positioning for language_dialog
    if dialog_key == 'languages':
        # Align the bottom of the dialog with the bottom of the button
        y = button_y + button_height - dialog_height
    else:
        # Default behavior: align top of dialog with top of button
        y = button_y

    dialog_window.geometry(f"+{x}+{y}")
    dialog_window.deiconify() # <-- الخطوة 2: إظهار النافذة في مكانها النهائي


def base_dialog(parent, title):
    win = tk.Toplevel(parent)
    win.withdraw()  # <-- الخطوة 1: إخفاء النافذة فوراً هنا
    win.title(title)
    try:
        # أضف هذا السطر هنا
        win.iconbitmap(resource_path("icon/icon.ico"))
    except tk.TclError:
        # في حال لم يتم العثور على الأيقونة، تجاهل الخطأ
        pass
    win.transient(parent)
    win.grab_set()
    win.resizable(False, False)

    container = ttk.Frame(win, padding=20)
    container.pack(expand=True, fill="both")
    container.columnconfigure(1, weight=1)
    return win, container

def certification_dialog(parent, controller, index=None, button_widget=None):
    is_edit = index is not None
    data = controller.get_item('certifications', index) if is_edit else None
    title = _("edit_certification") if is_edit else _("add_certification")

    win, container = base_dialog(parent, title)

    ttk.Label(container, text=_("certification_name")).grid(row=0, column=0, padx=10, pady=8, sticky="w")
    name_entry = ttk.Entry(container, width=50)
    name_entry.grid(row=0, column=1, padx=10, pady=8, sticky="ew")
    if is_edit: name_entry.insert(0, data['name'])

    ttk.Label(container, text=_("issuing_authority")).grid(row=1, column=0, padx=10, pady=8, sticky="w")
    authority_entry = ttk.Entry(container, width=50)
    authority_entry.grid(row=1, column=1, padx=10, pady=8, sticky="ew")
    if is_edit: authority_entry.insert(0, data['authority'])

    def save():
        name = name_entry.get()
        authority = authority_entry.get()
        if not name or not authority:
            messagebox.showerror(_("error"), _("fill_all_fields"), parent=win)
            return

        new_data = {'name': name, 'authority': authority}
        controller.add_or_update_item('certifications', new_data, index)
        win.destroy()

    btn_frame = ttk.Frame(container)
    btn_frame.grid(row=2, column=0, columnspan=2, pady=(20, 0))
    ttk.Button(btn_frame, text=_("save_button"), command=save, style="Accent.TButton").pack(side="left", padx=5)
    ttk.Button(btn_frame, text=_("cancel_button"), command=win.destroy).pack(side="left", padx=5)

    if button_widget:
        position_dialog_beside_button(win, button_widget, dialog_key='certifications')

def language_dialog(parent, controller, index=None, button_widget=None):
    is_edit = index is not None
    data = controller.get_item('languages', index) if is_edit else None
    title = _("edit_language") if is_edit else _("add_language")

    win, container = base_dialog(parent, title)

    ttk.Label(container, text=_("language")).grid(row=0, column=0, padx=10, pady=8, sticky="w")
    name_entry = ttk.Entry(container, width=40)
    name_entry.grid(row=0, column=1, padx=10, pady=8, sticky="ew")
    if is_edit: name_entry.insert(0, data['name'])

    ttk.Label(container, text=_("proficiency_level")).grid(row=1, column=0, padx=10, pady=8, sticky="w")
    proficiency_levels = language_manager.get_proficiency_levels()
    proficiency_combo = ttk.Combobox(container, values=proficiency_levels, width=38, state="readonly")
    proficiency_combo.grid(row=1, column=1, padx=10, pady=8, sticky="ew")

    if is_edit:
        # Convert from English to current language for display
        english_proficiency = data['proficiency']
        if language_manager.get_current_language() == "ar":
            proficiency_reverse = language_manager.get_proficiency_reverse_map()
            display_proficiency = proficiency_reverse.get(english_proficiency, english_proficiency)
        else:
            display_proficiency = english_proficiency
        proficiency_combo.set(display_proficiency)
    else:
        proficiency_combo.current(1)  # Intermediate as default

    def save():
        name = name_entry.get()
        proficiency_display = proficiency_combo.get()
        if not name or not proficiency_display:
            messagebox.showerror(_("error"), _("fill_all_fields"), parent=win)
            return

        # Convert from current language to English for storage
        if language_manager.get_current_language() == "ar":
            proficiency_translation = language_manager.get_proficiency_translation_map()
            proficiency_english = proficiency_translation.get(proficiency_display, proficiency_display)
        else:
            proficiency_english = proficiency_display

        new_data = {'name': name, 'proficiency': proficiency_english}
        controller.add_or_update_item('languages', new_data, index)
        win.destroy()

    btn_frame = ttk.Frame(container)
    btn_frame.grid(row=2, column=0, columnspan=2, pady=(20, 0))
    ttk.Button(btn_frame, text=_("save_button"), command=save, style="Accent.TButton").pack(side="left", padx=5)
    ttk.Button(btn_frame, text=_("cancel_button"), command=win.destroy).pack(side="left", padx=5)

    if button_widget:
        position_dialog_beside_button(win, button_widget, dialog_key='languages')

def experience_dialog(parent, controller, index=None, button_widget=None):
    is_edit = index is not None
    exp_data = controller.get_item('experiences', index) if is_edit else None
    title = _("edit_experience") if is_edit else _("add_experience")

    win, container = base_dialog(parent, title)

    field_keys = ["job_position", "company_name", "duration", "tasks_comma_separated"]
    field_data_keys = ["position", "company", "duration", "details"]
    entries = {}

    for i, (label_key, data_key) in enumerate(zip(field_keys, field_data_keys)):
        ttk.Label(container, text=_(label_key)).grid(row=i, column=0, padx=10, pady=8, sticky="w")
        entry = ttk.Entry(container, width=50)
        entry.grid(row=i, column=1, padx=10, pady=8, sticky="ew")
        if is_edit:
            initial_value = ", ".join(exp_data[data_key]) if data_key == 'details' else exp_data[data_key]
            entry.insert(0, initial_value)
        entries[data_key] = entry

    def save():
        pos = entries["position"].get()
        comp = entries["company"].get()
        if not (pos and comp):
            messagebox.showerror(_("error"), _("position_company_required"), parent=win)
            return

        details_raw = entries["details"].get()
        updated_exp = {
            "position": pos,
            "company": comp,
            "duration": entries["duration"].get(),
            "details": [d.strip() for d in details_raw.split(',') if d.strip()]
        }

        controller.add_or_update_item('experiences', updated_exp, index)
        win.destroy()

    btn_frame = ttk.Frame(container)
    btn_frame.grid(row=len(field_keys), column=0, columnspan=2, pady=(20, 0))
    ttk.Button(btn_frame, text=_("save_button"), command=save, style="Accent.TButton").pack(side="left", padx=5)
    ttk.Button(btn_frame, text=_("cancel_button"), command=win.destroy).pack(side="left", padx=5)

    if button_widget:
        position_dialog_beside_button(win, button_widget, dialog_key='experiences')
