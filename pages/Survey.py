# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Travel Survey",
    page_icon="✈️",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Travel Preferences Survey ✈️")
st.write("Please fill out the form below to share your travel preferences!")

# DATA INPUT FORM
with st.form("travel_form"):
    # Create text input widgets for the user to enter data.
    name_input = st.text_input("Enter your name:")
    destination_input = st.text_input("Enter your dream destination:")
    
    # Dropdown for travel style instead of free text
    style_input = st.selectbox(
        "What type of traveler are you?",
        ["Adventure 🏔️", "Relaxation 🏖️", "Foodie 🍜", "Culture 🎨", "City Explorer 🏙️"]
    )
    
    # Number input for countries visited
    countries_input = st.number_input("How many countries have you visited?", min_value=0, max_value=100, value=0)

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Travel Data")

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        # Create a dictionary with the new data
        new_data = {
            "name": name_input,
            "destination": destination_input,
            "travel_style": style_input,
            "countries_visited": countries_input
        }
        
        # Convert to DataFrame
        new_row = pd.DataFrame([new_data])
        
        # Check if file exists and append data
        if os.path.exists('data.csv'):
            # Read existing data and append new row
            existing_data = pd.read_csv('data.csv')
            updated_data = pd.concat([existing_data, new_row], ignore_index=True)
        else:
            # Create new file with the first row
            updated_data = new_row
        
        # Save to CSV
        updated_data.to_csv('data.csv', index=False)
        
        st.success("Your travel data has been submitted! 🎉")
        st.write(f"**Name:** {name_input}")
        st.write(f"**Dream Destination:** {destination_input}")
        st.write(f"**Travel Style:** {style_input}")
        st.write(f"**Countries Visited:** {countries_input}")


# DATA DISPLAY
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Travel Data")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv('data.csv')
    # Display the DataFrame as a table.
    st.dataframe(current_data_df)
else:
    st.warning("No travel data collected yet. Be the first to submit!")
