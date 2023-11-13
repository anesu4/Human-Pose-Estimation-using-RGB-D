# Description: This script compares the step lengths from the Optitrack and RGBD datasets.
# Author: Anesu Chakaingesu
# Usage: python comprehensive_comparison.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def load_and_normalize_data(optitrack_path, rgbd_path):
    # Load the datasets
    optitrack_data = pd.read_csv(optitrack_path)
    rgbd_data = pd.read_csv(rgbd_path)
    
    # Normalize the RGBD data to match the Optitrack data range
    scale_factor = optitrack_data['Step_Length'].max() / (rgbd_data['Left_Step_Length'].max() - rgbd_data['Left_Step_Length'].min())
    rgbd_data['Left_Step_Length'] *= scale_factor
    rgbd_data['Right_Step_Length'] *= scale_factor
    
    return optitrack_data, rgbd_data

def extract_cross_section_modified(data, column_name):
    # Find peaks
    peaks, _ = find_peaks(data[column_name])
    peak_values = data[column_name].iloc[peaks]
    
    # Identify the first major spike in movement by finding the max change in step length
    first_spike_idx = data[column_name].diff().idxmax()
    
    # Get indices of 1st and 3rd highest peaks
    highest_peak_idx = peak_values.idxmax()
    third_highest_peak_idx = peak_values.nlargest(3).idxmin()
    
    # Extract cross-section
    start_idx = min(first_spike_idx, highest_peak_idx, third_highest_peak_idx)
    end_idx = max(highest_peak_idx, third_highest_peak_idx)
    
    return data.iloc[start_idx:end_idx+1]

# Provide paths to your CSV files
optitrack_path = '' # Replace with your optitrack data path
rgbd_path = '' # Replace with your RGBD data path

optitrack_data, rgbd_data = load_and_normalize_data(optitrack_path, rgbd_path)

# Side-by-Side Comparison
fig, axs = plt.subplots(1, 2, figsize=(18, 6), sharey=True)
axs[0].plot(optitrack_data['Step_Length'], color='green')
axs[0].set_title('Optitrack Step Length')
axs[0].set_xlabel('Frames')
axs[0].set_ylabel('Normalized Step Length')
axs[0].grid(True)
axs[1].plot(rgbd_data['Times'], rgbd_data['Left_Step_Length'], label='RGBD Left Step Length', color='blue')
axs[1].plot(rgbd_data['Times'], rgbd_data['Right_Step_Length'], label='RGBD Right Step Length', color='red')
axs[1].legend()
axs[1].set_title('RGBD Step Lengths')
axs[1].set_xlabel('Time (s)')
axs[1].grid(True)
plt.tight_layout()
plt.savefig('side_by_side_comparison.png')
plt.show()

# Extract cross-sections for both datasets
optitrack_cross_section = extract_cross_section_modified(optitrack_data, 'Step_Length')
rgbd_cross_section_left = extract_cross_section_modified(rgbd_data, 'Left_Step_Length')
rgbd_cross_section_right = extract_cross_section_modified(rgbd_data, 'Right_Step_Length')

# Interpolate the RGBD data
num_frames = len(optitrack_cross_section)
rgbd_left_interpolated = np.interp(np.linspace(0, len(rgbd_cross_section_left)-1, num_frames), 
                                   np.arange(len(rgbd_cross_section_left)), 
                                   rgbd_cross_section_left['Left_Step_Length'])
rgbd_right_interpolated = np.interp(np.linspace(0, len(rgbd_cross_section_right)-1, num_frames), 
                                    np.arange(len(rgbd_cross_section_right)), 
                                    rgbd_cross_section_right['Right_Step_Length'])

# Layered Comparison with Interpolated Data
plt.figure(figsize=(14, 7))
plt.plot(optitrack_cross_section.index, optitrack_cross_section['Step_Length'], label='Optitrack Step Length', color='green')
plt.plot(optitrack_cross_section.index, rgbd_left_interpolated, label='RGBD Left Step Length (Interpolated)', color='blue')
plt.plot(optitrack_cross_section.index, rgbd_right_interpolated, label='RGBD Right Step Length (Interpolated)', color='red')
plt.legend()
plt.title('Layered Comparison (Interpolated): Optitrack vs. RGBD')
plt.xlabel('Frames')
plt.ylabel('Normalized Step Length')
plt.grid(True)
plt.savefig('layered_comparison.png')
plt.show()

# Display the consolidated script
# Path: scripts/analysis/comprehensive_comparison.py
