import tkinter as tk
from tkinter import messagebox
import pywhatkit as kit
import pyautogui
import random
import time
import os


# Global dictionaries for messages and location info
messages = {
    "Call Again": ["Please call again.", "Can you call back later?", "We missed your call. Please call again."],
    "Daily Message": ["This is your daily message reminder.", "Reminder for today’s task.",
                      "Here’s your daily update."],
    "Follow-up": ["This is a follow-up message.", "Just following up on our last conversation.",
                  "Following up on your request."],
    "Get a Call Back": ["Please call me back.", "I would appreciate a call back.", "Could you return my call?"],
    "Didn't Pick the Call": [
        "Missed our call? 😊 No problem! Please reach out via "
        "call or WhatsApp at +91****9899. 💪🌟\n"
        "हमारे कॉल को मिस कर दिया? 😊 कोई बात नहीं! कॉल या WhatsApp पर संपर्क करें: +91****9899। 💪 "

    ],

    "Confirmation Pending": [
        "Pending", "Wait time is longer than usual"
    ],
    "Out of Service": ["We are currently out of service.", "Our service is temporarily unavailable.",
                       "We’re out of service right now."],
    "Offers and Festive": ["🎉 Special Offers! 🎉"]
}

category_folders = {
    "Call Again": r"path of image",
    "Daily Message": r"path of image",
    "Follow-up": r"path of image",
    "Get a Call Back": r"path of image",
    "Didn't Pick the Call": r"path of image",
    "Confirmation Pending": r"path of image",
    "Out of Service": r"path of image",
    "Offers and Festive": r"path of image"
}

location_info = {
    "Bangalore": {
        "address": "BTM Stage 1,  560029",
        "map_link": "https://maps.app.goo.gl/TsSo35YVv7sMDzmRA"
    },
    "Delhi": {
        "address": "Beta 2, Greater Noida",
        "map_link": "https://maps.app.goo.gl/vD4KXQ8JNHn4TFzq9"
    },
    "Mumbai": {
        "address": "Bombay Stock Exchange",
        "map_link": "https://maps.app.goo.gl/k2GDqV7AnxQcLyGF7"
    },
    "Explore All": {
        "address": "",
        "map_link": ""
    }
}


# Function to send the WhatsApp message
def send_message(immediate=True):
    numbers, category, location = get_user_inputs()
    image_file = category_folders.get(category)

    if not numbers:
        messagebox.showerror("Input Error", "Please enter at least one phone number")
        return

    message = get_message_to_send(category, location)

    for number in numbers:
        if number:
            try:
                send_to_number(number, image_file, message, immediate)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while sending to {number}: {e}")


# Function to retrieve and clean user inputs
def get_user_inputs():
    numbers = phone_entry.get().strip().split(",")
    numbers = [num.strip() for num in numbers if num.strip()]
    category = category_var.get()
    location = location_var.get() if category == "Location" else None
    return numbers, category, location


# Function to generate the message content
def get_message_to_send(category, location):
    if category == "Location" and location:
        location_details = location_info.get(location, {})
        address = location_details.get("address", "Address not available")
        # print(location_details,address, location)
        if location == "Explore All":

            text = "🌟 Hi! 🌟\n\n🏥 Locations and Addresses:\n1️⃣ " \
                   "BTM Stage 1,  560029\n🗺️ " \
                   "https://maps.app.goo.gl/TsSo35YVv7sMDzmRA\n\n2️⃣ Beta 2, Greater Noida " \
                   "\n🗺️ https://maps.app.goo.gl/vD4KXQ8JNHn4TFzq9\n\n3️⃣ Bombay Stock Exchange \n🗺️ " \
                   "https://maps.app.goo.gl/k2GDqV7AnxQcLyGF7\n\n4\n\nWe're here to care for you every step of the " \
                   "way! 🌼 "
            return text
        else:
            address = location_details.get("address", "Address not available")
            map_link = location_details.get("map_link", "https://www.google.com/maps")
            return f"Address: {address}\nGoogle Maps Link: {map_link}\n\nRegards\nAkash Singh\nhttps://medium.com/@akashsingh9303"
    elif category in messages:
        return random.choice(messages[category])
    return "No message selected."


# Function to handle the sending process to each number
def send_to_number(number, image_file, message, immediate):
    if image_file and os.path.exists(image_file):
        kit.sendwhats_image(f"+{number}", image_file, caption=message)
        time.sleep(10)
        pyautogui.press('enter')
        time.sleep(5)
    else:
        if immediate:
            kit.sendwhatmsg_instantly(f"+{number}", message)
            time.sleep(10)
            pyautogui.press('enter')
        else:
            schedule_message(number, message)


# Function to schedule a message
def schedule_message(number, message):
    time_hour = hour_entry.get()
    time_minute = minute_entry.get()
    if not time_hour or not time_minute:
        messagebox.showerror("Input Error", "Please enter the time to schedule the message")
        return
    kit.sendwhatmsg(f"+{number}", message, int(time_hour), int(time_minute))
    time.sleep(10)
    pyautogui.press('enter')
    messagebox.showinfo("Success", f"Message scheduled for {time_hour}:{time_minute} to {number}!")


# Function to show or hide time input fields based on selection
def show_time_input():
    if option_var.get() == "Schedule Message":
        time_frame.pack(pady=10)
    else:
        time_frame.pack_forget()


# Function to show or hide location dropdown based on category selection
def update_location_dropdown(*args):
    if category_var.get() == "Location":
        location_frame.pack(pady=10)
    else:
        location_frame.pack_forget()


