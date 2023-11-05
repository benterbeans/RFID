import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

def get_user_occupation():
    while True:
        occupation = input("Enter your occupation (Airport Security, Police Officer, Medic, Admin): ")
        if occupation in ["Airport Security", "Police Officer", "Medic", "Admin"]:
            return occupation
        else:
            print("Invalid occupation. Please choose from the options provided.")

def validate_verification_id(occupation):
    while True:
        verification_id = input(f"Enter your {occupation} verification ID: ")
        if (
            (occupation == "Airport Security" and verification_id.startswith("A") and
             verification_id[1:-1].isdigit() and verification_id[-1] == "S")
            or
            (occupation == "Police Officer" and verification_id.startswith("P") and
             verification_id[1:-1].isdigit() and verification_id[-1] == "O")
            or
            (occupation == "Medic" and verification_id.startswith("M") and
             verification_id[1:-1].isdigit() and verification_id[-1] == "D")
            or
            (occupation == "Admin" and verification_id.startswith("A") and
             verification_id[1:-1].isdigit() and verification_id[-1] == "N")
        ):
            return verification_id
        else:
            print("Invalid verification ID. Please follow the format for your occupation.")

def input_admin_info():
    info = {}
    info["First Name"] = input("Please input First Name: ")
    info["Last Name"] = input("Please input Last Name: ")
    info["ID Number"] = input("Please input ID Number: ")
    info["Address"] = input("Please input Address: ")
    info["Date of Birth"] = input("Please input Date of Birth: ")
    info["ID Expiry Date"] = input("Please input ID Expiry Date: ")
    info["Sex"] = input("Please input Sex: ")
    info["Height"] = input("Please input Height: ")
    info["Safe Driver Status"] = input("Please input Safe Driver Status: ")
    info["Blood Type"] = input("Please input Blood Type: ")
    info["Diseases"] = input("Please input Diseases: ")
    info["Allergies"] = input("Please input Allergies: ")
    return info

def write_info_to_rfid(rfid, info):
    info_str = ', '.join(f"{key}: {value}" for key, value in info.items())
    rfid.write(info_str)
    print("Information written to RFID card.")

def display_info(occupation, rfid, verification_id):
    id, text = rfid.read()
    if not text:
        print("No information found on RFID card.")
        return

    data = text.split(', ')
    
    print(f"Occupation: {occupation}")
    print(f"Verification ID: {verification_id}")
    
    for item in data:
        field_name, field_value = item.split(": ")
        print(f"{field_name}: {field_value}")

rfid = SimpleMFRC522()

while True:
    user_occupation = get_user_occupation()
    verification_id = validate_verification_id(user_occupation)
    
    if user_occupation == "Admin":
        admin_info = input_admin_info()
        write_info_to_rfid(rfid, admin_info)
    else:
        display_info(user_occupation, rfid, verification_id)
