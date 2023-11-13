import pyrealsense2 as rs
import numpy as np
import csv
import os

def extract_depth_data_to_csv(bag_file, output_folder):
    # Configure depth stream
    pipeline = rs.pipeline()
    config = rs.config()
    rs.config.enable_device_from_file(config, bag_file)
    config.enable_stream(rs.stream.depth)

    # Start streaming from file
    pipeline.start(config)

    frame_count = 0
    try:
        while True:
            # Get frameset of depth
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            if not depth_frame:
                continue

            # Get depth data as numpy array
            depth_data = np.asanyarray(depth_frame.get_data())

            # Create a CSV file for each frame
            csv_file = os.path.join(output_folder, f'depth_data_{frame_count}.csv')
            with open(csv_file, 'w', newline='') as file:
                writer = csv.writer(file)
                for i in range(depth_data.shape[0]):
                    writer.writerow(depth_data[i])

            frame_count += 1

    except RuntimeError:
        pass
    finally:
        pipeline.stop()

if __name__ == "__main__":
    bag_file = 'path_to_your_bag_file.bag'  # Replace with your .bag file path
    output_folder = 'output_folder_path'    # Replace with your desired output folder path
    extract_depth_data_to_csv(bag_file, output_folder)
