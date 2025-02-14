import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import random
from fpdf import FPDF
import os
from twilio.rest import Client
from datetime import date

def send_sms_notification(receiver_contact, tracking_id):
    # Twilio credentials
    account_sid = "AC0f0de57af4b48f9d174985"  #
    auth_token = "292fbff3faae63e9161e899b8f"
    client = Client(account_sid, auth_token)

    # SMS content
    message = client.messages.create(
        body=f"Your package with tracking ID {tracking_id} is now in transit.Soon the delivery boy will call you ",
        from_="+15057058083", 
        to='+9779869939258'  
    )
    print(message.sid)
    print(f"Notification sent to {receiver_contact}")



if not firebase_admin._apps:
    cred = credentials.Certificate("courierapp-56369-firebase-adminsdk-fbsvc-911b5d.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://courierapp-59-default-rtdb.firebaseio.com/"
    })


ref = db.reference('courier')
ref_for_registration= db.reference('Registered')

# Function to generate PDF
def generate_pdf(data, unique_id):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, txt="Courier Service Details", ln=True, align='C')
    pdf.ln(10)

    # Content
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=f"Tracking ID: {unique_id}", ln=True)
    pdf.ln(5)

    pdf.cell(0, 10, txt="Sender Information:", ln=True)
    pdf.cell(0, 10, txt=f"Name: {data['sender_name']}", ln=True)
    pdf.cell(0, 10, txt=f"Contact Number: {data['sender_contact']}", ln=True)
    pdf.cell(0, 10, txt=f"Email: {data['sender_email']}", ln=True)
    pdf.cell(0, 10, txt=f"Address: {data['sender_address']}", ln=True)
    pdf.ln(5)

    pdf.cell(0, 10, txt="Receiver Information:", ln=True)
    pdf.cell(0, 10, txt=f"Name: {data['receiver_name']}", ln=True)
    pdf.cell(0, 10, txt=f"Contact Number: {data['receiver_contact']}", ln=True)
    pdf.cell(0, 10, txt=f"Email: {data['receiver_email']}", ln=True)
    pdf.cell(0, 10, txt=f"Address: {data['receiver_address']}", ln=True)
    pdf.cell(0, 10, txt=f"District: {data['receiver_district']}", ln=True)
    pdf.ln(5)

    pdf.cell(0, 10, txt="Package Details:", ln=True)
    pdf.cell(0, 10, txt=f"Description: {data['package_description']}", ln=True)
    pdf.cell(0, 10, txt=f"Preferred Delivery Date: {data['delivery_date']}", ln=True)

    # Save PDF 
    pdf_file = f"{unique_id}_courier_details.pdf"
    pdf.output(pdf_file)
    return pdf_file

st.image("Ai delivers.png", width=630)

# Streamlit Interface
st.title("Courier Service Registration and Tracking")


tab1, tab2, tab3, tab4 , tab5, tab6 = st.tabs(["Register Courier", "Track Courier","Admin Login","Delivery Boy Register","Delivery","Tutorial"])

# Tab 1: Register Courier
with tab1:
    st.header("Register a New Courier")
    st.subheader("Sender Information")
    sender_name = st.text_input("Sender Name", key="sender_name_input")
    sender_contact = st.text_input("Sender Contact Number", key="sender_contact_input")
    sender_email = st.text_input("Sender Email Address", key="sender_email_input")
    sender_address = st.text_input("Sender precise address (e.g., Kalanki, opposite Baba Petrol Pump)", key="sender_address_input")

    st.subheader("Receiver Information")
    receiver_name = st.text_input("Receiver Name", key="receiver_name_input")
    receiver_contact = st.text_input("Receiver Contact Number", key="receiver_contact_input")
    receiver_email = st.text_input("Receiver Email Address", key="receiver_email_input")
    receiver_address = st.text_input("Receiver precise address (e.g., Street No. 17, near Avia Club, Lakeside, Pokhara)", key="receiver_address_input")
    receiver_district = st.selectbox("District of Receiver", ["Rupandehi", "Kaski", "Chitwan", "Lalitpur", "Bhaktapur", "Kathmandu", "Dharan", "Makwanpur", "Dhading", "Syangja", "Dang", "Gorkha", "Mahendranagar", "Bardiya", "Kapilvastu", "Jhapa", "Morang", "Sunsari"])

    st.subheader("Package Details")
    package_description = st.text_area("Package Description (e.g., documents, electronics, etc.)", key="package_description_input")
    delivery_type = st.radio("Select Delivery Type", ["Schedule Delivery", "Fast Delivery"])
    
    if delivery_type == "Schedule Delivery":
        delivery_date = st.date_input("Preferred Delivery Date", key="delivery_date_input")
    else:
        delivery_date = "Fast Delivery"
    
    
    
    
    

    if st.button("Submit", key="submit_button"):
        if sender_name and sender_contact and sender_email and sender_address and receiver_name and receiver_contact and receiver_email and receiver_address and receiver_district and package_description and delivery_date:
            # Generate a random unique number
            random_number = random.randint(10000, 99999)

            # Check if the random number already exists (avoid collisions)
            while ref.child(str(random_number)).get() is not None:
                random_number = random.randint(10000, 99999)

            # Data to be submitted
            data = {
                "sender_name": sender_name,
                "sender_contact": sender_contact,
                "sender_email": sender_email,
                "sender_address": sender_address,
                "receiver_name": receiver_name,
                "receiver_contact": receiver_contact,
                "receiver_email": receiver_email,
                "receiver_address": receiver_address,
                "receiver_district": receiver_district,
                "package_description": package_description,
                "delivery_date": str(delivery_date) if isinstance(delivery_date, date) else delivery_date,
                "status": "Pending" 
            }
            # Add data to Firebase
            ref.child(str(random_number)).set(data)

            # Generate PDF
            pdf_file = generate_pdf(data, random_number)

            # Display PDF download link
            with open(pdf_file, "rb") as file:
                st.download_button(
                    label="Download PDF",
                    data=file,
                    file_name=pdf_file,
                    mime="application/pdf"
                )

            # Clean up temporary file
            os.remove(pdf_file)

            st.success(f"Courier registered successfully! Tracking ID: {random_number}")
        else:
            st.error("Please fill in all fields.")

