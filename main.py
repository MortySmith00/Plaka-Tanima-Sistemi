import tkinter as tk
import cv2
from PIL import Image, ImageTk
import imutils
import numpy as np
import easyocr
import sqlite3
from datetime import datetime, timedelta
import re
from tkinter import messagebox
import os
from info_window import show_info_window

conn = sqlite3.connect("recognized_plates.db")
c = conn.cursor()
reader = easyocr.Reader(['en'], gpu=True)
plaka_cache = {}

class Save:
    @staticmethod
    def write(plate):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO plates (plate, timestamp) VALUES (?, ?)", (plate, timestamp))
        conn.commit()
        print(f"Plaka: {plate}, Zaman: {timestamp} veritabanına kaydedildi.")

save = Save()

def plaka_kontrol(plate):
    simdiki_zaman = datetime.now()
    
    if plate in plaka_cache and (simdiki_zaman - plaka_cache[plate]) < timedelta(seconds=10):
        print(f"{plate} plakası 10 saniye içinde zaten kaydedildi. Veritabanına yazılmadı.")
        return False
    else:
        plaka_cache[plate] = simdiki_zaman
        return True

def process_plate(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 9, 75, 75)
    edged = cv2.Canny(gray, 50, 150)
    
    try:
        cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
        screenCnt = None

        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.017 * peri, True)
            if len(approx) == 4:
                screenCnt = approx
                break

        if screenCnt is None:
            return img

        cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)

        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1)
        new_image = cv2.bitwise_and(img, img, mask=mask)

        (x, y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        Cropped = gray[topx:bottomx + 1, topy:bottomy + 1]

        text = reader.readtext(Cropped)
        if text:
            text = text[0][1].replace(" ", "").upper()

            if re.match("^[A-Z0-9]+$", text):
                if len(text) >= 6:
                    if plaka_kontrol(text):
                        save.write(text)
            else:
                print(f"Geçersiz plaka: {text}")

    except Exception as e:
        print("Hata: ", e)
    
    return img

def get_last_plate():
    c.execute("SELECT plate FROM plates ORDER BY timestamp DESC LIMIT 1")
    result = c.fetchone()
    if result:
        return result[0]
    return None

def remove_transparency(image):
    if image.mode == 'RGBA':
        background = Image.new("RGBA", image.size, (169, 169, 169, 255))
        background.paste(image, mask=image.split()[3])
        return background.convert("RGB")
    return image

def show_login_logs():
  
    logs_window = tk.Toplevel()
    logs_window.title("Geçmiş Giriş Kayıtları")
    logs_window.geometry("600x400")
    text_box = tk.Text(logs_window, wrap=tk.WORD)
    text_box.pack(expand=True, fill=tk.BOTH)
    text_box.insert(tk.END, f"{'ID':<5} {'Kullanıcı Adı':<20} {'Giriş Zamanı':<25}\n")
    text_box.insert(tk.END, "-" * 60 + "\n") 

    try:
        conn_users = sqlite3.connect("users.db")
        c_users = conn_users.cursor()
        c_users.execute("SELECT * FROM login_logs")
        logs = c_users.fetchall()

        for log in logs:
            text_box.insert(tk.END, f"{log[0]:<5} {log[1]:<20} {log[2]:<25}\n")
        conn_users.close()
    except sqlite3.Error as e:
        messagebox.showerror("Hata", f"Veritabanı hatası: {e}")

def show_plate_logs():
    plate_logs_window = tk.Toplevel()
    plate_logs_window.title("Geçmiş Araç İzlencesi")
    plate_logs_window.geometry("600x400")
    text_box = tk.Text(plate_logs_window, wrap=tk.WORD)
    text_box.pack(expand=True, fill=tk.BOTH)
    text_box.insert(tk.END, f"{'ID':<5} {'Plaka':<15} {'Zaman':<25}\n")
    text_box.insert(tk.END, "-" * 50 + "\n")

    try:
        conn_plates = sqlite3.connect("recognized_plates.db")
        c_plates = conn_plates.cursor()

        c_plates.execute("SELECT id, plate, timestamp FROM plates ORDER BY timestamp DESC")
        plate_logs = c_plates.fetchall()

        if not plate_logs:
            text_box.insert(tk.END, "No data available.\n")

        for log in plate_logs:
            text_box.insert(tk.END, f"{log[0]:<5} {log[1]:<15} {log[2]:<25}\n")

        conn_plates.close()
    except sqlite3.Error as e:
        messagebox.showerror("Hata", f"Veritabanı hatası: {e}")

def create_gui():
    root = tk.Tk()
    root.geometry("1400x900")
    root.configure(bg="#A9A9A9")
    root.title("Main")
    button_style = {
        'bg': "#003366", 'fg': "white", 'font': ("Helvetica", 14, "bold"),
        'relief': "raised", 'bd': 5, 'highlightthickness': 0,
        'activebackground': "#00509E", 'activeforeground': "white",
        'width': 20, 'height': 2, 'overrelief': "sunken",
                   }

    button1 = tk.Button(root, text="Geçmiş Görevli İzlencesi", **button_style, command=show_login_logs)
    button2 = tk.Button(root, text="Geçmiş Araç İzlencesi", **button_style, command=show_plate_logs)
    button3 = tk.Button(root, text="Bilgileri Gör", **button_style, command=show_info_window)
    camera_label = tk.Label(root)
    camera_label.place(x=457, y=196, width=486, height=451)
    image_label1 = tk.Label(root)
    image_label2 = tk.Label(root)
    plaka_label = tk.Label(root, text="", bg="white", fg="black", 
                            font=("Helvetica", 14, "bold"), relief="flat", bd=0)

    original_image = remove_transparency(Image.open("Uygulama Görselleri//history.png"))

    label = tk.Label(root, text="Canlı Kamera", bg="white", fg="black", 
                     font=("Helvetica", 14, "bold"), relief="flat", bd=0)

    def on_window_resize(event):
        new_width, new_height = root.winfo_width(), root.winfo_height()

        button1.place(x=int(90 * (new_width / 1400)), y=int(391 * (new_height / 900)),
                      width=int(247 * (new_width / 1400)), height=int(118 * (new_height / 900)))
        button2.place(x=int(1063 * (new_width / 1400)), y=int(391 * (new_height / 900)),
                      width=int(247 * (new_width / 1400)), height=int(118 * (new_height / 900)))
        button3.place(x=int(575 * (new_width / 1400)), y=int(730 * (new_height / 900)),
                      width=int(250 * (new_width / 1400)), height=int(80 * (new_height / 900)))
        camera_label.place(x=int(457 * (new_width / 1400)), y=int(196 * (new_height / 900)),
                            width=int(486 * (new_width / 1400)), height=int(451 * (new_height / 900)))
        label.place(x=int(575 * (new_width / 1400)), y=int(90 * (new_height / 900)),
                    width=int(250 * (new_width / 1400)), height=int(43.5 * (new_height / 900)))
        plaka_label.place(x=int(575 * (new_width / 1400)), y=int(665 * (new_height / 900)),
                          width=int(250 * (new_width / 1400)), height=int(43.5 * (new_height / 900)))

        image1_width = int(128.5 * (new_width / 1400))
        image1_height = int(111 * (new_height / 900))
        image2_width = int(128.5 * (new_width / 1400))
        image2_height = int(111 * (new_height / 900))
        resized_image1 = original_image.resize((image1_width, image1_height))
        img1 = ImageTk.PhotoImage(resized_image1)
        image_label1.img = img1
        image_label1.config(image=img1)
        image_label1.place(x=int(149 * (new_width / 1400)), y=int(239 * (new_height / 900)),
                           width=image1_width, height=image1_height)

        resized_image2 = original_image.resize((image2_width, image2_height))
        img2 = ImageTk.PhotoImage(resized_image2)
        image_label2.img = img2
        image_label2.config(image=img2)
        image_label2.place(x=int(1122 * (new_width / 1400)), y=int(239 * (new_height / 900)),
                           width=image2_width, height=image2_height)

    cap = cv2.VideoCapture(0)
    def show_frame():
        ret, frame = cap.read()
        if ret:

            frame = process_plate(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            new_width = camera_label.winfo_width()
            new_height = camera_label.winfo_height()
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            imgtk = ImageTk.PhotoImage(image=img)
            camera_label.imgtk = imgtk
            camera_label.configure(image=imgtk)
            last_plate = get_last_plate()
            if last_plate:
                plaka_label.config(text=f"Plaka: {last_plate}")

        camera_label.after(10, show_frame)

    show_frame()
    root.bind("<Configure>", on_window_resize)
    root.mainloop()
    cap.release()
    conn.close()

create_gui()