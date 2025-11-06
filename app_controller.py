# app_controller.py

import tkinter as tk
from tkinter import ttk # Added ttk import
import threading
import queue
from tkinter import filedialog, messagebox
from openai import OpenAI

from ui.main_window import MainWindow
from api_handler import analyze_job_description, parse_ai_response
from ui.reorder_dialog import ReorderDialog
from ui.reset_dialog import ResetDialog
from ui.about_window import AboutWindow
from language import language_manager, _
from settings_manager import settings_manager
from reset_manager import ResetManager
from path_utils import resource_path

class AppController:
    def __init__(self, root):
        self.root = root
        self.user_data = {
            'name': '', 'title': '', 'email': '', 'linkedin': '', 'phone': '', 'location': '',
            'university': '', 'degree': '',
            'certifications': [], 'languages': [], 'experiences': []
        }
        # Load saved section order or use default
        default_order = [
            'profile', 'experiences', 'skills', 'interests', 'education', 'certifications', 'languages'
        ]
        self.section_order = settings_manager.load_settings('section_order', default_order)
        
        self.main_view = MainWindow(root, self)

        # Store reference to AI settings tab for easy access
        self.ai_settings_tab = self.main_view.ai_settings_tab
        self.template_tab = self.main_view.template_tab

        # Initialize reset manager
        self.reset_manager = ResetManager(self)

        # Center the window on screen
        self.center_window()

        # Set up cleanup on window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.root.mainloop()

    def center_window(self):
        """Center the main window on the screen."""
        # Update the window to get accurate dimensions
        self.root.update_idletasks()

        # Get current window dimensions (or use default if not set)
        window_width = self.root.winfo_reqwidth()
        window_height = self.root.winfo_reqheight()

        # If window dimensions are too small, use minimum reasonable size
        min_width = 800
        min_height = 600

        if window_width < min_width:
            window_width = min_width
        if window_height < min_height:
            window_height = min_height

        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate center position
        center_x = (screen_width - window_width) // 2
        center_y = (screen_height - window_height) // 2

        # Ensure the window doesn't go off-screen (minimum margins of 50 pixels)
        margin = 50
        center_x = max(margin, min(center_x, screen_width - window_width - margin))
        center_y = max(margin, min(center_y, screen_height - window_height - margin))

        # Set the window size and position
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        # Ensure window is visible and focused
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def open_reorder_dialog(self, button_widget):
        """
        Opens the section order customization dialog after syncing new and deleted sections.
        """
        settings_info = self.main_view.settings_tab.get_data()

        # --- Main modification start ---

        # 1. Get all current keys from settings and static sections
        ai_section_keys = set(settings_info['section_names'].keys())
        static_keys = {'experiences', 'education', 'certifications', 'languages'}
        all_current_keys = ai_section_keys.union(static_keys)

        # 2. Sync current order list
        # Remove sections that no longer exist
        synced_order = [key for key in self.section_order if key in all_current_keys]

        # Add new sections that weren't in the order list
        for key in all_current_keys:
            if key not in synced_order:
                synced_order.append(key)

        # Update main order list in the application
        self.section_order = synced_order

        # 3. Create full names dictionary for display in the window
        all_section_names = {**settings_info['section_names']}
        all_section_names.update({
            'experiences': _('experience_section'),
            'education': _('education_section'),
            'certifications': _('certifications_section'),
            'languages': _('languages_section')
        })
        # --- Main modification end ---

        dialog = ReorderDialog(self.root, self.section_order, all_section_names, button_widget)
        if dialog.result:
            self.section_order = dialog.result
            # Save section order to settings
            settings_manager.save_settings('section_order', self.section_order)
            messagebox.showinfo(_("success"), _("sections_order_saved"), parent=self.root)


    def generate_cv(self):
        personal_info = self.main_view.user_info_tab.get_data()
        settings_info = self.main_view.settings_tab.get_data()

        self.user_data.update(personal_info)

        job_desc = settings_info['job_desc']
        api_key = settings_info['api_key']
        model = settings_info['model']
        excluded_terms = settings_info['excluded_terms']
        section_names = settings_info['section_names']
        template = self.template_tab.get_selected_template()

        if not all([self.user_data['name'], api_key, model, job_desc]):
            messagebox.showerror(_("error"), _("fill_required_fields"))
            return

        provider = settings_info['provider']
        headers = {}
        if provider == "openrouter":
            base_url = "https://openrouter.ai/api/v1"
            if settings_info['http_referer']: headers["HTTP-Referer"] = settings_info['http_referer']
            if settings_info['x_title']: headers["X-Title"] = settings_info['x_title']
        else:
            base_url = "https://api.openai.com/v1"
        
        try:
            client = OpenAI(api_key=api_key, base_url=base_url, default_headers=headers)
        except Exception as e:
            messagebox.showerror(_("api_error"), _("api_client_error", error=str(e)))
            return

        # --- Threading Implementation ---

        # 1. Create a non-modal "working" window
        working_window = tk.Toplevel(self.root)
        working_window.title(_("working"))
        working_window.transient(self.root)
        working_window.grab_set()
        working_window.resizable(False, False)
        try:
            # Add this line here
            working_window.iconbitmap(resource_path("icon/icon.ico"))
        except tk.TclError:
            pass
        ttk.Label(working_window, text=_("analyzing_job_description"), padding=20).pack()
        
        # Center the working window
        self.root.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (working_window.winfo_reqwidth() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (working_window.winfo_reqheight() // 2)
        working_window.geometry(f"+{x}+{y}")

        # 2. Create a queue to communicate between threads
        result_queue = queue.Queue()

        # 3. Define the worker function to run in a separate thread
        def worker():
            try:
                ai_result = analyze_job_description(client, model, job_desc, excluded_terms, section_names)
                if ai_result.startswith("Error"):
                    result_queue.put(("error", ai_result))
                    return
                
                ai_data = parse_ai_response(ai_result, section_names)
                result_queue.put(("success", ai_data))
            except Exception as e:
                result_queue.put(("error", str(e)))

        # 4. Start the worker thread
        threading.Thread(target=worker, daemon=True).start()

        # 5. Define a function to check the queue and process the result in the main thread
        def check_queue():
            try:
                status, data = result_queue.get_nowait()
                
                # Close the "working" window
                working_window.destroy()

                if status == "success":
                    ai_data = data
                    save_path = filedialog.asksaveasfilename(
                        defaultextension=".docx",
                        filetypes=[("Word Document", "*.docx")],
                        initialfile=f"CV_{self.user_data['name']}.docx",
                        parent=self.root
                    )
                    if not save_path:
                        return

                    try:
                        if template == 'professional':
                            from doc_generator1 import write_cv
                        else:
                            from doc_generator import write_cv

                        write_cv(self.user_data, ai_data, save_path, section_names, self.section_order)
                        messagebox.showinfo(_("completed_successfully"), _("cv_created_successfully", path=save_path), parent=self.root)
                    except Exception as e:
                        messagebox.showerror(_("write_error"), _("save_failed", error=str(e)), parent=self.root)
                else: # status == "error"
                    messagebox.showerror(_("api_error"), data, parent=self.root)

            except queue.Empty:
                # If the queue is empty, check again after 100ms
                self.root.after(100, check_queue)

        # 6. Start polling the queue
        self.root.after(100, check_queue)

    def add_or_update_item(self, key, item_data, index=None):
        if index is None:
            self.user_data[key].append(item_data)
        else:
            self.user_data[key][index] = item_data
        self.main_view.user_info_tab.refresh_listbox(key)

    def delete_item(self, key, index):
        if 0 <= index < len(self.user_data[key]):
            del self.user_data[key][index]
            self.main_view.user_info_tab.refresh_listbox(key)

    def get_item(self, key, index):
        if 0 <= index < len(self.user_data[key]):
            return self.user_data[key][index]
        return None

    def open_reset_dialog(self, button_widget):
        """Open the reset dialog to allow user to choose what to reset."""
        dialog = ResetDialog(self.root, button_widget)
        self.root.wait_window(dialog.window)

        if dialog.result:
            # تنفيذ إعادة التعيين
            success, reset_count = self.reset_manager.reset_selected_data(dialog.result)

            if success:
                messagebox.showinfo(
                    _("success"),
                    _("reset_success"),
                    parent=self.root
                )
            else:
                messagebox.showerror(
                    _("error"),
                    "حدث خطأ أثناء إعادة التعيين",
                    parent=self.root
                )

    def open_about_window(self):
        """Opens the About window."""
        AboutWindow(self.root)

    def on_closing(self):
        """Handle application closing - save all settings before exit."""
        try:
            # Save AI settings and provider preference
            if hasattr(self, 'ai_settings_tab') and self.ai_settings_tab:
                # Save current provider data first
                self.ai_settings_tab.save_current_provider_data()
                # Save all provider settings to file
                self.ai_settings_tab.save_settings_to_file()
                # Save provider preference
                self.ai_settings_tab.save_provider_preference()


            # Save personal information and user lists
            if hasattr(self, 'main_view') and hasattr(self.main_view, 'user_info_tab'):
                self.main_view.user_info_tab.save_personal_info()
                self.main_view.user_info_tab.save_user_lists()

            # Save section names
            if hasattr(self, 'main_view') and hasattr(self.main_view, 'settings_tab'):
                self.main_view.settings_tab.save_section_names()

            # Save section order
            settings_manager.save_settings('section_order', self.section_order)

            # Save template preference
            if hasattr(self, 'template_tab') and self.template_tab:
                self.template_tab.save_template_preference()

        except Exception as e:
            print(f"Error saving settings on close: {e}")
        finally:
            # Close the application
            self.root.destroy()