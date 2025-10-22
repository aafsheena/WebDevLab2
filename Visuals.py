# This creates the page for displaying data visualizations.
# It should read data from both 'data.csv' and 'data.json' to create graphs.

import streamlit as st
import pandas as pd
import json
import os

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visualizations",
    page_icon="📈",
)

# PAGE TITLE AND INFORMATION
st.title("Data Visualizations 📈")
st.write("This page displays graphs based on the collected travel data.")

# DATA LOADING
st.divider()
st.header("Load Data")

# Load CSV data
csv_data = None
if os.path.exists('data.csv'):
    csv_data = pd.read_csv('data.csv')
    st.success("CSV data loaded!")
else:
    st.warning("No CSV data found. Go to Survey page to add data!")

# Load JSON data  
json_data = None
if os.path.exists('data.json'):
    with open('data.json', 'r') as f:
        json_data = json.load(f)
    st.success("JSON data loaded!")
else:
    st.warning("JSON data file not found.")

# GRAPH CREATION
st.divider()
st.header("Graphs")

# Set up session states to remember user choices
if 'my_picks' not in st.session_state:
    st.session_state.my_picks = ["Japan", "Spain", "Morocco", "Greece", "Korea"]

if 'current_filter' not in st.session_state:
    st.session_state.current_filter = "All"

if 'chart_style' not in st.session_state:
    st.session_state.chart_style = "Bar Chart"

# GRAPH 1: STATIC GRAPH - Popular travel styles
st.subheader("Graph 1: Most Popular Travel Styles")

st.write("This graph shows which travel styles people prefer the most.")

if csv_data is not None and not csv_data.empty:
    # Count each travel style
    style_counts = csv_data['travel_style'].value_counts()
    
    # Display the chart
    st.bar_chart(style_counts)
    
    # Show the exact numbers
    st.write("**Breakdown by style:**")
    for style, count in style_counts.items():
        st.write(f"- {style}: {count} people")
else:
    st.info("No data yet. Be the first to submit on the Survey page!")

# GRAPH 2: DYNAMIC GRAPH - Dream destinations
st.subheader("Graph 2: My Dream Travel Destinations 🌍")

st.write("See how badly I want to visit different countries!")

try:
    with open('data.json', 'r') as f:
        json_data = json.load(f)
    
    # Let user pick which countries to show
    all_countries = ["Japan", "Spain", "Morocco", "Greece", "Korea"]
    user_selection = st.multiselect(
        "Pick countries to display:",
        options=all_countries,
        default=st.session_state.my_picks
    )
    
    # Save the selection
    st.session_state.my_picks = user_selection
    
    # Only show the selected countries
    filtered_list = [item for item in json_data['data_points'] if item['label'] in st.session_state.my_picks]
    
    if filtered_list:
        # Get ready for the chart
        chart_data = {}
        for item in filtered_list:
            chart_data[item['label']] = item['value']
        
        st.write(f"**Showing {len(filtered_list)} destinations** (my interest level 1-10):")
        
        # Make the bar chart
        st.bar_chart(chart_data)
        
        # Little note at the bottom
        st.caption("Changes automatically when you select different countries")
        
        # Show the numbers
        st.write("**My ratings:**")
        for item in filtered_list:
            st.write(f"- {item['label']}: {item['value']}/10")
        
    else:
        st.info("Choose at least one country from the list above!")
        
except Exception as e:
    st.error("Had trouble loading the destination data.")

# GRAPH 3: DYNAMIC GRAPH - Travel experience
st.subheader("Graph 3: Travel Experience Explorer ✈️")

st.write("Compare how many countries different travelers have visited.")

if csv_data is not None and not csv_data.empty:
    # Let user choose chart type
    chart_choice = st.radio(
        "What kind of chart?",
        ["Bar Chart", "Line Chart"],
        index=0 if st.session_state.chart_style == "Bar Chart" else 1
    )
    st.session_state.chart_style = chart_choice
    
    # Let user filter by travel style
    all_options = ["All"] + list(csv_data['travel_style'].unique())
    
    style_choice = st.selectbox(
        "Show which type of travelers?",
        all_options,
        index=all_options.index(st.session_state.current_filter) if st.session_state.current_filter in all_options else 0
    )
    
    st.session_state.current_filter = style_choice
    
    # Filter the data
    if style_choice == "All":
        working_data = csv_data
    else:
        working_data = csv_data[csv_data['travel_style'] == style_choice]
    
    if not working_data.empty:
        # Calculate average
        avg_visited = working_data['countries_visited'].mean()
        st.write(f"**Average countries visited: {avg_visited:.1f}**")
        
        # Prepare data for chart
        visit_data = working_data[['name', 'countries_visited']].set_index('name')
        
        # Show the right chart type
        if st.session_state.chart_style == "Bar Chart":
            st.bar_chart(visit_data)
        else:
            st.line_chart(visit_data)
            
        st.write(f"*Currently showing: {style_choice} travelers*")
        
else:
    st.info("Need some travel data first! Check out the Survey page.")

