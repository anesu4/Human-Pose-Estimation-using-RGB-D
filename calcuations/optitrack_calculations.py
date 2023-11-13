import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set Variable Names
file_path_optitrack = 'Your_Optitrack_File.csv'  # Update this path as needed
patient_name_optitrack = 'PatientName' # Update this name as needed

# 1. Load the Optitrack data
optitrack_data = pd.read_csv(file_path_optitrack, header=None)

# 2. Extract position data and reshape the dataframe
body_points = [val for i, val in enumerate(optitrack_data.iloc[0]) if pd.notna(val) and "Name" not in val]
body_point_cols = {}
for i, point in enumerate(body_points):
    start_index = optitrack_data.columns[optitrack_data.iloc[0] == point][0]
    body_point_cols[point] = list(range(start_index + 2, start_index + 5))
position_data_list = [optitrack_data.iloc[:, body_point_cols[point]] for point in body_points]
position_data_optitrack = pd.concat(position_data_list, axis=1)
new_columns = []
for point in body_points:
    for coord in ['X', 'Y', 'Z']:
        new_columns.append(f"{point}_{coord}")
position_data_optitrack.columns = new_columns
position_data_optitrack = position_data_optitrack.drop([0, 1, 2]).reset_index(drop=True)

# 3. Convert heel position columns to float type and compute step length
heel_columns_float = [f" {patient_name_optitrack}_LHeel_X", f" {patient_name_optitrack}_LHeel_Y", 
                      f" {patient_name_optitrack}_LHeel_Z", f" {patient_name_optitrack}_RHeel_X", 
                      f" {patient_name_optitrack}_RHeel_Y", f" {patient_name_optitrack}_RHeel_Z"]
position_data_optitrack[heel_columns_float] = position_data_optitrack[heel_columns_float].astype(float)
position_data_optitrack['Step_Length'] = np.sqrt(
    (position_data_optitrack[f" {patient_name_optitrack}_RHeel_X"] - position_data_optitrack[f" {patient_name_optitrack}_LHeel_X"])**2 +
    (position_data_optitrack[f" {patient_name_optitrack}_RHeel_Y"] - position_data_optitrack[f" {patient_name_optitrack}_LHeel_Y"])**2 +
    (position_data_optitrack[f" {patient_name_optitrack}_RHeel_Z"] - position_data_optitrack[f" {patient_name_optitrack}_LHeel_Z"])**2
)

# 3. Calculate Knee Angle


# 3. Calculate Swing & Stance Time
# Adjust the function to handle the initial state when no event time has been set
def calculate_swing_stance_times_from_events_fixed(gait_events):
    """
    Calculate the average swing and stance times from the gait events data.

    Parameters:
    gait_events (DataFrame): Dataframe with identified gait events and timestamps

    Returns:
    float: Average swing time
    float: Average stance time
    """
    # Initialize lists to hold swing and stance times
    swing_times = []
    stance_times = []

    # We'll track the state of each foot - 'swing' or 'stance'
    right_foot_state = 'stance'
    left_foot_state = 'stance'

    # Track the last event time for each foot
    right_last_event_time = None
    left_last_event_time = None

    for index, row in gait_events.iterrows():
        # Set the initial last event times
        if right_last_event_time is None or left_last_event_time is None:
            if row['RHeelStrike']:
                right_last_event_time = row['Time']
                right_foot_state = 'stance'
            if row['LHeelStrike']:
                left_last_event_time = row['Time']
                left_foot_state = 'stance'
            continue

        # Check for right heel strike
        if row['RHeelStrike'] and right_foot_state == 'swing':
            swing_times.append(row['Time'] - right_last_event_time)
            right_foot_state = 'stance'
            right_last_event_time = row['Time']

        # Check for right toe off
        elif row['RToeOff'] and right_foot_state == 'stance':
            stance_times.append(row['Time'] - right_last_event_time)
            right_foot_state = 'swing'
            right_last_event_time = row['Time']

        # Check for left heel strike
        if row['LHeelStrike'] and left_foot_state == 'swing':
            swing_times.append(row['Time'] - left_last_event_time)
            left_foot_state = 'stance'
            left_last_event_time = row['Time']

        # Check for left toe off
        elif row['LToeOff'] and left_foot_state == 'stance':
            stance_times.append(row['Time'] - left_last_event_time)
            left_foot_state = 'swing'
            left_last_event_time = row['Time']

    # Calculate average times
    average_swing_time = np.mean(swing_times) if swing_times else 0
    average_stance_time = np.mean(stance_times) if stance_times else 0

    return average_swing_time, average_stance_time, swing_times, stance_times

# Recalculate swing and stance times for Bing
average_swing_time_bing, average_stance_time_bing, swing_times_bing, stance_times_bing = calculate_swing_stance_times_from_events_fixed(bing_gait_events)

average_swing_time_bing, average_stance_time_bing, len(swing_times_bing), len(stance_times_bing)

# 4. Save the data to a CSV file
position_data_optitrack.to_csv(f'{patient_patient_name_optitrackname}_optitrack_position_data.csv', index=False)

# # Visualize the step length over frames
# plt.figure(figsize=(12, 6))
# plt.plot(patient_name_optitrack['Step_Length'])
# plt.title("Step Length over Frames (Optitrack Data)")
# plt.xlabel("Frame")
# plt.ylabel("Step Length (units)")
# plt.grid(True)
# plt.savefig(f'{patient_name_optitrack}_optitrack_step_length.png')  # Save the plot as an image
# plt.show()