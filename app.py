contacts = []

while True:
    print("\nContact Management\n")
    print("""
    1- Add a contact
    2- View contacts
    3- Edit a contact
    4- Exit
    """)

    service = int(input("Please choose a number from 1-4: "))

    if service == 1:
        contact_id = int(input("Enter the contact ID: "))
        name = input("Please type a name: ")
        phone = input("Please type a phone number: ")
        contacts.append({"ID": contact_id, "Name": name, "Phone": phone})
        print("Contact added successfully.")

    elif service == 2:
        if contacts:
            for contact in contacts:
                print(f"ID: {contact['ID']} | Name: {contact['Name']} | Phone: {contact['Phone']}")
        else:
            print("No contacts found.")

    elif service == 3:
        contact_id = int(input("Enter the contact ID to edit: "))
        found = False
        for contact in contacts:
            if contact["ID"] == contact_id:
                contact["Name"] = input("Please type a new name: ")
                contact["Phone"] = input("Please type a new phone number: ")
                print("Contact updated successfully.")
                found = True
                break
        if not found:
            print("Contact ID not found.")

    elif service == 4:
        break

print("\nYou have left the program.")
