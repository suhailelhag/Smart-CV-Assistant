# ui/reorder_dialog.py

import tkinter as tk
from tkinter import ttk
from language import language_manager, _
from path_utils import resource_path

class ReorderDialog(tk.Toplevel):
    def __init__(self, parent, section_order, section_names, button_widget):
        super().__init__(parent)
        self.withdraw()  # <-- إخفاء النافذة فوراً هنا

        self.title(_("reorder_dialog_title"))
        try:
            # أضف هذا السطر هنا
            self.iconbitmap(resource_path("icon/icon.ico"))
        except tk.TclError:
            pass
        self.geometry("350x400")
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)

        self.new_order = list(section_order)
        self.section_names = section_names
        self.result = None

        container = ttk.Frame(self, padding=15)
        container.pack(expand=True, fill="both")

        ttk.Label(container, text=_("reorder_instructions")).pack(pady=(0, 10))

        list_frame = ttk.Frame(container)
        list_frame.pack(padx=10, pady=5, fill="both", expand=True)

        self.listbox = tk.Listbox(list_frame, selectmode="single", height=12, borderwidth=0, highlightthickness=0)
        self.listbox.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.populate_listbox()

        btn_frame = ttk.Frame(container)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text=_("move_up"), command=self.move_up).pack(side="left", padx=5)
        ttk.Button(btn_frame, text=_("move_down"), command=self.move_down).pack(side="left", padx=5)

        action_frame = ttk.Frame(container)
        action_frame.pack(pady=(15, 0))

        ttk.Button(action_frame, text=_("save_order"), command=self.save_order, style="Accent.TButton").pack(side="left", padx=10)
        ttk.Button(action_frame, text=_("cancel_button"), command=self.destroy).pack(side="left", padx=10)

        self.position_window(button_widget)
        self.wait_window()

    def position_window(self, button_widget):
        # self.withdraw() <-- قم بإزالة هذا السطر من هنا
        """Positions the dialog window below the specified button."""
        self.update_idletasks()  # Update window to get correct dimensions

        button_x = button_widget.winfo_rootx()
        button_y = button_widget.winfo_rooty()
        button_height = button_widget.winfo_height()

        # Position the dialog below the button
        x = button_x
        y = button_y + button_height + 5  # 5 pixels of padding
        self.geometry(f"+{x}+{y}")
        self.deiconify() # <-- إظهار النافذة في النهاية


    def populate_listbox(self):
        self.listbox.delete(0, tk.END)
        for key in self.new_order:
            display_name = self.section_names.get(key, key.capitalize())
            self.listbox.insert(tk.END, display_name)

    def move_up(self):
        selected_indices = self.listbox.curselection()
        if not selected_indices:
            return
        
        index = selected_indices[0]
        if index > 0:
            self.new_order[index], self.new_order[index - 1] = self.new_order[index - 1], self.new_order[index]
            self.populate_listbox()
            self.listbox.selection_set(index - 1)
            self.listbox.activate(index - 1)

    def move_down(self):
        selected_indices = self.listbox.curselection()
        if not selected_indices:
            return

        index = selected_indices[0]
        if index < len(self.new_order) - 1:
            self.new_order[index], self.new_order[index + 1] = self.new_order[index + 1], self.new_order[index]
            self.populate_listbox()
            self.listbox.selection_set(index + 1)
            self.listbox.activate(index + 1)

    def save_order(self):
        self.result = self.new_order
        self.destroy()