# Function to create and place all UI components
def create_ui():
    # Main application window setup
    app.title("WhatsApp Automation")
    app.geometry("800x600")
    app.configure(bg="#e0f7fa")

    # Create the main frame
    main_frame = tk.Frame(app, bg="#ffffff", padx=20, pady=20, borderwidth=2, relief="groove")
    main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    # Title Label
    title_label = tk.Label(main_frame, text="WhatsApp Automation", font=("Helvetica", 18, "bold"), bg="#ffffff",
                           fg="#006064")
    title_label.pack(pady=10)

    # Phone number input
    create_phone_number_input(main_frame)

    # Category selection
    create_category_selection(main_frame)

    # Option selection
    create_option_selection(main_frame)

    # Time input fields
    create_time_input_fields(main_frame)

    # Buttons for sending messages
    create_buttons(main_frame)


# Function to create phone number input fields
def create_phone_number_input(parent_frame):
    phone_label = tk.Label(parent_frame, text="Enter Phone Numbers (with country code, comma-separated):", bg="#ffffff",
                           font=("Helvetica", 12), fg="#004d40")
    phone_label.pack(pady=10)
    global phone_entry
    phone_entry = tk.Entry(parent_frame, width=80, font=("Helvetica", 12), fg="#000000", bg="#b2dfdb")
    phone_entry.pack(pady=5)


# Function to create category selection fields
def create_category_selection(parent_frame):
    global category_var, location_var, location_frame
    category_var = tk.StringVar(value="Select Category")
    category_var.trace("w", update_location_dropdown)

    category_label = tk.Label(parent_frame, text="Select Message Category:", bg="#ffffff", font=("Helvetica", 12),
                              fg="#004d40")
    category_label.pack(pady=10)

    category_menu = tk.OptionMenu(parent_frame, category_var, *messages.keys(), "Location")
    category_menu.config(font=("Helvetica", 12), fg="#004d40", bg="#b2dfdb")
    category_menu.pack(pady=5)

    location_var = tk.StringVar(value="Select Location")
    location_frame = tk.Frame(parent_frame, bg="#ffffff")

    location_label = tk.Label(location_frame, text="Select Location:", bg="#ffffff", font=("Helvetica", 12),
                              fg="#004d40")
    location_label.pack(pady=5)

    location_menu = tk.OptionMenu(location_frame, location_var, *location_info.keys())
    location_menu.config(font=("Helvetica", 12), fg="#004d40", bg="#b2dfdb")
    location_menu.pack(pady=5)


# Function to create option selection fields
def create_option_selection(parent_frame):
    global option_var, options_frame
    option_var = tk.StringVar(value="Select Option")

    options_frame = tk.Frame(parent_frame, bg="#ffffff")
    options_frame.pack(pady=10)

    main_options = ["Send Immediate", "Schedule Message"]
    for option in main_options:
        button = tk.Radiobutton(options_frame, text=option, variable=option_var, value=option, bg="#ffffff",
                                font=("Helvetica", 12), fg="#004d40", command=show_time_input)
        button.pack(anchor=tk.W, pady=5)


# Function to convert hex to string
def hex_to_str(hex_str):
    bytes_object = bytes.fromhex(hex_str)
    return bytes_object.decode("ASCII")


# Function to create time input fields
def create_time_input_fields(parent_frame):
    global time_frame, hour_entry, minute_entry
    time_frame = tk.Frame(parent_frame, bg="#ffffff")

    time_hour_label = tk.Label(time_frame,
                               text="Hour (24-hour format):\nNote:- Please avoid using the scheduled format,"
                                    "\nas image automation doesn't support it.\nWe are sending images along with the "
                                    "messages.", bg="#ffffff", font=("Helvetica", 12), fg="#004d40")
    time_hour_label.pack(pady=5)

    hour_entry = tk.Entry(time_frame, width=5, font=("Helvetica", 12), fg="#000000", bg="#b2dfdb")
    hour_entry.pack(pady=5)

    time_minute_label = tk.Label(time_frame, text="Minute:", bg="#ffffff", font=("Helvetica", 12), fg="#004d40")
    time_minute_label.pack(pady=5)

    minute_entry = tk.Entry(time_frame, width=5, font=("Helvetica", 12), fg="#000000", bg="#b2dfdb")
    minute_entry.pack(pady=5)

    # hex_string = "44657369676E6564202620446576656C6F7065642042793A204A696779617368612050617468616B0A646F63636F6D706" \
    #              "173730A68747470733A2F2F7777772E646F63636F6D706173732E636F6D"
    # patent_text = hex_to_str(hex_string)
    patent_text = "Akash Kumar Singh"
    patent_label = tk.Label(app, text=f"{patent_text}", font=("Helvetica", 10), bg="#e0f7fa",
                            fg="#004d40")
    patent_label.pack(side=tk.BOTTOM, pady=5)


# Function to create buttons for sending messages
def create_buttons(parent_frame):
    button_frame = tk.Frame(parent_frame, bg="#ffffff")
    button_frame.pack(pady=20)

    generate_button = tk.Button(button_frame, text="Generate and Send Message", font=("Helvetica", 12), bg="#00796b",
                                fg="#ffffff", relief="raised",
                                command=lambda: send_message(option_var.get() == "Send Immediate"))
    generate_button.pack(pady=10)


# Initialize and run the application
if __name__ == "__main__":
    app = tk.Tk()
    create_ui()
    app.mainloop()
