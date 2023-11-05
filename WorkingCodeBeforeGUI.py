import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import os

rfid = SimpleMFRC522()

# Function to verify identity based on occupation
def verify_identity(occupation):
    while True:
        verification_id = input(f"Enter your {occupation} verification ID ({occupation[0]}123456{occupation[-1]}): ")
        if (
            len(verification_id) == 8
            and verification_id[0] == occupation[0]
            and verification_id[1:7].isdigit()
            and verification_id[7] == occupation[-1]
        ):
            return verification_id
        else:
            print("Invalid verification number. Please try again.")

# Function to create and add information to a text file
def create_text_file(file_name):
    with open(file_name + ".txt", "w") as file:
        file.write("First Name: " + input("Enter First Name: ") + "\n")
        file.write("Last Name: " + input("Enter Last Name: ") + "\n")
        file.write("Passport Number: " + input("Enter Passport Number: ") + "\n")
        file.write("Nationality: " + input("Enter Nationality: ") + "\n")
        file.write("Date of Birth: " + input("Enter Date of Birth: ") + "\n")
        file.write("Place of Birth: " + input("Enter Place of Birth: ") + "\n")
        file.write("Sex: " + input("Enter Sex: ") + "\n")
        file.write("Passport Date of Issue: " + input("Enter Passport Date of Issue: ") + "\n")
        file.write("Date of Passport Expiry: " + input("Enter Date of Passport Expiry: ") + "\n")
        file.write("Medical History: " + input("Enter Medical History: ") + "\n")
        file.write("Medical Conditions: " + input("Enter Medical Conditions: ") + "\n")
        file.write("Treatments: " + input("Enter Treatments: ") + "\n")
        file.write("License Number: " + input("Enter License Number: ") + "\n")
        file.write("Address: " + input("Enter Address: ") + "\n")
        file.write("Height: " + input("Enter Height: ") + "\n")
        file.write("Safe Driver Status: " + input("Enter Safe Driver Status: ") + "\n")
        file.write("Date of License Issue: " + input("Enter Date of License Issue: ") + "\n")
        file.write("Date of License Expiration: " + input("Enter Date of License Expiration: ") + "\n")

# Function to read and display information from the text file
def read_text_file(id):
    file_name = str(id)
    with open(file_name + ".txt", "r") as file:
        content = file.readlines()
        print("".join(content))

# Function to display Medic-specific information
def display_medic_info(id):
    try:
        with open(str(id) + ".txt", "r") as file:
            content = file.readlines()
            if len(content) >= 13:
                print("First Name: " + content[0].strip())
                print("Last Name: " + content[1].strip())
                print("Date of Birth: " + content[2].strip())
                print("Sex: " + content[3].strip())
                print("Medical History: " + content[10].strip())
                print("Medical Conditions: " + content[11].strip())
                print("Treatments: " + content[12].strip())
            else:
                print("Not enough information in the file.")
    except FileNotFoundError:
        print("File not found. Try again.")

# Function to display Police Officer-specific information
def display_police_officer_info(id):
    try:
        with open(str(id) + ".txt", "r") as file:
            content = file.readlines()
            if len(content) >= 18:
                print("First Name: " + content[0].strip())
                print("Last Name: " + content[1].strip())
                print("Date of Birth: " + content[4].strip())
                print("Sex: " + content[6].strip())
                print("License Number " + content[12].strip())
                print("Address " + content[13].strip())
                print("Height: " + content[14].strip())
                print("Safe Driver Status: " + content[15].strip())
                print("Date of License Issue: " + content[16].strip())
                print("Date of License Expiration: " + content[17].strip())
            else:
                print("Not enough information in the file.")
    except FileNotFoundError:
        print("File not found. Try again.")

# Function to display Airport Security-specific information
def display_airport_security_info(id):
    try:
        with open(str(id) + ".txt", "r") as file:
            content = file.readlines()
            if len(content) >= 14:
                print("First Name: " + content[0].strip())
                print("Last Name: " + content[1].strip())
                print("Passport Number: " + content[7].strip())
                print("Nationality: " + content[8].strip())
                print("Date of Birth: " + content[9].strip())
                print("Place of Birth: " + content[10].strip())
                print("Sex: " + content[11].strip())
                print("Passport Date of Issue: " + content[12].strip())
                print("Date of Passport Expiry: " + content[13].strip())
            else:
                print("Not enough information in the file.")
    except FileNotFoundError:
        print("File not found. Try again.")

while True:
    occupation = input("Enter your occupation (Admin, Medic, Police Officer, Airport Security): ")
    
    if occupation == "Admin":
        verification_id = verify_identity("D")
        view_rfid = input("Do you want to view the RFID ID number before creating a new file? (Y/N): ")
        if view_rfid == "Y":
            id = rfid.read()  # Read and print the RFID ID number
            print("RFID ID:", id)
        create_file = input("Do you want to create a text file? (Y/N): ")
        if create_file == "Y":
            file_name = input("Enter the file name (without extension) needs to be the same as the RFID id number: ")
            create_text_file(file_name)
            erase_data = input("Do you want to erase all information on the RFID? (Y/N): ")
            if erase_data == "Y":
                rfid.read()  # Scan the RFID to erase all contents
        continue  # Go back to the beginning

    elif occupation == "Medic":
        verification_id = verify_identity("M")
        display_medic_info(rfid.read_id())
        continue

    elif occupation == "Police Officer":
        verification_id = verify_identity("P")
        display_police_officer_info(rfid.read_id())
        continue

    elif occupation == "Airport Security":
        verification_id = verify_identity("A")
        display_airport_security_info(rfid.read_id())
        continue
