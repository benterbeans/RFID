import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import tkinter as tk
from tkinter import simpledialog, messagebox

# Initialize the RFID reader
rfid = SimpleMFRC522()

# Create the main GUI window
root = tk.Tk()
root.title("RFID Card Management System")

# Function to verify identity based on occupation
def verify_identity(occupation):
    while True:
        verification_id = simpledialog.askstring(f"Enter {occupation} Verification ID", f" Medic, Police Officer, and Airport Security please make sure to scan RFID card/tag after verification ID is entered.\n Enter your {occupation} verification ID ({occupation[0]}XXXXXX{occupation[-1]}):")
        if (
            len(verification_id) == 8
            and verification_id[0] == occupation[0]
            and verification_id[1:7].isdigit()
            and verification_id[7] == occupation[-1]
        ):
            return verification_id
        else:
            # Show an error message and retry
            result = messagebox.showerror("Error", "Verification ID is incorrect. Please try again.", icon="error")
            if result == "ok":
                continue

# Function to create and add information to a text file using tkinter
def create_text_file_with_gui(file_name):
    # Create a new window for data entry
    data_entry_window = tk.Toplevel(root)
    data_entry_window.title("Enter Information")

    data = {}
    fields = [
        "First Name",
        "Last Name",
        "Passport Number",
        "Nationality",
        "Date of Birth",
        "Place of Birth",
        "Sex",
        "Passport Date of Issue",
        "Date of Passport Expiry",
        "Medical History",
        "Medical Conditions",
        "Treatments",
        "License Number",
        "Address",
        "Height",
        "Safe Driver Status",
        "Date of License Issue",
        "Date of License Expiration",
    ]

    # Create entry fields for each data field
    for field in fields:
        label = tk.Label(data_entry_window, text=field)
        label.pack()
        entry = tk.Entry(data_entry_window, width=40)
        entry.pack()
        data[field] = entry

    def save_data():
        with open(file_name + ".txt", "w") as file:
            for field, entry in data.items():
                file.write(field + ": " + entry.get() + "\n")

        messagebox.showinfo("File Created", f"Text file '{file_name}.txt' has been created.")
        data_entry_window.destroy()

    save_button = tk.Button(data_entry_window, text="Save", command=save_data)
    save_button.pack()
    
def read_text_file(id):
    file_name = str(id)
    with open(file_name + ".txt", "r") as file:
        content = file.read()
        return content
    
# Function for Admin operations
def on_admin():
    verification_id = verify_identity("D")
    if verification_id:
        create_file = simpledialog.askstring("Create File", "Do you want to create a text file? Please Scan RFID card/tag afterwards if 'Y' or 'Yes' (Y/N): ")
        if create_file and create_file.lower() == "y":
            # Create a new window for entering the file name and displaying the RFID numeric ID
            file_name_window = tk.Toplevel(root)
            file_name_window.title("Enter File Name")

            # Display the RFID numeric ID along with the instruction
            id = rfid.read()  # Read and print the RFID ID number
            numeric_id = str(id[0])
            tk.Label(file_name_window, text="RFID Numeric ID: " + numeric_id).pack()
            tk.Label(file_name_window, text="Please type this exact numeric ID into the input bar below to name the file the same as the RFID's internal numeric ID.").pack()

            # Create an entry field for entering the file name
            file_name_entry = tk.Entry(file_name_window, width=40)
            file_name_entry.pack()

            # Function to create the text file with the given name
            def create_file_with_name():
                file_name = file_name_entry.get()
                if file_name:
                    create_text_file_with_gui(file_name)
                    messagebox.showinfo("File Created", f"Text file '{file_name}.txt' has been created.")
                    erase_data = simpledialog.askstring("Erase Data", "Do you want to erase all information on the RFID? (Y/N): ")
                    if erase_data and erase_data.lower() == "y":
                        rfid.read()  # Scan the RFID to erase all contents
                else:
                    messagebox.showerror("Error", "File name cannot be empty.")

            create_button = tk.Button(file_name_window, text="Create File", command=create_file_with_name)
            create_button.pack()

# Function to display Medic-specific information in a window
def display_medic_info(id):
    # Extract the 12-digit numeric ID from the tuple
    numeric_id = str(id[0])
    content = read_text_file(numeric_id)
    if content:
        content = content.split('\n')
        first_name = content[0].split(": ")[1]
        last_name = content[1].split(": ")[1]
        date_of_birth = content[4].split(": ")[1]
        sex = content[6].split(": ")[1]
        medical_history = content[9].split(": ")[1]
        medical_conditions = content[10].split(": ")[1]
        treatments = content[11].split(": ")[1]
        
        # Create a new window for displaying Medic-specific information
        medic_window = tk.Toplevel(root)
        medic_window.title("Medic Information")
        
        # Create and set labels for the information
        tk.Label(medic_window, text="First Name: " + first_name).pack()
        tk.Label(medic_window, text="Last Name: " + last_name).pack()
        tk.Label(medic_window, text="Date of Birth: " + date_of_birth).pack()
        tk.Label(medic_window, text="Sex: " + sex).pack()
        tk.Label(medic_window, text="Medical History: " + medical_history).pack()
        tk.Label(medic_window, text="Medical Conditions: " + medical_conditions).pack()
        tk.Label(medic_window, text="Treatments: " + treatments).pack()
    else:
        print("Not enough information in the file.")

