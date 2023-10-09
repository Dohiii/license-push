import customtkinter
from tkinter import filedialog
import tkinter as tk
from utils import push_license, validate_ipv4_input


# Description for argparse help.
tool_description = "This tool allows sending Solstice license files to Pods. To receive your license file please " \
                   "contact Mersive support support@mersive.com."


# Utils and constants
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("green")
loading = False


def start_loading_animation():
    global loading
    loading = True
    animate_loading()


def animate_loading():
    if loading:
        push_button.configure(text="Loading.")
        root.after(500, lambda: animate_loading())
        push_button.update_idletasks()  # Update the push_button display
    else:
        push_button.configure(text="Start Loading")


def stop_loading_animation():
    global loading
    loading = False
    push_button.configure(text="Push license")


# Function to start the license push process
def push_license_button_clicked():
    print("Clicked")
    animate_loading()
    ip_address = ip_entry.get()
    password = password_entry.get()
    file_path = file_entry.get()
    try:
        response = push_license(
            ip=ip_address, admin_password=password, path=file_path)
        # response_formatted = response.text.split('"')
        # response.raise_for_status()
        # update_text_widget(
        #     f" \n License file Pushed to the Pod with ip adress IP Address: {ip_address} \n ")
        # print(response_formatted[-2])
        # print(response_formatted)
    except Exception as error:
        if str(error).split("'")[1] == "Connection aborted.":
            update_text_widget(
                " \n License uploaded and the pod is rebooting to apply the new license.\n ")
        else:
            update_text_widget(error)
            update_text_widget(" \n Could not connect to the Pod. \n")
    finally:
        stop_loading_animation()
        print("Finally")


# Browse file to app
def browse_file_func():
    file_path = filedialog.askopenfilename(
        filetypes=[("BIM Files", "*.bim")], initialdir="./", title="Select a .bim file")
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)


# Update widget with information
def update_text_widget(text):
    text_widget.config(state=tk.NORMAL)  # Enable text widget for editing
    # text_widget.delete(1.0, tk.END)  # Clear existing text
    text_widget.insert(tk.END, text)  # Insert new text
    text_widget.config(state=tk.DISABLED)  # Disable text widget for editing


# Update widget with information
def update_button_load_toggle(text):
    push_button.config(state=tk.NORMAL)  # Enable text widget for editing
    push_button.delete(1.0, tk.END)  # Clear existing text
    push_button.insert(tk.END, text)  # Insert new text
    push_button.config(state=tk.DISABLED)  # Disable text widget for editing


root = customtkinter.CTk()
root.title("License Tool")
# Increased window height to accommodate the text field
root.geometry("570x250")

# IP Address Entry with validation
ip_label = customtkinter.CTkLabel(root, text="IP address:")
ip_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

# Validation function to allow only valid IPv4 addresses
validate_ipv4_func = root.register(validate_ipv4_input)
ip_entry = customtkinter.CTkEntry(
    root, validate="key", validatecommand=(validate_ipv4_func, "%P"))
ip_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

# Password Entry
password_label = customtkinter.CTkLabel(root, text="Pod password:")
password_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

password_entry = customtkinter.CTkEntry(root, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

# File Entry on the right
file_label = customtkinter.CTkLabel(root, text="Path to License file:")
file_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")

file_entry = customtkinter.CTkEntry(root)
file_entry.grid(row=0, column=3, padx=10, pady=5, sticky="w")

# Browse Button under the file input field on the right
browse_button = customtkinter.CTkButton(
    root, text="Browse", command=browse_file_func)
browse_button.grid(row=1, column=3, padx=10, pady=5, sticky="w")

# Push License button in the middle
button_frame = tk.Frame(root)
button_frame.grid(row=2, column=0, columnspan=4, pady=20)

push_button = customtkinter.CTkButton(
    button_frame, text="Push License", command=push_license_button_clicked)
push_button.pack()

# Text Field below the "Push License" button that stretches horizontally
text_widget = tk.Text(root, height=3, wrap=tk.WORD)
text_widget.grid(row=3, column=0, columnspan=4, padx=10, pady=5, sticky="nsew")
text_widget.config(state=tk.DISABLED)  # Disable text widget for editing

# Make the text field stretch horizontally and vertically
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)

root.mainloop()
