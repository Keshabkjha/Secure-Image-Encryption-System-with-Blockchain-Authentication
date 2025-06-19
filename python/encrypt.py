# encrypt.py

import tkinter as tk
from tkinter import filedialog, messagebox, Canvas, Frame, Button, simpledialog
from PIL import Image, ImageTk
import cv2
import numpy as np
import os
import json
import requests
import time
import hashlib
import random
from ultralytics import YOLO

# Chaotic Maps
def ikeda_map(x, y, u=0.918):
    t = 0.4 - 6 / (1 + x**2 + y**2)
    x1 = 1 + u * (x * np.cos(t) - y * np.sin(t))
    y1 = u * (x * np.sin(t) + y * np.cos(t))
    return x1 % 1, y1 % 1

def circle_map(x, k=0.5):
    return (x + k - (0.5 / (2 * np.pi)) * np.sin(2 * np.pi * x)) % 1

def logistic_map(x, r=3.99):
    return r * x * (1 - x)

# Hashing and OTP
def hash_string(s):
    return hashlib.sha256(s.encode()).hexdigest()

def generate_otp():
    return ''.join(random.choices('0123456789', k=6))

def generate_combined_hash(user_hash, otp_hash):
    return hashlib.sha256((user_hash + otp_hash).encode()).hexdigest()

# Chaotic Matrix Generator
def generate_chaotic_matrix(height, width, combined_hash):
    seed = int(combined_hash[:16], 16)
    random.seed(seed)
    x = random.random()
    y = random.random()
    k = random.random()
    r = 3.99

    chaotic_values = []
    for _ in range(height * width):
        x, y = ikeda_map(x, y)
        x = circle_map(x, k)
        x = logistic_map(x, r)
        chaotic_values.append(int(x * 255) % 256)

    chaotic_matrix = np.array(chaotic_values, dtype=np.uint8).reshape(height, width)
    return chaotic_matrix

# Encryption
def encrypt_region_multichannel(region, chaotic_region):
    h, w, c = region.shape
    encrypted = region.copy().astype(np.int32)

    row_shifts = (chaotic_region[:, 0] % w).astype(int)
    col_indices = (np.arange(w)[None, :] + row_shifts[:, None]) % w
    encrypted = encrypted[np.arange(h)[:, None], col_indices, :]

    col_shifts = (chaotic_region[0, :] % h).astype(int)
    row_indices = (np.arange(h)[:, None] + col_shifts[None, :]) % h
    encrypted = encrypted[row_indices, np.arange(w)[None, :], :]

    encrypted = (encrypted + chaotic_region[:, :, None]) % 256
    return encrypted.astype(np.uint8)

# Store Data on Blockchain
def store_data_on_blockchain(email, otp, user_hash, combined_hash, region_keys, regions):
    url = "http://localhost:3000/store-data"
    data = {
        "email": email,
        "otp": otp,
        "userHash": user_hash,
        "combinedHash": combined_hash,
        "chaoticKeys": [str(key) for key in region_keys],
        "regions": regions
    }
    response = requests.post(url, json=data)
    print(f"Storing data on blockchain: {data}")
    if response.status_code == 200:
        return True
    else:
        print("❌ Blockchain Error:", response.text)
        return False

# Segment image using YOLO
def segment_image(image_path):
    model = YOLO("yolo11n-seg.pt")
    results = model(image_path)
    return results

# Main processing logic
def process_segmented_encryption(image_path, email, password):
    try:
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Image loading failed!")

        results = segment_image(image_path)
        encrypted_image = img.copy()
        region_keys = []
        encrypted_regions = []
        regions = []

        for i, cls in enumerate(results[0].boxes.cls):
            if int(cls) == 0:
                x1, y1, x2, y2 = map(int, results[0].boxes.xyxy[i].cpu().numpy())
                regions.append((i, x1, y1, x2, y2))

        # Sort & adjust overlapping regions
        regions.sort(key=lambda x: x[1])
        adjusted_regions = []
        prev_x2 = -1
        for i, x1, y1, x2, y2 in regions:
            if x1 < prev_x2:
                x1 = prev_x2
            if x1 < x2:
                adjusted_regions.append((i, x1, y1, x2, y2))
                prev_x2 = x2

        otp = generate_otp()
        user_hash = hash_string(password)
        otp_hash = hash_string(otp)
        combined_hash = generate_combined_hash(user_hash, otp_hash)

        for i, x1, y1, x2, y2 in adjusted_regions:
            region = encrypted_image[y1:y2, x1:x2].copy()
            chaotic_region = generate_chaotic_matrix(region.shape[0], region.shape[1], combined_hash)
            encrypted = encrypt_region_multichannel(region, chaotic_region)
            encrypted_image[y1:y2, x1:x2] = encrypted
            region_keys.append(combined_hash)
            encrypted_regions.append({"x1": x1, "y1": y1, "x2": x2, "y2": y2})

        success = store_data_on_blockchain(email, otp, user_hash, combined_hash, region_keys, encrypted_regions)
        if success:
            print("✅ Data stored successfully on Hedera.")
            time.sleep(5)

        return encrypted_image

    except Exception as e:
        messagebox.showerror("Error", f"Encryption failed: {e}")
        print(f"[ERROR] {e}")
        return None

# GUI actions
def save_encrypted_image(image, path):
    cv2.imwrite(path, image)

def display_image(image, canvas):
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)
    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
    canvas.image = img_tk

def open_image():
    file_path = filedialog.askopenfilename(title="Select Image")
    if file_path:
        email = simpledialog.askstring("Input", "Enter Email:")
        password = simpledialog.askstring("Input", "Enter Password:", show='*')
        if email and password:
            global encrypted_image
            encrypted_image = process_segmented_encryption(file_path, email, password)
            if encrypted_image is not None:
                display_image(encrypted_image, encrypted_canvas)
        else:
            messagebox.showwarning("Warning", "Email and password are required.")

def save_image():
    if encrypted_image is not None:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            title="Save Encrypted Image",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if file_path:
            save_encrypted_image(encrypted_image, file_path)
            messagebox.showinfo("Success", "Encrypted image saved!")

# GUI Setup
root = tk.Tk()
root.title("Segmented Image Encryption")
root.geometry("850x450")

Button(root, text="Open Image", command=open_image).pack(pady=5)
Button(root, text="Save Encrypted Image", command=save_image).pack(pady=5)

frame = Frame(root)
frame.pack()

encrypted_canvas = Canvas(frame, width=350, height=350, bg="lightgray")
encrypted_canvas.pack(side=tk.RIGHT, padx=10)

encrypted_image = None

root.mainloop()
