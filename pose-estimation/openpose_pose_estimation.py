import cv2
import pandas as pd
import numpy as np
from openpose import pyopenpose as op

params = dict()
params["model_folder"] = "" # Replace with your OpenPose models folder path

# Initialize the OpenPose object
opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()

# Load video using OpenCV
cap = cv2.VideoCapture('') # Replace with your video file path

# Prepare an empty DataFrame to hold our data
data = pd.DataFrame()

# Process each frame
while(cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        break

    # Create new datum object and assign frame to it
    datum = op.Datum()
    datum.cvInputData = frame

    # Process the frame
    opWrapper.emplaceAndPop([datum])

    # Extract pose keypoints
    pose_keypoints = datum.poseKeypoints

    # Body keypoints order can be found here: https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/output.md#pose-output-format-coco
    if pose_keypoints is not None:
        # We'll ignore the confidence scores for simplicity
        pose_keypoints = pose_keypoints[:, :, :2].reshape(-1, 2)

        # Add keypoints to DataFrame
        df_frame = pd.DataFrame(pose_keypoints, columns=['X', 'Y'])
        
        # Calculate step length
        df_frame['step_length'] = np.sqrt((df_frame.loc[24, 'X'] - df_frame.loc[21, 'X'])**2 + (df_frame.loc[24, 'Y'] - df_frame.loc[21, 'Y'])**2)

        # Calculate arm and knee angles
        for side, shoulder, elbow, wrist, hip, knee, ankle in [('right', 2, 3, 4, 8, 9, 10), ('left', 5, 6, 7, 11, 12, 13)]:
            shoulder_to_elbow = df_frame.loc[shoulder] - df_frame.loc[elbow]
            elbow_to_wrist = df_frame.loc[elbow] - df_frame.loc[wrist]
            df_frame[f'{side}_arm_angle'] = np.degrees(np.arccos(shoulder_to_elbow.dot(elbow_to_wrist) / (np.linalg.norm(shoulder_to_elbow) * np.linalg.norm(elbow_to_wrist))))

            hip_to_knee = df_frame.loc[hip] - df_frame.loc[knee]
            knee_to_ankle = df_frame.loc[knee] - df_frame.loc[ankle]
            df_frame[f'{side}_knee_angle'] = np.degrees(np.arccos(hip_to_knee.dot(knee_to_ankle) / (np.linalg.norm(hip_to_knee) * np.linalg.norm(knee_to_ankle))))

        # Add the DataFrame to the main data
        data = pd.concat([data, df_frame])

# Release video object and close windows
cap.release()
cv2.destroyAllWindows()

# Export data to CSV
data.to_csv('pose_data.csv', index=False)
