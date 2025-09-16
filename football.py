import streamlit as st
import mysql.connector
from mysql.connector import Error
import hashlib
import pandas as pd

# Initialize session state variables if they don't exist
# if 'logged_in' not in st.session_state:
#     st.session_state['logged_in'] = False
# if 'current_user' not in st.session_state:
#     st.session_state['current_user'] = None

# Load the DataFrame globally
df = pd.read_csv("fifaratings.csv")

# # Function to connect to MySQL database
# def connect_to_database():
#     try:
#         connection = mysql.connector.connect(
#             host='localhost',
#             database='manazer_db',
#             user='root',  # Update with your MySQL username
#             password=''  # Update with your MySQL password
#         )
#         if connection.is_connected():
#             return connection
#     except Error as e:
#         st.error(f"Error while connecting to MySQL: {e}")
#         return None

# # Function to hash a password
# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()

# # Function to register a new user
# def register_user(email, password, full_name, weight, height, age, exercise_time, bed_time, working_time, football_time):
#     try:
#         connection = connect_to_database()
#         if connection:
#             cursor = connection.cursor()
#             hashed_password = hash_password(password)  # Hash the password
#             query = """
#             INSERT INTO users (email, password, full_name, weight, height, age, exercise_time, bed_time, working_time, football_time)
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#             """
#             data = (email, hashed_password, full_name, weight, height, age, exercise_time, bed_time, working_time, football_time)
#             cursor.execute(query, data)
#             connection.commit()
#             st.info(f"Registered user: {email}")  # Debug message
#             return True
#         else:
#             st.error("Failed to connect to the database.")
#     except Error as e:
#         st.error(f"Error while registering user: {e}")
#         return False
#     finally:
#         if connection:
#             cursor.close()
#             connection.close()

# # Function to authenticate user login
# def authenticate_user(email, password):
#     try:
#         connection = connect_to_database()
#         if connection:
#             cursor = connection.cursor()
#             query = "SELECT * FROM users WHERE email = %s"
#             data = (email,)
#             cursor.execute(query, data)
#             user = cursor.fetchone()
#             if user:
#                 # Check if password matches
#                 hashed_password = hash_password(password)
#                 if user[2] == hashed_password:  # Assuming password is stored as hashed in the database
#                     return user
#             return None
#     except Error as e:
#         st.error(f"Error while authenticating user: {e}")
#         return None
#     finally:
#         if connection:
#             cursor.close()
#             connection.close()

# def login_register_page():
#     st.title("Login/Register")
#     option = st.radio("Select an option:", ["Login", "Register"])

#     if option == "Login":
#         email = st.text_input("Email:")
#         password = st.text_input("Password:", type="password")
#         if st.button("Login"):
#             user = authenticate_user(email, password)
#             if user:
#                 st.session_state['logged_in'] = True
#                 st.session_state['current_user'] = user
#                 st.success("Login Successful!")
#                 st.experimental_rerun()
#             else:
#                 st.error("Login Failed. Please check your credentials.")

#     elif option == "Register":
#         email = st.text_input("Email:")
#         password = st.text_input("Password:", type="password")
#         full_name = st.text_input("Full Name:")
#         weight = st.number_input("Weight (kg):")
#         height = st.text_input("Height (feet-inch):")
#         age = st.number_input("Age:")
#         exercise_time = st.number_input("Exercise Time (hours/day):")
#         bed_time = st.number_input("Bed Time (hours/day):")
#         working_time = st.number_input("Working Time (hours/day):")
#         football_time = st.number_input("Football Time (hours/day):")
#         if st.button("Register"):
#             st.info(f"Attempting to register: {email}")  # Debug message
#             if register_user(email, password, full_name, weight, height, age, exercise_time, bed_time, working_time, football_time):
#                 st.success("Registration Successful!")
#             else:
#                 st.error("Registration Failed. Please try again.")

# # Logout function
# def logout():
#     st.session_state['logged_in'] = False
#     st.session_state['current_user'] = None
#     st.experimental_rerun()

