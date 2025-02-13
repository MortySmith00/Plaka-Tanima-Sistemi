import tkinter as tk
from tkinter import messagebox
import sqlite3
import os
from PIL import Image, ImageTk

def get_last_plate():
    conn = sqlite3.connect("recognized_plates.db")
    c = conn.cursor()
    c.execute("SELECT plate FROM plates ORDER BY timestamp DESC LIMIT 1")
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]
    return None

def show_info_window():

    last_plate = get_last_plate()
    
    if not last_plate:
        messagebox.showerror("Hata", "Plaka kayıtı bulunamadı.")
        return
    conn = sqlite3.connect("vehicle_info.db")
    c = conn.cursor()
    c.execute("SELECT * FROM vehicle_info WHERE plaka = ?", (last_plate,))
    result = c.fetchone()
    conn.close()

    if not result:
        messagebox.showerror("Hata", f"{last_plate} plakasına ait bilgi bulunamadı.")
        return

    info_window = tk.Toplevel()
    info_window.title("Araç ve Sürücü Bilgileri")
    info_window.geometry("1400x900")
    info_window.configure(bg="#A9A9A9")

    original_width = 1400
    original_height = 900
    label_width = 276
    label_height = 74.8

    label_positions = [
        (90, 209.6), (90, 317.6), (90, 425.4), (90, 533.1), (90, 640.9), (90, 749),
        (1034, 209.6), (1034, 317.6), (1034, 425.4), (1034, 533.1), (1034, 640.9), (1034, 749)
                      ]

    label_texts = [
        "Plaka:", "Araç Modeli:", "Yük Türü:", "Araç Ağırlığı:", "E-Beyanname:", "Sigorta Numarası:",
        "Ad Soyad:", "Kimlik No:", "Pasaport No:", "İletişim Bilgisi:", "Yetki Belgesi Türü:", "Firma:"
                  ]
    labels = []
    for i, text in enumerate(label_texts):
        label = tk.Label(info_window, text=text, bg="lightblue", font=("Helvetica", 12))
        labels.append(label)

    image_label = tk.Label(info_window, bg="white")
    image_label.place(x=550, y=312.7, width=300, height=300)

    icon1_path = "Uygulama Görselleri//truck.png"
    if os.path.exists(icon1_path):
        icon1_img = Image.open(icon1_path)
        icon1_img = icon1_img.resize((150, 150), Image.Resampling.LANCZOS)
        icon1_tk = ImageTk.PhotoImage(icon1_img)
        icon1_label = tk.Label(info_window, image=icon1_tk, bg="#A9A9A9")
        icon1_label.image = icon1_tk
        icon1_label.place(x=128.7, y=11.2, width=180, height=175)

    icon2_path = "Uygulama Görselleri//profile.png"
    if os.path.exists(icon2_path):
        icon2_img = Image.open(icon2_path)
        icon2_img = icon2_img.resize((150, 150), Image.Resampling.LANCZOS)
        icon2_tk = ImageTk.PhotoImage(icon2_img)
        icon2_label = tk.Label(info_window, image=icon2_tk, bg="#A9A9A9")
        icon2_label.image = icon2_tk
        icon2_label.place(x=1082, y=11.2, width=180, height=175)

    button_style = {
        'bg': "#003366", 'fg': "white", 'font': ("Helvetica", 14, "bold"),
        'relief': "raised", 'bd': 5, 'highlightthickness': 0,
        'activebackground': "#00509E", 'activeforeground': "white",
        'width': 20, 'height': 2, 'overrelief': "sunken"
                   }

    button_image_path = "Uygulama Görselleri//lock.png"
    if os.path.exists(button_image_path):
        button_img = Image.open(button_image_path)
        button_img = button_img.resize((53, 53), Image.Resampling.LANCZOS)
        button_img_tk = ImageTk.PhotoImage(button_img)
    else:
        button_img_tk = None

    button = tk.Button(info_window, **button_style, image=button_img_tk, compound="top")
    button.image = button_img_tk
    button.place(x=656, y=717.5, width=88.2, height=69.2)

    original_button_x = 656
    original_button_y = 717.5
    original_button_width = 88.2
    original_button_height = 69.2

    def on_button_click():
        info_label = tk.Label(info_window, text="Bariyer Açılıyor...", bg="#A9A9A9", font=("Helvetica", 16))
        info_label.place(x=550, y=650, width=300, height=50)
    button.config(command=on_button_click)

    def update_labels(event=None):
        new_width = info_window.winfo_width()
        new_height = info_window.winfo_height()

        for i, (x, y) in enumerate(label_positions):
            new_x = int(x * (new_width / original_width))
            new_y = int(y * (new_height / original_height))
            new_label_width = int(label_width * (new_width / original_width))
            new_label_height = int(label_height * (new_height / original_height))
            labels[i].place(x=new_x, y=new_y, width=new_label_width, height=new_label_height)

        new_image_x = int(550 * (new_width / original_width))
        new_image_y = int(312.7 * (new_height / original_height))
        new_image_width = int(300 * (new_width / original_width))
        new_image_height = int(300 * (new_height / original_height))
        image_label.place(x=new_image_x, y=new_image_y, width=new_image_width, height=new_image_height)

        new_icon1_x = int(128.7 * (new_width / original_width))
        new_icon1_y = int(11.2 * (new_height / original_height))
        new_icon1_width = int(180 * (new_width / original_width))
        new_icon1_height = int(175 * (new_height / original_height))

        icon1_label.place(x=new_icon1_x, y=new_icon1_y, width=new_icon1_width, height=new_icon1_height)
        new_icon2_x = int(1082 * (new_width / original_width))
        new_icon2_y = int(11.2 * (new_height / original_height))
        new_icon2_width = int(180 * (new_width / original_width))
        new_icon2_height = int(175 * (new_height / original_height))

        icon2_label.place(x=new_icon2_x, y=new_icon2_y, width=new_icon2_width, height=new_icon2_height)
        new_button_x = int(original_button_x * (new_width / original_width))
        new_button_y = int(original_button_y * (new_height / original_height))
        new_button_width = int(original_button_width * (new_width / original_width))
        new_button_height = int(original_button_height * (new_height / original_height))
        button.place(x=new_button_x, y=new_button_y, width=new_button_width, height=new_button_height)

        if last_plate:
            image_path = os.path.join("C:\\Users\\Morty\\Desktop\\Plaka Tanima Sistemi\\Sürücüler", f"{last_plate}.png")
            if os.path.exists(image_path):
                img = Image.open(image_path)
                img = img.resize((new_image_width, new_image_height), Image.Resampling.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                image_label.config(image=img_tk)
                image_label.image = img_tk

    info_window.bind("<Configure>", update_labels)

    if last_plate:
        conn = sqlite3.connect("vehicle_info.db")
        c = conn.cursor()
        c.execute("SELECT * FROM vehicle_info WHERE plaka = ?", (last_plate,))
        result = c.fetchone()
        conn.close()

        if result:
            for i, value in enumerate(result[1:]):
                labels[i].config(text=f"{label_texts[i]} {value}")

            image_path = os.path.join("C:\\Users\\Morty\\Desktop\\Plaka Tanima Sistemi\\Sürücüler", f"{last_plate}.png")

            if os.path.exists(image_path):
                img = Image.open(image_path)
                img = img.resize((300, 300), Image.Resampling.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                image_label.config(image=img_tk)
                image_label.image = img_tk
            
        else:
            messagebox.showerror("Hata", f"{last_plate} plakasına ait bilgi bulunamadı.")
    else:
        messagebox.showerror("Hata", "Plaka kayıtı bulunamadı..")
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    show_info_window()
    root.mainloop()

