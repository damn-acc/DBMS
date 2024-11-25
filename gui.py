import tkinter as tk
from tkinter import messagebox
from database import DBMS

class GUI:
    def __init__(self, root):
        self.db = DBMS()

        root.title("Simple DB GUI")
        root.geometry("385x445")
        root.configure(bg="#001f3f")

        tk.Label(
            root,
            text="Database Management System",
            font=("Arial", 16, "bold"),
            bg="#001f3f",
            fg="#ffffff"
        ).grid(row=0, column=0, columnspan=2, pady=10)

        self.key_entry = tk.Entry(root, width=30, font=("Arial", 12), bg="#011d4b", fg="#ffffff")
        self.key_entry.grid(row=1, column=1, padx=10, pady=10)
        self.value_entry = tk.Entry(root, width=30, font=("Arial", 12), bg="#011d4b", fg="#ffffff")
        self.value_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(
            root, text="Key:", font=("Arial", 12), bg="#001f3f", fg="#ffffff"
        ).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        tk.Label(
            root, text="Value:", font=("Arial", 12), bg="#001f3f", fg="#ffffff"
        ).grid(row=2, column=0, padx=10, pady=10, sticky="e")

        button_style = {"font": ("Arial", 12), "bg": "#004080", "fg": "#ffffff", "activebackground": "#00509e"}

        tk.Button(root, text="Add", command=self.add_record, **button_style).grid(row=3, column=0, padx=10, pady=10)
        tk.Button(root, text="Delete", command=self.delete_record, **button_style).grid(row=3, column=1, padx=10, pady=10)
        tk.Button(root, text="Edit", command=self.edit_record, **button_style).grid(row=4, column=0, padx=10, pady=10)
        tk.Button(root, text="Search", command=self.search_record, **button_style).grid(row=4, column=1, padx=10, pady=10)

        self.output = tk.Text(
            root,
            height=10,
            width=40,
            font=("Arial", 12),
            bg="#011d4b",
            fg="#ffffff",
            wrap=tk.WORD,
            state=tk.NORMAL,
        )
        self.output.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def add_record(self):
        try:
            key = int(self.key_entry.get())
            value = self.value_entry.get()
            self.db.add_record(key, value)
            messagebox.showinfo("Success", "Record added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Key must be an integer.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_record(self):
        try:
            key = int(self.key_entry.get())
            self.db.delete_record(key)
            messagebox.showinfo("Success", "Record deleted successfully!")
        except ValueError:
            messagebox.showerror("Error", "Key must be an integer.")
        except KeyError:
            messagebox.showerror("Error", "Key not found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def edit_record(self):
        try:
            key = int(self.key_entry.get())
            value = self.value_entry.get()
            self.db.edit_record(key, value)
            messagebox.showinfo("Success", "Record updated successfully!")
        except ValueError:
            messagebox.showerror("Error", "Key must be an integer.")
        except KeyError:
            messagebox.showerror("Error", "Key not found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search_record(self):
        try:
            key = int(self.key_entry.get())
            value = self.db.search_record(key)
            self.output.delete(1.0, tk.END)
            if value is not None:
                self.output.insert(tk.END, f"Key: {key}, Value: {value}")
            else:
                self.output.insert(tk.END, "Record not found.")
        except ValueError:
            messagebox.showerror("Error", "Key must be an integer.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
