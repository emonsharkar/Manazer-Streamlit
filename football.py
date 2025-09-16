import streamlit as st
import pandas as pd

# Load the DataFrame globally
df = pd.read_csv("fifaratings.csv")

# Page for Find Position
def find_position():
    st.subheader("Find POSITION")

    st.text("Rate yourself between 1 and 100 for the following statistics:")

    stats = [
        "Overall", "Potential", "Pace Total", "Shooting Total", "Passing Total,
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
    option = st.radio("Choose an option:", ["Find POSITION", "Find SIMILAR PLAYER", "KNOW PLAYER"])

    if option == "Find POSITION":
        find_position()
    elif option == "Find SIMILAR PLAYER":
        find_similar_player()
    elif option == "KNOW PLAYER":
        know_player()

# Main function to run the app
def main():
    option_page()

if __name__ == "__main__":
    main()

