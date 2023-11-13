# Description: This script compares the step lengths from the Optitrack and RGBD datasets.
#
# Usage: python comparison.py
#

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_and_normalize_data(optitrack_path, rgbd_path):
    # Load the datasets
    optitrack_data = pd.read_csv(optitrack_path)
    rgbd_data = pd.read_csv(rgbd_path)
    
    # Normalize the RGBD data to match the Optitrack data range
    scale_factor = optitrack_data['Step_Length'].max() / (rgbd_data['Left_Step_Length'].max() - rgbd_data['Left_Step_Length'].min())
    rgbd_data['Left_Step_Length'] *= scale_factor
    rgbd_data['Right_Step_Length'] *= scale_factor
    
    return optitrack_data, rgbd_data

def plot_comparison(optitrack_data, rgbd_data):
    # Plotting the step lengths from both sources for comparison
    plt.figure(figsize=(14, 7))
    plt.plot(optitrack_data['Step_Length'], label='Optitrack Step Length', color='green')
    plt.plot(rgbd_data['Left_Step_Length'], label='RGBD Left Step Length', color='blue')
    plt.plot(rgbd_data['Right_Step_Length'], label='RGBD Right Step Length', color='red')
    plt.legend()
    plt.title('Step Length Comparison: Optitrack vs. RGBD')
    plt.xlabel('Time/Frames')
    plt.ylabel('Normalized Step Length')
    plt.grid(True)
    plt.show()

# Provide paths to your CSV files
optitrack_path = 'your_optitrack_data_path.csv'
rgbd_path = 'your_rgbd_data_path.csv'

optitrack_data, rgbd_data = load_and_normalize_data(optitrack_path, rgbd_path)
plot_comparison(optitrack_data, rgbd_data)

# Save the normalized RGBD data to a CSV file
rgbd_data.to_csv('your_output_path_rgbd_normalized.csv', index=False)

# Save the comparison plot to an image file
plt.savefig('step_length_comparison.png')

