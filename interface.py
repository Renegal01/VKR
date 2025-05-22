import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
from PIL import Image, ImageTk


# Function to create heatmaps for each screenshot
def create_heatmaps():
    try:
        subprocess.run(["python", "heat_map.py"], check=True)
    except FileNotFoundError:
        messagebox.showerror("Ошибка", "Файл heat_map.py не найден.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Ошибка", "Произошла ошибка при выполнении heat_map.py.")

# Function to start eyetracking
def start_eyetracking():
    try:
        subprocess.run(["python", "demo.py"], check=True)
    except FileNotFoundError:
        messagebox.showerror("Ошибка", "Файл demo.py не найден.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Ошибка", "Произошла ошибка при выполнении demo.py.")

# Function to show brief instructions in a new fullscreen window
def show_instructions():
    instruction_window = tk.Toplevel()
    instruction_window.title("Инструкция")
    instruction_window.attributes("-fullscreen", False)

    instruction_text = """
    Добро пожаловать в программу для Eyetracking и построения тепловых карт.

    Инструкция по использованию:
    1. Нажмите кнопку 'Начать Eyetracking' для запуска отслеживания взгляда.
    2. Нажмите кнопку 'Построить тепловую карту' для построения тепловой карты по имеющимся данным.
    3. Следуйте инструкциям на экране для дальнейших действий.
    """

    instruction_label = tk.Label(instruction_window, text=instruction_text, justify="left", font=("Arial", 16))
    instruction_label.pack(padx=20, pady=20)

    # Button to exit fullscreen
    exit_button = tk.Button(instruction_window, text="Закрыть", command=instruction_window.destroy, font=("Arial", 14))
    exit_button.pack(pady=20)

# Function to show user settings

# Function to save user settings (placeholder)
def save_settings(sensitivity, heatmap_color):
    messagebox.showinfo("Настройки сохранены", f"Чувствительность: {sensitivity}\nЦвет тепловой карты: {heatmap_color}")

# Create the main interface
def create_main_interface():
    root = tk.Tk()
    root.title("ПО Renegal")
    root.geometry("800x600")

    # Load background image using PIL
    try:
        bg_image = Image.open("background.png")
        bg_image = bg_image.resize((300, 200), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Add background image to a label and place it
        background_label = tk.Label(root, image=bg_photo)
        background_label.image = bg_photo  # Keep a reference to prevent garbage collection
        background_label.place(x=250, y=250, width=300, height=200)
    except FileNotFoundError:
        print("Background image 'background.png' not found.")

    # Button to start eyetracking
    start_button = tk.Button(root, text="Начать Eyetracking для сбора данных", command=start_eyetracking)
    start_button.pack(pady=10)

    # Button to create heatmap
    heatmap_button = tk.Button(root, text="Построить тепловую карту по имеющимся данным", command=create_heatmaps)
    heatmap_button.pack(pady=10)

    # Button to show brief instructions
    instruction_button = tk.Button(root, text="Инструкция по использованию", command=show_instructions)
    instruction_button.pack(pady=10)

    # Version label
    version_label = tk.Label(root, text="Version 1.0", font=("Arial", 10))
    version_label.pack(side="bottom", pady=10)

    # Run the main loop
    root.mainloop()

if __name__ == "__main__":
    create_main_interface()

