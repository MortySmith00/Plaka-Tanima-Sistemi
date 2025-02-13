import tkinter as tk
from tkinter import font, messagebox
import sqlite3
import subprocess
import threading
from datetime import datetime

def initialize_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

def save_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    
    if result:
        messagebox.showerror("Hata", "Bu kullanıcı adı zaten mevcut.")
        conn.close()
        return False 
    
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Başarılı", "Kullanıcı başarıyla oluşturuldu!")
        conn.close()
        return True  
    except sqlite3.Error as e:
        messagebox.showerror("Veritabanı Hatası", f"Bir hata oluştu: {e}")
        conn.close()
        return False

def log_login(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO login_logs (username, login_time) VALUES (?, ?)", (username, login_time))
    conn.commit()
    conn.close()

def login():
    username = username_entry.get()
    password = password_entry.get()
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    
    if result:
        stored_password = result[0]
        
        if stored_password == password:
            messagebox.showinfo("Başarılı", "Giriş başarılı!")
            
            log_login(username)
            
            try:
                threading.Thread(target=run_main_py).start()
                root.quit()
                root.destroy()
            except Exception as e:
                messagebox.showerror("Hata", f"main dosyası çalıştırılamadı: {e}")
        else:
            messagebox.showerror("Hata", "Geçersiz şifre.")
    else:
        messagebox.showerror("Hata", "Kullanıcı adı bulunamadı.")
    
    conn.close()

def run_main_py():
    try:
        subprocess.run(["python", "main.py"], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Hata", f"main dosyası çalıştırılamadı: {e}")

def create_user():
    
    create_window = tk.Toplevel(root)
    create_window.title("Kullanıcı Oluştur")
    create_window.geometry("400x400")
    
    create_username_label = tk.Label(create_window, text="Kullanıcı Adı :", font=font_small)
    create_username_label.pack(pady=10)
    create_username_entry = tk.Entry(create_window, font=font_small)
    create_username_entry.insert(0, "")
    create_username_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, create_username_entry, "Kullanıcı Adı :"))
    create_username_entry.bind("<FocusOut>", lambda event: restore_placeholder(event, create_username_entry, "Kullanıcı Adı :"))
    create_username_entry.pack(pady=10)
    
    create_password_label = tk.Label(create_window, text="Şifre:", font=font_small)
    create_password_label.pack(pady=10)
    create_password_entry = tk.Entry(create_window, font=font_small, show="*")
    create_password_entry.insert(0, "")
    create_password_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, create_password_entry, "Şifre"))
    create_password_entry.bind("<FocusOut>", lambda event: restore_placeholder(event, create_password_entry, "Şifre"))
    create_password_entry.pack(pady=10)
    
    def submit_new_user():
        username = create_username_entry.get()
        password = create_password_entry.get()
        
        if username and password:
            if save_user(username, password):
                create_window.destroy()
        else:
            messagebox.showerror("Hata", "Kullanıcı adı ve şifre boş olamaz.")
    
    create_button = tk.Button(create_window, text="Kullanıcı Oluştur", **button_style, command=submit_new_user)
    create_button.pack(pady=20)

def clear_placeholder(event, entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, tk.END)
        entry.config(fg="black")

def restore_placeholder(event, entry, placeholder):
    if entry.get() == "":
        entry.insert(0, placeholder)
        entry.config(fg="gray")

root = tk.Tk()
root.title("Giriş Ekranı")
root.geometry("1400x900")
root.configure(bg="#b3b3b3")

font_large = font.Font(family="Arial", size=12, weight="bold")
font_small = font.Font(family="Arial", size=10)

button_style = {
    'bg': "#003366", 'fg': "white", 'font': ("Helvetica", 14, "bold"),
    'relief': "raised", 'bd': 5, 'highlightthickness': 0,
    'activebackground': "#00509E", 'activeforeground': "white",
    'width': 20, 'height': 2, 'overrelief': "sunken"
}

username_frame = tk.Frame(root, bg="white", bd=0, relief="solid")
username_frame.place(relx=0.5, rely=0.4, anchor="center", width=250, height=40)

username_entry = tk.Entry(username_frame, bd=0, font=font_small)
username_entry.insert(0, "Kullanıcı Adı :")
username_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, username_entry, "Kullanıcı Adı :"))
username_entry.bind("<FocusOut>", lambda event: restore_placeholder(event, username_entry, "Kullanıcı Adı :"))
username_entry.pack(side="left", fill="x", expand=True)

password_frame = tk.Frame(root, bg="white", bd=0, relief="solid")
password_frame.place(relx=0.5, rely=0.55, anchor="center", width=250, height=40)

password_entry = tk.Entry(password_frame, bd=0, show="*", font=font_small)
password_entry.insert(0, "Şifre")
password_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, password_entry, "Şifre"))
password_entry.bind("<FocusOut>", lambda event: restore_placeholder(event, password_entry, "Şifre"))
password_entry.pack(side="left", fill="x", expand=True)

login_button = tk.Button(root, text="Giriş Yap", **button_style, command=login)
login_button.place(relx=0.5, rely=0.7, anchor="center", width=250, height=40)

create_button = tk.Button(root, text="Kullanıcı Oluştur", **button_style, command=create_user)
create_button.place(relx=0.5, rely=0.8, anchor="center", width=250, height=40)

initialize_database()

root.mainloop()