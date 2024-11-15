import pyshorteners
import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip
import validators

class URLShortenerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("URL Shortener")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")

        # Create main frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(
            self.main_frame, 
            text="URL Shortener",
            font=("Helvetica", 24, "bold")
        )
        title_label.pack(pady=20)

        # URL Entry
        self.url_frame = ttk.Frame(self.main_frame)
        self.url_frame.pack(fill=tk.X, pady=20)

        self.url_entry = ttk.Entry(self.url_frame, width=50)
        self.url_entry.pack(side=tk.LEFT, padx=5)
        self.url_entry.insert(0, "Enter URL here...")
        self.url_entry.bind("<FocusIn>", self.clear_placeholder)
        self.url_entry.bind("<FocusOut>", self.restore_placeholder)

        # Shorten Button
        self.shorten_button = ttk.Button(
            self.url_frame,
            text="Shorten URL",
            command=self.shorten_url
        )
        self.shorten_button.pack(side=tk.LEFT, padx=5)

        # Result Frame
        self.result_frame = ttk.Frame(self.main_frame)
        self.result_frame.pack(fill=tk.X, pady=20)

        # Result Entry
        self.result_entry = ttk.Entry(self.result_frame, width=50)
        self.result_entry.pack(side=tk.LEFT, padx=5)
        self.result_entry.insert(0, "Shortened URL will appear here...")
        self.result_entry.configure(state='readonly')

        # Copy Button
        self.copy_button = ttk.Button(
            self.result_frame,
            text="Copy URL",
            command=self.copy_url
        )
        self.copy_button.pack(side=tk.LEFT, padx=5)
        self.copy_button.configure(state='disabled')

        # Status Label
        self.status_label = ttk.Label(
            self.main_frame,
            text="",
            font=("Helvetica", 10)
        )
        self.status_label.pack(pady=10)

    def clear_placeholder(self, event):
        if self.url_entry.get() == "Enter URL here...":
            self.url_entry.delete(0, tk.END)

    def restore_placeholder(self, event):
        if not self.url_entry.get():
            self.url_entry.insert(0, "Enter URL here...")

    def validate_url(self, url):
        return validators.url(url)

    def shorten_url(self):
        url = self.url_entry.get()
        
        # Check if URL is empty or placeholder
        if url == "Enter URL here..." or not url:
            messagebox.showerror("Error", "Please enter a URL")
            return

        # Validate URL
        if not self.validate_url(url):
            messagebox.showerror("Error", "Please enter a valid URL")
            return

        try:
            # Initialize shortener
            shortener = pyshorteners.Shortener()
            
            # Get shortened URL
            shortened_url = shortener.tinyurl.short(url)
            
            # Update result entry
            self.result_entry.configure(state='normal')
            self.result_entry.delete(0, tk.END)
            self.result_entry.insert(0, shortened_url)
            self.result_entry.configure(state='readonly')
            
            # Enable copy button
            self.copy_button.configure(state='normal')
            
            # Update status
            self.status_label.configure(
                text="URL shortened successfully!",
                foreground="green"
            )

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_label.configure(
                text="Failed to shorten URL",
                foreground="red"
            )

    def copy_url(self):
        shortened_url = self.result_entry.get()
        pyperclip.copy(shortened_url)
        self.status_label.configure(
            text="URL copied to clipboard!",
            foreground="green"
        )

def main():
    root = tk.Tk()
    app = URLShortenerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()