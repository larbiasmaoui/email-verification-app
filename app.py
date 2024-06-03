import tkinter as tk
from email_verifier.gui import EmailVerifierApp

if __name__ == "__main__":
    root = tk.Tk()
    app = EmailVerifierApp(root)
    root.mainloop()
