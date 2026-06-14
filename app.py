import streamlit as st
import pandas as pd

# 1. Initialize Session State to keep the contacts data alive across reruns
if "contacts" not in st.session_state:
    st.session_state.contacts = []

# Application Title and Header
st.title("📞 Contact Management System")
st.write("Welcome to your interactive contact manager application!")

# 2. Sidebar navigation replacing the traditional console while loop
menu = ["Add a Contact", "View Contacts", "Edit a Contact"]
choice = st.sidebar.selectbox("Please choose a service:", menu)

# --- OPTION 1: ADD A CONTACT ---
if choice == "Add a Contact":
    st.subheader("➕ Add a New Contact")
    
    # Using st.form so inputs are submitted all at once when the button is clicked
    with st.form("add_form", clear_on_submit=True):
        contact_id = st.number_input("Enter the contact ID:", min_value=1, step=1)
        name = st.text_input("Please type a name:")
        phone = st.text_input("Please type a phone number:")
        submit_button = st.form_submit_button("Add Contact")
        
        if submit_button:
            # Check if the ID already exists to maintain data integrity
            id_exists = any(c["ID"] == contact_id for c in st.session_state.contacts)
            
            if id_exists:
                st.error("This ID already exists! Please use a unique ID.")
            elif name.strip() and phone.strip():
                # Save data into session_state if fields are not empty
                st.session_state.contacts.append({
                    "ID": int(contact_id), 
                    "Name": name.strip(), 
                    "Phone": phone.strip()
                })
                st.success(f"Contact '{name.strip()}' added successfully! 🎉")
            else:
                st.warning("Please fill out all fields.")

# --- OPTION 2: VIEW CONTACTS ---
elif choice == "View Contacts":
    st.subheader("📋 View Contacts List")
    
    if st.session_state.contacts:
        # Displaying the data using an interactive Pandas Dataframe
        df = pd.DataFrame(st.session_state.contacts)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No contacts found yet. Go to 'Add a Contact' to add some!")

# --- OPTION 3: EDIT A CONTACT ---
elif choice == "Edit a Contact":
    st.subheader("📝 Edit an Existing Contact")
    
    if not st.session_state.contacts:
        st.info("No contacts available to edit.")
    else:
        # FIX 1: Extract IDs as stable options for the dropdown
        contact_ids = [c["ID"] for c in st.session_state.contacts]
        
        # Helper function to dynamically display the name alongside the ID
        def get_contact_label(id_val):
            c = next((item for item in st.session_state.contacts if item["ID"] == id_val), None)
            return f"{c['Name']} (ID: {c['ID']})" if c else f"ID: {id_val}"
        
        selected_id = st.selectbox(
            "Select the contact to edit:",
            options=contact_ids,
            format_func=get_contact_label
        )
        
        # Find the actual contact dictionary matching the selected ID
        contact = next(c for c in st.session_state.contacts if c["ID"] == selected_id)
        
        # FIX 2: Added a unique `key` bound to the selected_id so text inputs refresh properly
        with st.form("edit_contact_form"):
            new_name = st.text_input("Edit Name:", value=contact["Name"], key=f"name_{selected_id}")
            new_phone = st.text_input("Edit Phone Number:", value=contact["Phone"], key=f"phone_{selected_id}")
            update_btn = st.form_submit_button("Update Contact")
            
            # Input validation before saving the updated record
            if update_btn:
                if new_name.strip() and new_phone.strip():
                    contact["Name"] = new_name.strip()
                    contact["Phone"] = new_phone.strip()
                    st.success("Contact updated successfully! ✨")
                    st.rerun()  # Forces Streamlit to instantly refresh and show new data
                else:
                    st.error("Fields cannot be empty.")
