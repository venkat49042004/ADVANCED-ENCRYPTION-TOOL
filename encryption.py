import os
import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import base64
import hashlib


def generate_key(password: str) -> bytes:
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())


def encrypt_file(file_path: str, key: bytes):
    with open(file_path, 'rb') as f:
        data = f.read()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)
    with open(file_path + '.enc', 'wb') as f:
        f.write(encrypted)


def decrypt_file(file_path: str, key: bytes):
    with open(file_path, 'rb') as f:
        data = f.read()
    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)
    original_path = file_path.replace('.enc', '')
    with open(original_path, 'wb') as f:
        f.write(decrypted)


class EncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Encryption Tool (AES-256)")
        self.root.geometry("500x200")

        self.label = tk.Label(root, text="Enter Password:")
        self.label.pack()

        self.password_entry = tk.Entry(root, show="*", width=50)
        self.password_entry.pack()

        self.encrypt_btn = tk.Button(root, text="Encrypt File", command=self.encrypt)
        self.encrypt_btn.pack(pady=10)

        self.decrypt_btn = tk.Button(root, text="Decrypt File", command=self.decrypt)
        self.decrypt_btn.pack(pady=10)

    def encrypt(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return
        password = self.password_entry.get()
        key = generate_key(password)
        try:
            encrypt_file(file_path, key)
            messagebox.showinfo("Success", "File encrypted successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def decrypt(self):
        file_path = filedialog.askopenfilename(filetypes=[("Encrypted files", "*.enc")])
        if not file_path:
            return
        password = self.password_entry.get()
        key = generate_key(password)
        try:
            decrypt_file(file_path, key)
            messagebox.showinfo("Success", "File decrypted successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = EncryptionApp(root)
    root.mainloop()
