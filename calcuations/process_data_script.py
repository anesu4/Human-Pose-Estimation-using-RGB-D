
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_and_process_data(filename):
    # Load data from CSV
    data = pd.read_csv(filename)
    
    # Reshape the data
    body_parts = data.iloc[0, 2:].values
    types = data.iloc[1, 2:].values
    details = data.iloc[2, 2:].values
    
    columns = [f"{body_part} {data_type} {detail}" for body_part, data_type, detail in zip(body_parts, types, details)]
    correctly_reshaped_data = pd.DataFrame(data.values[3:, 2:], columns=columns, dtype=float)
    correctly_reshaped_data.insert(0, 'Frame', data['Unnamed: 0'].values[3:].astype(int))
    correctly_reshaped_data.insert(1, 'Time(Seconds)', data['Name'].values[3:].astype(float))
    
    # Filter and rename columns
    relevant_columns = ['Frame', 'Time(Seconds)', 
                        f'{patient_name}_LHeel Position X', f'{patient_name}_LHeel Position Y', f'{patient_name}_LHeel Position Z',
                        f'{patient_name}_RHeel Position X', f'{patient_name}_RHeel Position Y', f'{patient_name}_RHeel Position Z']
    heel_data_filtered = correctly_reshaped_data[relevant_columns]
    heel_data_filtered.columns = ['Frame', 'Time(Seconds)', 
                                  'Left Heel X', 'Left Heel Y', 'Left Heel Z',
                                  'Right Heel X', 'Right Heel Y', 'Right Heel Z']
    
    # Convert data types
    heel_data_filtered = heel_data_filtered.convert_dtypes()
    
    # Calculate step length
    heel_data_filtered['Step Length'] = np.sqrt(
        (heel_data_filtered['Right Heel X'] - heel_data_filtered['Left Heel X'])**2 +
        (heel_data_filtered['Right Heel Y'] - heel_data_filtered['Left Heel Y'])**2 +
        (heel_data_filtered['Right Heel Z'] - heel_data_filtered['Left Heel Z'])**2
    )
    
    return heel_data_filtered

def visualize_step_length(data):
    # Plotting step length over time
    plt.figure(figsize=(14, 6))
    plt.plot(data['Frame'], data['Step Length'], label='Step Length', color='blue')
    plt.title('Step Length Over the Session')
    plt.xlabel('Frame')
    plt.ylabel('Step Length (in meters)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Usage:
patient_name = "" # Update this with the name of the patient

data = load_and_process_data("path_to_your_file.csv")
visualize_step_length(data)