# Function to display Police Officer-specific information in a window
def display_police_officer_info(id):
    # Extract the 12-digit numeric ID from the tuple
    numeric_id = str(id[0])
    content = read_text_file(numeric_id)
    if content:
        content = content.split('\n')
        first_name = content[0].split(": ")[1]
        last_name = content[1].split(": ")[1]
        date_of_birth = content[4].split(": ")[1]
        sex = content[6].split(": ")[1]
        license_number = content[12].split(": ")[1]
        address = content[13].split(": ")[1]
        height = content[14].split(": ")[1]
        safe_driver_status = content[15].split(": ")[1]
        date_of_license_issue = content[16].split(": ")[1]
        date_of_license_expiration = content[17].split(": ")[1]
        
        # Create a new window for displaying Police Officer-specific information
        police_window = tk.Toplevel(root)
        police_window.title("Police Officer Information")
        
        # Create and set labels for the information
        tk.Label(police_window, text="First Name: " + first_name).pack()
        tk.Label(police_window, text="Last Name: " + last_name).pack()
        tk.Label(police_window, text="Date of Birth: " + date_of_birth).pack()
        tk.Label(police_window, text="Sex: " + sex).pack()
        tk.Label(police_window, text="License Number: " + license_number).pack()
        tk.Label(police_window, text="Address: " + address).pack()
        tk.Label(police_window, text="Height: " + height).pack()
        tk.Label(police_window, text="Safe Driver Status: " + safe_driver_status).pack()
        tk.Label(police_window, text="Date of License Issue: " + date_of_license_issue).pack()
        tk.Label(police_window, text="Date of License Expiration: " + date_of_license_expiration).pack()
    else:
        print("Not enough information in the file.")

# Function to display Airport Security-specific information in a window
def display_airport_security_info(id):
    # Extract the 12-digit numeric ID from the tuple
    numeric_id = str(id[0])
    content = read_text_file(numeric_id)
    if content:
        content = content.split('\n')
        first_name = content[0].split(": ")[1]
        last_name = content[1].split(": ")[1]
        passport_number = content[2].split(": ")[1]
        nationality = content[3].split(": ")[1]
        date_of_birth = content[4].split(": ")[1]
        place_of_birth = content[5].split(": ")[1]
        sex = content[6].split(": ")[1]
        passport_date_of_issue = content[7].split(": ")[1]
        date_of_passport_expiry = content[8].split(": ")[1]
        
        # Create a new window for displaying Airport Security-specific information
        security_window = tk.Toplevel(root)
        security_window.title("Airport Security Information")
        
        # Create and set labels for the information
        tk.Label(security_window, text="First Name: " + first_name).pack()
        tk.Label(security_window, text="Last Name: " + last_name).pack()
        tk.Label(security_window, text="Passport Number: " + passport_number).pack()
        tk.Label(security_window, text="Nationality: " + nationality).pack()
        tk.Label(security_window, text="Date of Birth: " + date_of_birth).pack()
        tk.Label(security_window, text="Place of Birth: " + place_of_birth).pack()
        tk.Label(security_window, text="Sex: " + sex).pack()
        tk.Label(security_window, text="Passport Date of Issue: " + passport_date_of_issue).pack()
        tk.Label(security_window, text="Date of Passport Expiry: " + date_of_passport_expiry).pack()
    else:
        print("Not enough information in the file.")

# Function to read RFID and execute an occupation-specific function
def read_rfid_and_execute_occupation(occupation, occupation_function):
    verification_id = verify_identity(occupation)
    if verification_id:
        id = rfid.read()  # Read RFID ID
        print(f"RFID ID: {id}")
        occupation_function(id)
        
# Create buttons for different occupations
admin_button = tk.Button(root, text="Admin", command=on_admin)
medic_button = tk.Button(root, text="Medic", command=lambda: read_rfid_and_execute_occupation("Medic", display_medic_info))
police_button = tk.Button(root, text="Police Officer", command=lambda: read_rfid_and_execute_occupation("Police Officer", display_police_officer_info))
security_button = tk.Button(root, text="Airport Security", command=lambda: read_rfid_and_execute_occupation("Airport Security", display_airport_security_info))

admin_button.pack()
medic_button.pack()
police_button.pack()
security_button.pack()

root.mainloop()