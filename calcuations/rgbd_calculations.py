# Authors: Anesu Chakaingesu
# Date created: 2023-10-26
# Description: This script is used to calculate step lengths from RGBD data.
# Usage: python3 rgbd_calculations.py
# Parameters:
#   - patient_name: The name of the patient (e.g. Eric)
#   - filename: The name of the CSV file containing the RGBD data
# Output: A CSV file containing the RGBD data with step lengths calculated.
# Notes:
#   - The RGBD data should be in the same directory as this script.
#   - The RGBD data should be in the same format as the data exported from the
#     rgbd_data_processing.py script.
#   - The CSV file containing the RGBD data should be named
#     <patient_name>_BLAZEPOSE_points.csv
#   - The CSV file containing the RGBD data should have the following columns:
#       - Frame
#       - Time(Seconds)
#       - DavidPagnon.etc.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Load the RGBD dataset
file_path_rgbd = 'Your_RGBD_File.csv'  # Update this path as needed
rgbd_data = pd.read_csv(file_path_rgbd, header=None)

# 2. Extract positional data for relevant keypoints
rgbd_data.columns = rgbd_data.iloc[2]
rgbd_data = rgbd_data[3:].reset_index(drop=True)
rgbd_data = rgbd_data.apply(pd.to_numeric, errors='coerce')

# 3. Calculate step lengths (assuming 'LHeel' and 'RHeel' are the relevant columns)
rgbd_data['Left_Step_Length'] = np.sqrt(
    (rgbd_data['LHeel'].iloc[:, 0] - rgbd_data['RHeel'].iloc[:, 0])**2 +
    (rgbd_data['LHeel'].iloc[:, 1] - rgbd_data['RHeel'].iloc[:, 1])**2
)
rgbd_data['Right_Step_Length'] = np.sqrt(
    (rgbd_data['RHeel'].iloc[:, 0] - rgbd_data['LHeel'].iloc[:, 0])**2 +
    (rgbd_data['RHeel'].iloc[:, 1] - rgbd_data['LHeel'].iloc[:, 1])**2
)

# 3. Calculate Knee Angle 


# 3. Calculate Swing Time 
# We will consider a likelihood threshold to ensure data reliability
likelihood_threshold = 0.5

# Filter the rows where the likelihood of both the heel and the big toe of the right foot is above the threshold
reliable_data = rgbd_data[(rgbd_data['RHeel.likelihood'] > likelihood_threshold) & 
                              (rgbd_data['RBigToe.likelihood'] > likelihood_threshold)].copy()

# We'll need to identify when the right toe-off and heel-strike occur. 
# A toe-off event can be considered when the big toe 'y' coordinate starts increasing (toe moving upwards).
# A heel-strike event can be considered when the heel 'y' coordinate starts decreasing (heel moving downwards).

# Calculate the difference in the 'y' coordinates to find when the toe lifts off and the heel strikes
reliable_data['RBigToe.y.diff'] = reliable_data['RBigToe.y'].diff()
reliable_data['RHeel.y.diff'] = reliable_data['RHeel.y'].diff()

# Identify the toe-off events (when the diff is positive, it means the toe is moving upwards)
reliable_data['RToeOff'] = reliable_data['RBigToe.y.diff'] > 0

# Identify the heel-strike events (when the diff is negative, it means the heel is moving downwards)
reliable_data['RHeelStrike'] = reliable_data['RHeel.y.diff'] < 0

# Now let's find the actual events by looking at the change from False to True in these flags
reliable_data['RToeOffEvent'] = reliable_data['RToeOff'] & ~reliable_data['RToeOff'].shift(1).fillna(False)
reliable_data['RHeelStrikeEvent'] = reliable_data['RHeelStrike'] & ~reliable_data['RHeelStrike'].shift(1).fillna(False)

# Calculate the time differences between consecutive toe-off and heel-strike events to get swing times
# First, we'll create a series with timestamps of toe-off events
toe_off_times = reliable_data.loc[reliable_data['RToeOffEvent'], 'Times.seconds']

# Then create a series with timestamps of heel-strike events
heel_strike_times = reliable_data.loc[reliable_data['RHeelStrikeEvent'], 'Times.seconds']

# Calculate swing times by taking the difference between heel-strike and the next toe-off
swing_times = heel_strike_times.shift(-1) - toe_off_times
swing_times = swing_times.dropna()  # Drop the last NaN value which doesn't have a matching pair

# Calculate the average swing time
average_swing_time = swing_times.mean()

# Output the average swing time
average_swing_time, swing_times

# 3. Calculate Stance Time


# 3. Calculate Flexion from Angles
# Define a function to process each CSV file that contains knee angles and calculate the average peak knee flexion
def analyze_peak_knee_flexion_from_angles(file_path):
    # Load the data
    data = pd.read_csv(file_path)
    
    # Clean up the dataframe by setting the correct header
    data.columns = data.iloc[1] + '.' + data.iloc[2]
    data = data[3:]  # Exclude the header rows
    data = data.reset_index(drop=True)
    data = data.apply(pd.to_numeric, errors='coerce')

    # Calculate peak knee flexion for both legs
    # We take the absolute value because flexion is indicated with negative values
    peak_l_knee_flexion = data['Left knee.flexion'].abs().max()
    peak_r_knee_flexion = data['Right knee.flexion'].abs().max()

    return peak_l_knee_flexion, peak_r_knee_flexion

# Process each CSV file that contains knee angles and collect the average peak knee flexion
peak_knee_flexions_from_angles = {}

for file_path in angle_file_paths:
    peak_l_knee_flexion, peak_r_knee_flexion = analyze_peak_knee_flexion_from_angles(file_path)
    peak_knee_flexions_from_angles[file_path.split('/')[-1]] = {
        'Peak_L_Knee_Flexion': peak_l_knee_flexion,
        'Peak_R_Knee_Flexion': peak_r_knee_flexion
    }

peak_knee_flexions_from_angles

# 4. Save the processed RGBD position data to a CSV file
rgbd_data.to_csv('', index=False) # Update this path as needed - Your_Output_Path_RGBD_Processed.csv