# Tab 2: Track Courier
with tab2:
    st.header("Track Courier")
    tracking_id = st.text_input("Enter Tracking ID", key="tracking_id_input")

    if st.button("Search", key="search_button"):
        if tracking_id:
            courier_data = ref.child(tracking_id).get()
            if courier_data:
                st.write("Courier Details:")
                st.json(courier_data)
            else:
                st.error("No data found for this Tracking ID.")
        else:
            st.error("Please enter a valid Tracking ID.")


# Tab 3: Admin Login
with tab3:
    # Step 1: Admin Login
    with st.expander("Admin Login", expanded=True):
        st.header("Admin Login")
        
        # Add some custom CSS for the login form
        st.markdown("""
            <style>
            .stTextInput > label {
                font-size: 16px;
                font-weight: bold;
                color: #0066cc;
            }
            </style>
            """, unsafe_allow_html=True)

        # Login fields with icons
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("👤")
        with col2:
            admin_email = st.text_input("Admin Email", key="admin_email_input")
            
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("🔒")
        with col2:
            admin_password = st.text_input("Admin Password", type="password", key="admin_password_input")

        # Center the login button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Login", key="admin_login_button", use_container_width=True):
                # Hardcoded admin credentials
                hardcoded_email = "bidhan@gmail.com"
                hardcoded_password = "Bidhan99@"

                if admin_email == hardcoded_email and admin_password == hardcoded_password:
                    st.success("✅ Admin logged in successfully!")
                    st.session_state.logged_in = True
                else:
                    st.error("❌ Invalid email or password. Please try again.")

    # Step 2: Show Date Picker After Login
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        st.markdown("---")
        st.subheader("📊 Dashboard - Filter Transactions by Date")

        # Create two columns for date picker and view button
        col1, col2 = st.columns([2, 1])
        
        with col1:
            selected_date = st.date_input(
                "Select Date to View Transactions", 
                key="filter_date_input", 
                value=None,
                help="Choose a date to view all deliveries scheduled for that day"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)  # Add some spacing
            view_clicked = st.button("🔍 View Transactions", use_container_width=True)

        if view_clicked:
            with st.spinner('Fetching delivery data...'):
                # Fetch all courier IDs
                all_couriers = ref.get()
                
                if all_couriers:
                    filtered_deliveries = []
                    
                    # Iterate through each courier ID
                    for courier_id, courier_data in all_couriers.items():
                        # Check if the delivery date matches
                        if courier_data.get("delivery_date") == str(selected_date):
                            filtered_deliveries.append({
                                "courier_id": courier_id,
                                "package_description": courier_data.get("package_description", "N/A"),
                                "receiver_address": courier_data.get("receiver_address", "N/A"),
                                "delivery_date": courier_data.get("delivery_date", "N/A")
                            })
                    
                    if filtered_deliveries:
                        # Display summary metrics
                        st.markdown("### 📈 Summary")
                        metric1, metric2 = st.columns(2)
                        with metric1:
                            st.metric("Total Deliveries", len(filtered_deliveries))
                        with metric2:
                            # Convert date to string before displaying in metric
                            st.metric("Delivery Date", str(selected_date))
                        
                        st.markdown("### 📦 Delivery Details")
                        
                        # Display each delivery in a card format
                        for delivery in filtered_deliveries:
                            with st.container():
                                col1, col2 = st.columns([1, 2])
                                
                                # Left column for Courier ID and Date
                                with col1:
                                    st.markdown(
                                        f"""
                                        <div style='background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin: 5px;'>
                                            <h4 style='color: #0066cc; margin: 0;'>Courier ID: {delivery['courier_id']}</h4>
                                            <p style='color: #666666; margin: 5px 0;'>📅 {delivery['delivery_date']}</p>
                                        </div>
                                        """,
                                        unsafe_allow_html=True
                                    )
                                
                                # Right column for Package and Address details
                                with col2:
                                    st.markdown(
                                        f"""
                                        <div style='background-color:black; padding: 10px; border-radius: 5px; margin: 5px; border: 1px solid #e1e4e8;'>
                                            <p style='margin: 5px 0;'><strong>📦 Package:</strong> {delivery['package_description']}</p>
                                            <p style='margin: 5px 0;'><strong>📍 Address:</strong> {delivery['receiver_address']}</p>
                                        </div>
                                        """,
                                        unsafe_allow_html=True
                                    )
                                
                                # Add a divider between entries
                                st.markdown("<hr style='margin: 10px 0; border: none; border-top: 1px solid #e1e4e8;'>", unsafe_allow_html=True)
                        
                        # Export options
                        st.markdown("### 📥 Export Options")
                        
                        # Add export to CSV option
                        import pandas as pd
                        df = pd.DataFrame(filtered_deliveries)
                        csv = df.to_csv(index=False).encode('utf-8')
                        
                        st.download_button(
                            "Download Data as CSV",
                            csv,
                            "delivery_data.csv",
                            "text/csv",
                            key='download-csv',
                            help="Download the filtered delivery data as a CSV file"
                        )
                        
                    else:
                        st.warning("📭 No deliveries found for the selected date.")
                else:
                    st.warning("📭 No data available in the database.")
                    
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        st.markdown("---")
        st.subheader("📦 Update Package Status")

        # Input for tracking ID and status
        tracking_id_to_update = st.text_input("Enter Tracking ID to Update Status", key="tracking_id_update")
        status = st.selectbox("Select Status", ["Pending", "In Transit", "Delivered"], key="status_select")

        if st.button("Update Status", key="update_status_button"):
            if tracking_id_to_update:
                # Fetch current courier data
                courier_data = ref.child(tracking_id_to_update).get()
                if courier_data:
                    # Update the status
                    ref.child(tracking_id_to_update).update({"status": status})
                    st.success(f"Package status updated to {status}!")
                    if status == "In Transit":
                     receiver_contact = courier_data.get("receiver_contact")  # Get receiver's phone number
                     send_sms_notification(receiver_contact, tracking_id_to_update)
                    
                    
                    
                else:
                    st.error("❌ No data found for this Tracking ID.")
            else:
                st.error("Please enter a valid Tracking ID.")

        # Optionally, display updated status here
        st.markdown("### Updated Status")
        if tracking_id_to_update:
            updated_data = ref.child(tracking_id_to_update).get()
            if updated_data:
                st.write(f"Tracking ID: {tracking_id_to_update}")
                st.write(f"Status: {updated_data.get('status', 'Not Available')}")
                

    if 'logged_in' in st.session_state and st.session_state.logged_in:
        st.markdown("---")
        st.subheader("🚚 Assign Delivery Tasks")

        # Fetch all tracking IDs with their receiver district
        all_couriers = ref.get()
        if all_couriers:
            tracking_options = [
                f"{courier_id} - {courier_data.get('receiver_district', 'Unknown District')}"
                for courier_id, courier_data in all_couriers.items()
            ]
        else:
            tracking_options = []

        # Dropdown for tracking ID selection
        selected_tracking_option = st.selectbox(
            "Select Tracking ID (with Receiver District)",
            tracking_options,
            key="select_tracking_id"
        )

        # Extract the actual tracking ID from the selected option
        selected_tracking_id = selected_tracking_option.split(" - ")[0] if selected_tracking_option else None

        # Fetch all delivery boys with their address
        delivery_boys_data = ref_for_registration.get()
        if delivery_boys_data:
            delivery_boy_options = [
                f"{value['delivery_boy_name']} - {value.get('delivery_boy_address', 'Unknown Address')}"
                for key, value in delivery_boys_data.items()
            ]
        else:
            delivery_boy_options = []

        # Dropdown for delivery boy selection
        selected_delivery_boy_option = st.selectbox(
            "Select Delivery Boy (with Address)",
            delivery_boy_options,
            key="select_delivery_boy"
        )

        # Extract the delivery boy name from the selected option
        selected_delivery_boy = (
            selected_delivery_boy_option.split(" - ")[0] if selected_delivery_boy_option else None
        )

        # Assign button
        if st.button("Assign", key="assign_button"):
            if selected_tracking_id and selected_delivery_boy:
                # Find the delivery boy's unique key
                delivery_boy_key = None
                for key, value in delivery_boys_data.items():
                    if value["delivery_boy_name"] == selected_delivery_boy:
                        delivery_boy_key = key
                        break

                if delivery_boy_key:
                    # Update the tracking ID with the delivery boy's information
                    ref.child(selected_tracking_id).update({"assigned_to": delivery_boy_key})
                    st.success(
                        f"Tracking ID {selected_tracking_id} has been assigned to {selected_delivery_boy}!"
                    )
                else:
                    st.error("Unable to find the selected delivery boy in the database.")
            else:
                st.error("Please select both a Tracking ID and a Delivery Boy.")


