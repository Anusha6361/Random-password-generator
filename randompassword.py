import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip


def update_length_display(val):
    length_display.config(text=f"Selected Length: {int(float(val))}")


def set_complexity(level):
    # Set checkboxes based on complexity level
    if level == "Low":
        letters_var.set(True)
        numbers_var.set(False)
        symbols_var.set(False)
    elif level == "Medium":
        letters_var.set(True)
        numbers_var.set(True)
        symbols_var.set(False)
    elif level == "High":
        letters_var.set(True)
        numbers_var.set(True)
        symbols_var.set(True)
    elif level == "Custom":
        # Leave it up to user
        pass


def generate_password():
    length = int(length_var.get())
    use_letters = letters_var.get()
    use_numbers = numbers_var.get()
    use_symbols = symbols_var.get()
    exclude_chars = exclude_var.get()

    if length < 4:
        messagebox.showwarning("Warning", "Password length should be at least 4.")
        return

    if not (use_letters or use_numbers or use_symbols):
        messagebox.showerror("Error", "Please select at least one character type.")
        return

    char_pool = ''
    if use_letters:
        char_pool += string.ascii_letters
    if use_numbers:
        char_pool += string.digits
    if use_symbols:
        char_pool += string.punctuation

    char_pool = ''.join(ch for ch in char_pool if ch not in exclude_chars)

    if not char_pool:
        messagebox.showerror("Error", "Character pool is empty after exclusions!")
        return

    password_chars = []

    # Enforce at least one of each selected type (security rule)
    if use_letters:
        letters = ''.join(ch for ch in string.ascii_letters if ch not in exclude_chars)
        if letters:
            password_chars.append(random.choice(letters))
    if use_numbers:
        numbers = ''.join(ch for ch in string.digits if ch not in exclude_chars)
        if numbers:
            password_chars.append(random.choice(numbers))
    if use_symbols:
        symbols = ''.join(ch for ch in string.punctuation if ch not in exclude_chars)
        if symbols:
            password_chars.append(random.choice(symbols))

    remaining = length - len(password_chars)
    password_chars += random.choices(char_pool, k=remaining)
    random.shuffle(password_chars)
    password = ''.join(password_chars)

    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)


def copy_to_clipboard():
    password = password_entry.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")


# GUI Setup
app = tk.Tk()
app.title("🔐 Secure Password Generator")
app.attributes('-fullscreen', True)
app.configure(bg="#e9f1f7")

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Segoe UI", 13, "bold"), padding=10, background="#0066cc", foreground="white")
style.map("TButton", background=[("active", "#004d99")])
style.configure("TCheckbutton", background="#e9f1f7", font=("Segoe UI", 12))
style.configure("TLabel", background="#e9f1f7", font=("Segoe UI", 12))
style.configure("TCombobox", font=("Segoe UI", 12))
style.configure("Horizontal.TScale", background="#e9f1f7")

# Main Frame
frame = tk.Frame(app, bg="#e9f1f7")
frame.pack(expand=True)

# Title
ttk.Label(frame, text="🔐 Advanced Password Generator", font=("Segoe UI", 28, "bold")).pack(pady=20)

# Complexity
ttk.Label(frame, text="Password Complexity:").pack()
complexity_var = tk.StringVar(value="Custom")
complexity_combo = ttk.Combobox(frame, textvariable=complexity_var, values=["Low", "Medium", "High", "Custom"], state="readonly", width=15)
complexity_combo.pack(pady=5)
complexity_combo.bind("<<ComboboxSelected>>", lambda e: set_complexity(complexity_var.get()))

# Password length
ttk.Label(frame, text="Select Password Length:").pack(pady=(15, 0))
length_var = tk.DoubleVar(value=12)
ttk.Scale(frame, from_=4, to=32, orient="horizontal", variable=length_var, length=400, command=update_length_display).pack()
length_display = ttk.Label(frame, text=f"Selected Length: {int(length_var.get())}", font=("Segoe UI", 12, "bold"))
length_display.pack()

# Options
letters_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)

ttk.Checkbutton(frame, text="Include Letters (A–Z, a–z)", variable=letters_var).pack(anchor="w", padx=100, pady=5)
ttk.Checkbutton(frame, text="Include Numbers (0–9)", variable=numbers_var).pack(anchor="w", padx=100, pady=5)
ttk.Checkbutton(frame, text="Include Symbols (!@#$)", variable=symbols_var).pack(anchor="w", padx=100, pady=5)

# Exclude characters
ttk.Label(frame, text="Exclude Characters (e.g. O0l1):").pack(pady=(15, 0))
exclude_var = tk.StringVar()
ttk.Entry(frame, textvariable=exclude_var, width=40, font=("Segoe UI", 12)).pack(pady=5)

# Generate and Copy buttons
ttk.Button(frame, text="🔄 Generate Password", command=generate_password).pack(pady=20)
password_entry = ttk.Entry(frame, font=("Consolas", 18), justify="center")
password_entry.pack(pady=10, ipadx=10, ipady=6, fill="x", padx=200)
ttk.Button(frame, text="📋 Copy to Clipboard", command=copy_to_clipboard).pack(pady=10)
ttk.Button(frame, text="❌ Exit", command=app.destroy).pack(pady=20)

# Footer
ttk.Label(frame, text="© Designed by You ❤️", font=("Segoe UI", 10, "italic")).pack(pady=10)

app.mainloop()
