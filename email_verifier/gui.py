import tkinter as tk
from tkinter import filedialog, messagebox
import threading
from email_verifier.validator import EmailValidator
from email_verifier.utils import check_internet_connection
from email_verifier.export import export_results

class EmailVerifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Verification App")
        
        self.upload_button = tk.Button(root, text="Browse", command=self.open_file_and_process)
        self.upload_button.pack(pady=10)

        self.clear_button = tk.Button(root, text="Clear", command=self.clear_text_area)
        self.clear_button.pack(pady=10)

        self.loading_label = tk.Label(root, text="", fg="blue")
        self.loading_label.pack(pady=10)

        self.progress_label = tk.Label(root, text="")
        self.progress_label.pack(pady=10)
        
        self.text_area = tk.Text(root, wrap='word', height=20, width=50)
        self.text_area.pack(pady=10)

        self.export_button = tk.Button(root, text="Export Results", command=self.export_results, state=tk.DISABLED)
        self.export_button.pack(pady=10)

        self.results = []
        self.email_validator = EmailValidator()
        self.processing_lock = threading.Lock()

    def open_file_and_process(self):
        if not check_internet_connection():
            messagebox.showerror("Error", "No internet connection.")
            return

        if self.processing_lock.locked():
            messagebox.showinfo("Info", "Please wait until the current process is finished.")
            return

        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.upload_button.config(state=tk.DISABLED)
            self.clear_button.config(state=tk.DISABLED)
            self.loading_label.config(text="Processing, please wait...")
            self.text_area.delete(1.0, tk.END)
            threading.Thread(target=self.process_email_list, args=(file_path,)).start()

    def process_email_list(self, file_path):
        with self.processing_lock:
            try:
                with open(file_path, 'r') as file:
                    emails = file.readlines()

                total_emails = len(emails)
                valid_emails = []
                invalid_emails = []
                for idx, email in enumerate(emails):
                    email = email.strip()
                    if not email:
                        continue
                    is_valid, message = self.email_validator.validate_and_verify_email(email)
                    if is_valid:
                        valid_emails.append(email)
                    else:
                        invalid_emails.append(email)
                    self.text_area.insert(tk.END, f"{email}: {'Valid' if is_valid else 'Invalid'}\n")
                    self.progress_label.config(text=f"Processed {idx + 1}/{total_emails} emails")

                self.results = {"valid": valid_emails, "invalid": invalid_emails}
                self.export_button.config(state=tk.NORMAL)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
            finally:
                self.upload_button.config(state=tk.NORMAL)
                self.loading_label.config(text="")
                self.progress_label.config(text="")

    def export_results(self):
        export_results(self.results)
        messagebox.showinfo("Success", "Results exported successfully!")
    
    def clear_text_area(self):
        self.text_area.delete(1.0, tk.END)