## register for delivery person
with tab4:
    st.header("Register a Delivery Boy")
    st.subheader("Your Information")
    
    delivery_boy_name = st.text_input("Your Name", key="delivery_boy_name_input")
    delivery_boy_contact = st.text_input("Your Contact Number", key="delivery_boy_contact_input")
    delivery_boy_email = st.text_input("Email", key="delivery_boy_email_input")
    delivery_boy_address = st.text_input("Address", key="delivery_boy_address_input")
    delivery_vehicle_number = st.text_input("Vehicle Number", key="delivery_vehicle_number_input")
    delivery_vehicle_type = st.selectbox("Vehicle Type", ["MotorBike", "Scooter", "Car", "Cycle"], key="delivery_vehicle_type_input")
    
    # Password fields
    password = st.text_input("Password", type="password", key="delivery_boy_password_input")
    confirm_password = st.text_input("Confirm Password", type="password", key="delivery_boy_confirm_password_input")

    if st.button("Submit", key="delivery_submit_button"):
        if delivery_boy_name and delivery_boy_contact and delivery_boy_email and delivery_boy_address and delivery_vehicle_number and delivery_vehicle_type and password and confirm_password:
            if password != confirm_password:
                st.error("Passwords do not match. Please try again.")
            else:
                # Generate a random unique number for registration
                random_number = random.randint(10000, 99999)

                # Ensure the random number is unique
                while ref_for_registration.child(str(random_number)).get() is not None:
                    random_number = random.randint(10000, 99999)

                # Data to be submitted
                data = {
                    "delivery_boy_name": delivery_boy_name,
                    "delivery_boy_contact": delivery_boy_contact,
                    "delivery_boy_email": delivery_boy_email,
                    "delivery_boy_address": delivery_boy_address,
                    "delivery_vehicle_number": delivery_vehicle_number,
                    "delivery_vehicle_type": delivery_vehicle_type,
                    "password": password  # Store the password entered by the user
                }
                
                # Add data to Firebase
                ref_for_registration.child(str(random_number)).set(data)

                st.success("You are registered successfully")
        else:
            st.error("Please fill in all fields.")

