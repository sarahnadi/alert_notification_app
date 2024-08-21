import streamlit as st
import time
import random
import pandas as pd
import numpy as np

# Function to generate random simulation data with specific severity levels
def generate_simulation_data():
    parking_lots = ['Lot A', 'Lot B', 'Lot C', 'Lot D']
    exits = ['Exit 1', 'Exit 2', 'Exit 3', 'Exit 4', 'Exit 5']

    # Simulating random congestion data with predefined severity levels
    data = []
    for lot in parking_lots:  # Generate data for each parking lot
        for exit_id in exits:  # Generate data for each exit
            # Generate severity with equal probability of 0, 1, or 2
            severity = np.random.choice([0, 1, 2], p=[0.45, 0.45, 0.1])
            data.append({'Parking Lot': lot, 'Exit': exit_id, 'Severity': severity})

    return pd.DataFrame(data)

# Function to visualize the severity with color-coded circles based on new logic
def visualize_severity(severity):
    if severity == 0:
        color = 'green'
    elif severity == 1:
        color = 'yellow'
    elif severity == 2:
        color = 'red'
    return f"""
    <div style='background-color:{color}; width: 100%; padding: 10px; border-radius: 50%; text-align: center;'>
        &nbsp;
    </div>
    <div style='text-align: center; font-weight: bold; color: white;'>
        {severity}
    </div>
    """

# Function to create blinking effect for parking lots with severe congestion
def get_blinking_style():
    return """
    <style>
    @keyframes blink {
        0% { opacity: 1; }
        50% { opacity: 0; }
        100% { opacity: 1; }
    }
    .blinking {
        animation: blink 1s infinite;
    }
    </style>
    """

# Main Streamlit app
def main():
    st.title("Parking Lot Congestion Monitoring")

    # Store simulation data in session state and only update it every 10 seconds
    if 'data' not in st.session_state or 'last_refresh' not in st.session_state:
        st.session_state['data'] = generate_simulation_data()
        st.session_state['last_refresh'] = time.time()

    # Check if 10 seconds have passed since the last refresh
    if time.time() - st.session_state['last_refresh'] >= 10:
        st.session_state['data'] = generate_simulation_data()
        st.session_state['last_refresh'] = time.time()

    # Sidebar for parking lots
    st.sidebar.header("Parking Lots")
    parking_lots = st.session_state['data']['Parking Lot'].unique()
    
    # Add CSS for blinking effect
    st.markdown(get_blinking_style(), unsafe_allow_html=True)

    # Initialize selected parking lot
    if "selected_lot" not in st.session_state:
        st.session_state["selected_lot"] = parking_lots[0]
    
    # Display parking lots in the sidebar
    for lot in parking_lots:
        # Check if any exit in the lot has severity == 2
        lot_data = st.session_state['data'][st.session_state['data']['Parking Lot'] == lot]
        severe_congestion = lot_data['Severity'].max() == 2

        # Create blinking effect if there's severe congestion
        if severe_congestion:
            lot_button = st.sidebar.button(f"{lot}", key=f"{lot}_blinking")
            st.sidebar.markdown(f"<div class='blinking'>{lot}</div>", unsafe_allow_html=True)
        else:
            lot_button = st.sidebar.button(lot)
        
        # Update selected parking lot
        if lot_button:
            st.session_state["selected_lot"] = lot
    
    # Display selected parking lot's exits and severities
    selected_lot_data = st.session_state['data'][st.session_state['data']['Parking Lot'] == st.session_state["selected_lot"]]
    st.header(f"Details for {st.session_state['selected_lot']}")

    # Grid layout for exits and severity
    cols = st.columns(len(selected_lot_data))
    for idx, (_, row) in enumerate(selected_lot_data.iterrows()):
        with cols[idx]:
            st.write(f"**Exit**: {row['Exit']}")
            st.markdown(visualize_severity(row['Severity']), unsafe_allow_html=True)
    
    # Refresh the page after 30 seconds to update the data
    time.sleep(30)
    st.rerun()

if __name__ == "__main__":
    main()
