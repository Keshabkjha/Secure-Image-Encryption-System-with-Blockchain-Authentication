import smtplib
import hashlib
import time
import json
import requests
import os
import getpass
import cv2
import numpy as np
import random
from tkinter import messagebox, simpledialog
from tkinter.filedialog import askopenfilename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Chaotic Maps (for decryption)
def ikeda_map(x, y, u=0.918):
    t = 0.4 - 6 / (1 + x**2 + y**2)
    x1 = 1 + u * (x * np.cos(t) - y * np.sin(t))
    y1 = u * (x * np.sin(t) + y * np.cos(t))
    return x1 % 1, y1 % 1

def circle_map(x, k=0.5):
    return (x + k - (0.5 / (2 * np.pi)) * np.sin(2 * np.pi * x)) % 1

def logistic_map(x, r=3.99):
    return r * x * (1 - x)

# Replace these SMTP credentials with your own
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'developerkeshab@gmail.com'
SENDER_PASSWORD = 'tled wxvd pvir skbc'

def send_otp_email(otp, user_email):
    try:
        subject = "Your OTP for Image Decryption"
        body = f"Your OTP for decryption is: {otp}"
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = user_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, user_email, msg.as_string())
        server.quit()
        print("OTP sent successfully!")
    except Exception as e:
        print(f"Error sending OTP: {e}")
        messagebox.showerror("Email Error", "Failed to send OTP to the email address.")

# Generate Chaotic Matrix for Decryption
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

def retrieve_data_from_hedera(password):
    url = f"http://localhost:3000/get-data?password={password}"
    for attempt in range(10):
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        print(f"Retry attempt {attempt + 1}/10 failed with status: {response.status_code}, response: {response.text}")
        time.sleep(5)
    print("❌ Failed to retrieve data from Hedera after retries")
    return None

def validate_password(user_password, stored_user_hash):
    user_password_hash = hashlib.sha256(user_password.encode()).hexdigest()
    return user_password_hash == stored_user_hash

def request_user_otp():
    return simpledialog.askstring("OTP Verification", "Enter the OTP sent to your email:")

def decrypt_region(region, chaotic_region):
    """Decrypt a region using the inverse of the encryption operations."""
    # Convert to int32 for proper arithmetic
    decrypted = region.astype(np.int32)
    h, w = region.shape
    
    # Step 1: Subtract the chaotic values (reverse of addition in encryption)
    decrypted = (decrypted - chaotic_region) % 256
    
    # Step 2: Reverse column shifts
    col_shifts = (chaotic_region[0, :] % h).astype(int)
    row_indices = (np.arange(h)[:, None] - col_shifts[None, :]) % h
    decrypted = decrypted[row_indices, np.arange(w)[None, :]]
    
    # Step 3: Reverse row shifts
    row_shifts = (chaotic_region[:, 0] % w).astype(int)
    col_indices = (np.arange(w)[None, :] - row_shifts[:, None]) % w
    decrypted = decrypted[np.arange(h)[:, None], col_indices]
    
    return decrypted.astype(np.uint8)

def process_segmented_decryption(image_path, data):
    # Read image in color to handle all channels
    encrypted_img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if encrypted_img is None:
        print("Failed to load image")
        return None
        
    height, width = encrypted_img.shape[:2]
    decrypted_img = np.zeros_like(encrypted_img)

    for region, key in zip(data["regions"], data["chaoticKeys"]):
        x1 = int(region['x1'])
        y1 = int(region['y1'])
        x2 = int(region['x2'])
        y2 = int(region['y2'])
        
        # Extract the region from the image
        segment = encrypted_img[y1:y2, x1:x2]
        
        # Generate the same chaotic region used during encryption
        h, w = segment.shape[:2]
        chaotic_region = generate_chaotic_matrix(h, w, key)
        
        # Decrypt the region
        if len(segment.shape) == 3:  # Color image
            # Decrypt each channel separately
            decrypted_region = np.zeros_like(segment)
            for c in range(3):
                decrypted_region[:, :, c] = decrypt_region(segment[:, :, c], chaotic_region)
        else:  # Grayscale
            decrypted_region = decrypt_region(segment, chaotic_region)
            
        # Place the decrypted region back
        decrypted_img[y1:y2, x1:x2] = decrypted_region

    return decrypted_img

def save_decrypted_image(image):
    cv2.imwrite("decrypted_image.png", image)

def decrypt_image(user_password, otp_from_user, data):
    if otp_from_user != data.get("otp"):
        messagebox.showerror("Invalid OTP", "The OTP entered is incorrect!")
        return
    if not validate_password(user_password, data["userHash"]):
        messagebox.showerror("Invalid Password", "The password entered is incorrect!")
        return
    image_path = askopenfilename(title="Select Encrypted Image", filetypes=[("PNG Files", "*.png")])
    if not image_path:
        messagebox.showerror("Error", "❌ No file selected.")
        return
    decrypted_image = process_segmented_decryption(image_path, data)
    if decrypted_image is not None:
        save_decrypted_image(decrypted_image)
        messagebox.showinfo("Success", "Image decrypted and saved as 'decrypted_image.png'")
    else:
        messagebox.showerror("Error", "Decryption failed due to image processing error.")

def start_decryption():
    user_password = simpledialog.askstring("Password", "Enter your password to start decryption:")
    if not user_password:
        messagebox.showerror("Error", "Password is required.")
        return

    # Retrieve data from Hedera using only the password
    data = retrieve_data_from_hedera(user_password)
    if not data:
        messagebox.showerror("Error", "Failed to retrieve data from Hedera.")
        return

    user_email = data.get("email")
    otp = data.get("otp")
    if not user_email or not otp:
        messagebox.showerror("Error", "Email or OTP not found in Hedera data.")
        return

    send_otp_email(otp, user_email)
    otp_from_user = request_user_otp()
    if not otp_from_user:
        messagebox.showerror("Error", "No OTP entered.")
        return

    decrypt_image(user_password, otp_from_user, data)

# Uncomment to run decryption
start_decryption()
