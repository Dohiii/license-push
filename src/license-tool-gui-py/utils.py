import requests
import tkinter as tk
import re
from tkinter import filedialog


# Push a new license file to a pod. Since license files are pod specific, this option works with 1 pod at a time.
def push_license(ip, admin_password, path):
    url = f"https://{ip}/Config/service/uploadLicense"
    license_file = {"LICENSE_pkg": open(path, "rb")}
    response = requests.post(
        url, files=license_file, verify=False, auth=admin_password)
    return response


# Function to validate an IPv4 address
def validate_ipv4_input(P):
    # Allow empty input
    if P == "":
        return True

    # Check if the input matches the IPv4 pattern
    ip_pattern = r'^(\d{0,3}\.){0,3}\d{0,3}$'
    return re.match(ip_pattern, P) is not None


# def push_license(ip, admin_password, path):
#     print("Sending license file to Pod. The Pod will reboot after the license is applied.")
#     url = f"https://{ip}/Config/service/uploadLicense"
#     license_file = {"LICENSE_pkg": open(path, "rb")}
#     try:
#         response = requests.post(
#             url, files=license_file, verify=False, auth=admin_password)
#         response_formatted = response.text.split('"')
#         response.raise_for_status()
#         print(response_formatted[-2])

#     except Exception as error:
#         if str(error).split("'")[1] == "Connection aborted.":
#             print("License uploaded and the pod is rebooting to apply the new license.")
#         else:
#             print(error)
#             print("Could not connect to pod.")


# Update widget with information
def update_text_widget(widget, text):
    widget.config(state=tk.NORMAL)  # Enable widget for editing
    widget.delete(1.0, tk.END)  # Clear existing
    widget.insert(tk.END, text)  # Insert new text
    widget.config(state=tk.DISABLED)  # Disable widget for editing