# Page for Find Position
def find_position():
    st.subheader("Find POSITION")

    st.text("Rate yourself between 1 and 100 for the following statistics:")

    stats = [
        "Overall", "Potential", "Pace Total", "Shooting Total", "Passing Total",
        "Dribbling Total", "Defending Total", "Physicality Total", "Crossing",
        "Finishing", "Freekick Accuracy", "BallControl", "Acceleration", "Reactions",
        "Balance", "Shot Power", "Stamina", "Vision", "Penalties", "Marking",
        "Goalkeeper Diving", "Goalkeeper Handling", "GoalkeeperKicking", "Goalkeeper Reflexes"
    ]

    user_inputs = {}
    for stat in stats:
        user_inputs[stat] = st.slider(f"{stat}:", min_value=1, max_value=100, value=50)

    if st.button("Submit"):
        best_match = df.sample(1).iloc[0]
        st.subheader("Output:")
        st.text(f"Position: {best_match['Best Position']}")
        st.text(f"Player's Name: {best_match['Full Name']}")
        st.text(f"Nationality: {best_match['Nationality']}")
        st.text(f"Overall: {best_match['Overall']}")
        st.text(f"Potential: {best_match['Potential']}")
        st.image(best_match['Image Link'], caption="Player Image")

# Page for Find Similar Player
def find_similar_player():
    st.subheader("Find SIMILAR PLAYER")

    age = st.number_input("Enter your age:", min_value=1, max_value=150)

    positions = ["ST", "LW", "LF", "CF", "RF", "RW", "CAM", "LM", "RM", "CM", "CDM", "LWB", "RWB", "LB", "CB", "RB", "GK"]
    preferred_position = st.selectbox("Preferred Position:", positions)

    # conditions
    if preferred_position in ["ST", "LW", "LF", "CF", "RF", "RW", "CAM"]:
        stats = ["Pace Total", "Shooting Total", "Passing Total", "Dribbling Total",
                 "Physicality Total", "Crossing", "Finishing", "Freekick Accuracy", "BallControl",
                 "Acceleration", "Reactions", "Balance", "Shot Power", "Stamina", "Vision", "Penalties", "Marking"]
    elif preferred_position in ["LM", "CM", "RM", "CDM"]:
        stats = ["Pace Total", "Shooting Total", "Passing Total", "Defending Total",
                 "Physicality Total", "Crossing", "Finishing", "Freekick Accuracy", "BallControl",
                 "Acceleration", "Reactions", "Balance", "Shot Power", "Stamina", "Vision", "Penalties"]
    elif preferred_position in ["LWB", "RWB", "LB", "CB", "RB"]:
        stats = ["Pace Total", "Shooting Total", "Passing Total", "Defending Total",
                 "Physicality Total", "Finishing", "Freekick Accuracy", "BallControl",
                 "Acceleration", "Reactions", "Balance", "Shot Power", "Stamina", "Vision", "Penalties"]
    else:
        stats = ["Goalkeeper Diving", "Goalkeeper Handling", "GoalkeeperKicking", "Goalkeeper Reflexes"]

    user_inputs = {}
    for stat in stats:
        user_inputs[stat] = st.slider(f"{stat}:", min_value=1, max_value=100, value=50)

    if st.button("Submit"):
        best_match = df.sample(1).iloc[0]

        st.subheader("Output:")
        st.text(f"Age: {age}")
        st.text(f"Position: {preferred_position}")
        st.text(f"Similar Player's Name: {best_match['Full Name']}")
        st.text(f"Nationality: {best_match['Nationality']}")
        st.text(f"Overall: {best_match['Overall']}")
        st.text(f"Potential: {best_match['Potential']}")
        st.image(best_match['Image Link'], caption="Player Image")

# Page for Know Player
def know_player():
    st.subheader("KNOW PLAYER")
    player_names = df['Known As']
    selected_player = st.selectbox("Select a player:", player_names)
    selected_row = df[df['Known As'] == selected_player]
    if st.button("Show Player Data"):
        st.write(selected_row)

# Main option page
def option_page():
    st.title("OPTIONS")
    option = st.radio("Choose an option:", ["Find POSITION", "Find SIMILAR PLAYER", "KNOW PLAYER", "LOGOUT"])

    if option == "Find POSITION":
        find_position()
    elif option == "Find SIMILAR PLAYER":
        find_similar_player()
    elif option == "KNOW PLAYER":
        know_player()
    # elif option == "LOGOUT":
    #     logout()

# Main function to run the app
# def main():
#     if st.session_state['logged_in']:
#         option_page()
#     else:
#         login_register_page()

if __name__ == "__main__":
    main()


