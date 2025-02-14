![image](https://github.com/user-attachments/assets/42f98574-930a-46d5-842f-44362fffcb22)
Courier Service Web App with Streamlit and Firebase



This is a courier service web application built using Streamlit and Firebase. It allows users to register couriers, track packages, and manage deliveries.

Features

Courier Registration:

Capture sender and receiver information (name, contact, email, address).

Record package details (description, delivery type, preferred date).

Generate a unique tracking ID.

Store data securely in Firebase Realtime Database.

Generate and download a PDF summary of the courier details.

Courier Tracking:

Users can track their packages using the generated tracking ID.

Retrieve and display real-time courier status from Firebase.

Admin Panel:

Secure admin login with email and password.

View and filter deliveries by date.

Update package status (Pending, In Transit, Delivered).

Assign delivery tasks to registered delivery personnel.

Dashboard with summary metrics of deliveries.

Export delivery data as CSV.

Delivery Personnel Registration:

Delivery personnel can register with their information (name, contact, address, vehicle details).

Secure password storage.

Delivery Personnel Login:

Delivery personnel can log in to view their assigned tasks.

Display assigned deliveries with relevant details.

Technologies Used

Streamlit - For building the interactive web application.

Firebase - For real-time database and authentication.

FPDF - For generating PDF summaries.

Twilio - For sending SMS notifications.

Setup and Installation

1. Clone the repository:

git clone https://github.com/your-username/courier-service-app.git
cd courier-service-app

2. Install dependencies:

pip install streamlit firebase-admin fpdf twilio

3. Firebase Setup:

Create a Firebase project and a Realtime Database.

Download the google-services.json file and place it in your project directory.

Update firebase_admin.initialize_app() with your Firebase project details.

4. Twilio Setup:

Create a Twilio account and obtain your Account SID and Auth Token.

Replace the placeholders in the send_sms_notification() function with your Twilio credentials.

5. Run the app:

streamlit run app.py

