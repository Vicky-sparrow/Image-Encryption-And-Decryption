import tkinter
from tkinter import *
import tkinter as tk
import tkinter.messagebox as mbox
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
import cv2
import os
import numpy as np
from cv2 import *
import random
import ast

# defined variable
global count, emig, counter

panelB = None
panelA = None
counter = 0

# function defined to get the path of the image selected
def getpath(path):
    a = path.split(r'/')
    # print(a)
    fname = a[-1]
    l = len(fname)
    location = path[:-l]
    return location

# function defined to get the folder name from which image is selected
def getfoldername(path):
    a = path.split(r'/')
    # print(a)
    name = a[-1]
    return name

# function defined to get the file name of image is selected
def getfilename(path):
    a = path.split(r'/')
    fname = a[-1]
    a = fname.split('.')
    a = a[0]
    return a

# function defined to open the image file
def openfilename():
    filename = filedialog.askopenfilename(title='"pen')
    return filename

def open_image():
    global x, panelA, panelB
    global count, eimg, location, filename
    count = 0
    x = openfilename()
    img = Image.open(x)
    # Resize the image (replace with your desired width and height)
    img = img.resize((320, 260), Image.LANCZOS)
    eimg = img
    img = ImageTk.PhotoImage(img)
    temp = x
    location = getpath(temp)
    filename = getfilename(temp)
    # print(x)
    if panelA is None or panelB is None:
        panelA = tk.Label(image=img, bg="black")
        panelA.image = img
        panelA.place(x=20, y=90)
        panelB = tk.Label(image="", bg="black")  # Fix: initialize panelB with the image
        panelB.image = img
        panelB.place(x=358, y=88)
    else:
        panelA.configure(image=img)
        panelB.configure(image="")
        panelA.image = img

# function defined to make the image sharp
def decrypt():
    global image_encrypted, key, panelA, panelB, filename
    counter = filename[6:]
    key = np.load(f'NPY/key_features_{counter}.npy')
    image_encrypted = np.load(f'NPY/encryption_details_{counter}.npy')

    image_output = image_encrypted * key
    image_output *= 255.0
    filename = f'Decrypt/Image_{counter}.jpg'
    cv2.imwrite(filename, image_output)

    imgd = Image.open(filename)
    imgd = ImageTk.PhotoImage(imgd)
    panelB.configure(image=imgd)
    panelB.image = imgd
    mbox.showinfo("Status", "Image Decrypted Successfully.")

# function defined to same the edited image
def save_img():
    global location, filename, eimg
    print(filename)
    filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
    if not filename:
        return
    eimg.save(filename)
    mbox.showinfo("Success", "Image Saved Successfully!")

# function defined to reset the edited image to original one
def reset():
    panelA.configure(image="")
    panelB.configure(image="")
    mbox.showinfo("Success", "Reset Successfully! Now you can Decrypt Image ..")

def exit():
    root.destroy()

# GUI Setup
root = tk.Tk()
root.title("Cloud Storage System")
root.geometry("700x600+150+180")
root.resizable(False, False)
root.configure(bg="#009ACD")

# Icon
image_icon = tk.PhotoImage(file="logo.png")
root.iconphoto(False, image_icon)

# Logo
logo = PhotoImage(file="logo.png")
Label(root, image=logo, bg='#009ACD').place(x=30, y=10)

Label = tk.Label(root, text="IMAGES IN CLOUD STORAGE SYSTEM", bg="#009ACD", fg="white", font="arial 20 bold")
Label.place(x=100, y=16)

first_frame = tk.Frame(root, bd=3, bg="black", width=340, height=280, relief="groove")
first_frame.place(x=10, y=80)

first_frame = tk.Frame(root, bd=3, bg="black", width=340, height=280, relief="groove")
first_frame.place(x=350, y=80)

browse_button = tk.Button(root, text="Browse Image", width=12, height=2, font="arial 14 bold", command=open_image)
browse_button.place(x=100, y=380)

decrypt_button = tk.Button(root, text="Decrypt", width=12, height=2, font="arial 14 bold", command=decrypt)
decrypt_button.place(x=440, y=380)

reset = tk.Button(root, text="Reset", width=12, height=2, font="arial 14 bold", command=reset)
reset.place(x=190, y=500)

exit = tk.Button(root, text="Exit", width=12, height=2, font="arial 14 bold", command=exit)
exit.place(x=360, y=500)

root.mainloop()
