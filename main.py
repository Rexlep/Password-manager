import customtkinter as ctk
import os
from PIL import ImageTk

from DC.messagebox.CTkMessagebox import CTkMessagebox

tasks = []

def delete_password(task_frame, password):
    task_frame.destroy()
    tasks.remove(task_frame)

    with open('Password.txt', 'r') as file:
        lines = file.readlines()

    with open('Password.txt', 'w') as file:
        for line in lines:
            if line.strip() != password:
                file.write(line)

def toggle_password():
    if password_entry.cget('show') == '*':
        password_entry.configure(show='')
        toggle_button.configure(text='hide')
    else:
        password_entry.configure(show='*')
        toggle_button.configure(text='show')

def write_password():
    with open('Password.txt', "a+") as file:
        file.write(account_entry.get() + ' ' + password_entry.get() + '\n')
        account_entry.delete(0, 'end')
        password_entry.delete(0, 'end')

def copy_password(root, text):
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()
    CTkMessagebox(title="Info", message="The password got copy", icon="info", sound=True)

def read_passwords(task_list_container):

    tasks.clear()

    with open('Password.txt', "r") as file:
        lines = [line.strip() for line in file.readlines()]  # Only read ONCE

    for index, line in enumerate(lines):
        try:
            label, password = line.strip().split(' ')
        except ValueError:
            continue

        password_frame = ctk.CTkFrame(task_list_container, fg_color='transparent')
        password_frame.pack(fill='x', padx=10, pady=2)

        password_label = ctk.CTkLabel(
            password_frame,
            text=f"{label} - {password}",
            font=('Inter', 15),
            anchor="w"
        )
        password_label.pack(side='left', fill='x', expand=True)

        delete_button = ctk.CTkButton(
            password_frame,
            text="✕",
            width=30,
            command=lambda frame=password_frame, line_to_remove=line: delete_password(frame, line_to_remove)
        )
        delete_button.pack(side='right', padx=5)

        copy_button = ctk.CTkButton(
            password_frame,
            text="c",
            width=30,
            command=lambda: copy_password(task_list_container, password)
        )
        copy_button.pack(side='right', padx=5)

        tasks.append(password_frame)

def read_app_password(app_password):
    with open('App_password', "r") as file:
        if app_password == file.readline():
            return True
        return False

def app_password(entry, button1, button2, button3, container):
    if read_app_password(entry.get()):
        entry.destroy()
        entry.destroy()
        button1.destroy()
        button2.destroy()
        button3.destroy()
        read_passwords(container)
        return False
    else:
        CTkMessagebox(title="Error", message="App password is wrong", icon="cancel", sound=True)
        return None

def top_level():

    def top_level_change_password():

        def change_app_password():
            with open('App_password', "w") as file:
                file.write(change_password_top_level_entry.get())
                top_level_window.destroy()
                top_level()

        if top_level_password_entry.get() != '':
            if read_app_password(top_level_password_entry.get()):

                change_password_top_level = ctk.CTkToplevel()
                change_password_top_level.title("Change App Password")
                change_password_top_level.geometry("400x200")
                change_password_top_level.resizable(False, False)
                change_password_top_level.grab_set()

                container = ctk.CTkFrame(change_password_top_level, corner_radius=15)
                container.pack(expand=True, fill='both', padx=20, pady=20)

                change_label = ctk.CTkLabel(container, text="Enter New Password", font=("Arial", 16))
                change_label.pack(pady=(10, 5))

                change_password_top_level_entry = ctk.CTkEntry(container, placeholder_text="New password")
                change_password_top_level_entry.pack(fill='x', expand=True, padx=10, pady=10)

                change_password_top_level_button = ctk.CTkButton(container, text="Change Password", corner_radius=8,  command=change_app_password)
                change_password_top_level_button.pack(pady=(20, 10))

            else:
                CTkMessagebox(title="Error", message="App password is wrong", icon="cancel", sound=True)

        else:
            CTkMessagebox(title="Error", message="Please enter something", icon="cancel", sound=True)

    def toggle_password_top_level():
        if top_level_password_entry.cget('show') == '*':
            top_level_password_entry.configure(show='')
            top_level_password_button_toggle.configure(text='hide')
        else:
            top_level_password_entry.configure(show='*')
            top_level_password_button_toggle.configure(text='show')

    top_level_window = ctk.CTkToplevel()
    top_level_window.title('Passwords')
    top_level_window.geometry('400x400')
    top_level_window.grab_set()

    icon_path = ImageTk.PhotoImage(file=(os.path.join("L.ico")))
    top_level_window.wm_iconbitmap()
    top_level_window.iconphoto(False, icon_path)

    task_list_container = ctk.CTkScrollableFrame(top_level_window, label_text="Passwords", width=350, height=300, corner_radius=10)
    task_list_container.pack(pady=10)

    top_level_password_entry = ctk.CTkEntry(task_list_container, placeholder_text='Enter App password', show='*', height=40)
    top_level_password_entry.pack(pady=10, fill='x', expand=True)

    top_level_password_button = ctk.CTkButton(task_list_container, text="Check", width=50, command=lambda: app_password(
        top_level_password_entry,
        top_level_password_button,
        top_level_password_button_toggle,
        top_level_password_button_change,
        task_list_container))

    top_level_password_button.pack(side="left", pady=10)

    top_level_password_button_toggle = ctk.CTkButton(task_list_container, text="show", width=50, command=toggle_password_top_level)
    top_level_password_button_toggle.pack(side='right', padx=5)

    top_level_password_button_change = ctk.CTkButton(task_list_container, text="Change the password", width=50, command=top_level_change_password)
    top_level_password_button_change.pack(pady=10)


password_manager = ctk.CTk()
password_manager.geometry('400x400')
password_manager.title('Password Manager')
password_manager.resizable(False, False)

try:
    icon_path = ImageTk.PhotoImage(file=(os.path.join("L.ico")))
    password_manager.wm_iconbitmap()
    password_manager.iconphoto(False, icon_path)
except Exception as e:
    print("Icon loading failed:", e)

# Container frame
frame = ctk.CTkFrame(password_manager, corner_radius=15)
frame.pack(pady=40, padx=40, fill="both", expand=True)

# Title
title_label = ctk.CTkLabel(frame, text="🔐 Secure Password Vault", font=("Arial", 20, "bold"))
title_label.pack(pady=(20, 10))

# Account Label and Entry
account_label = ctk.CTkLabel(frame, text="Account (e.g., Google, GitHub)", anchor="w")
account_label.pack(fill="x", padx=10)

account_entry = ctk.CTkEntry(frame, placeholder_text="Enter account name")
account_entry.pack(pady=5, padx=10, fill="x")

# Password Label
password_label = ctk.CTkLabel(frame, text="Password", anchor="w")
password_label.pack(fill="x", padx=10)

# Frame for password entry and show button
password_frame = ctk.CTkFrame(frame, fg_color="transparent")
password_frame.pack(pady=5, padx=10, fill="x")

password_entry = ctk.CTkEntry(password_frame, placeholder_text="Enter your password", show="*")
password_entry.pack(side="left", fill="x", expand=True)

toggle_button = ctk.CTkButton(password_frame, text="show", width=50, command=toggle_password)
toggle_button.pack(side="left", padx=(5, 0))

save_button = ctk.CTkButton(frame, text="💾 Save Password", corner_radius=10, command=write_password)
save_button.pack(pady=20)

show_all_passwords = ctk.CTkButton(frame, text="Show Password", corner_radius=10, command=top_level)
show_all_passwords.pack(pady=5)

password_manager.mainloop()