# Tab 5: Delivery Boy Login
with tab5:

    st.header("Login")
    st.subheader("Enter Your Credentials")

    login_email = st.text_input("Email", key="login_email_input")
    login_password = st.text_input("Password", type="password", key="login_password_input")

    if st.button("Login", key="login_button"):
        # Validate email and password
        if login_email and login_password:
            delivery_boys_data = ref_for_registration.get()

            # Authenticate
            found = False
            for key, value in delivery_boys_data.items():
                if value["delivery_boy_email"] == login_email and value["password"] == login_password:
                    found = True
                    delivery_boy_key = key
                    st.success(f"Welcome, {value['delivery_boy_name']}!")

                    # Fetch all assigned tasks
                    all_couriers = ref.get()
                    assigned_tasks = [
                        {
                            "tracking_id": courier_id,
                            "package_description": courier_data.get("package_description", "N/A"),
                            "receiver_address": courier_data.get("receiver_address", "N/A"),
                            "delivery_date": courier_data.get("delivery_date", "N/A"),
                            "status": courier_data.get("status", "Pending")
                        }
                        for courier_id, courier_data in all_couriers.items()
                        if courier_data.get("assigned_to") == delivery_boy_key
                    ]

                    if assigned_tasks:
                        st.subheader("📋 Your Assigned Tasks")
                        for task in assigned_tasks:
                            st.markdown(f"""
                            **Tracking ID:** {task['tracking_id']}  
                            **Package:** {task['package_description']}  
                            **Address:** {task['receiver_address']}  
                            **Delivery Date:** {task['delivery_date']}  
                            
                
                            """)
                            st.markdown("---")
                    else:
                        st.info("No tasks assigned yet.")
                    break

            if not found:
                st.error("Invalid credentials. Please try again.")
        else:
            st.error("Please fill in both email and password.")

with tab6:
    st.header("How to Use the App")
    st.subheader("Watch the video below to learn how to use this app:")