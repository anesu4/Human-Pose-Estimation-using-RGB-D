import pyrealsense2 as rs

# Configure the pipeline to load the recorded depth bag file
pipeline = rs.pipeline()
config = rs.config()
config.enable_device_from_file('') # Replace with your path to the bag file - path_to_depth_bag_file.bag
 
# Start the pipeline
profile = pipeline.start(config)

# Create an align object. We'll align depth to the color stream based on default intrinsics
align = rs.align(rs.stream.color)

# Create a new BAG file writer
bag_writer = rs.recorder('', pipeline) # Replace with your path to the new BAG file - output_aligned.bag

try:
    while True:
        # Get the next set of frames from the bag file
        frames = pipeline.wait_for_frames()
        
        # Align the depth frames to the default RGB frame
        aligned_frames = align.process(frames)
        
        # Get the aligned depth frame
        aligned_depth_frame = aligned_frames.get_depth_frame()
        
        # Check if we got a valid depth frame
        if not aligned_depth_frame:
            continue

        # Write the aligned frames to the new BAG file
        bag_writer.write_frames(aligned_frames)

except Exception as e:
    print(e)

finally:
    # Stop the pipeline
    pipeline.stop()
    bag_writer.pause_recording()
