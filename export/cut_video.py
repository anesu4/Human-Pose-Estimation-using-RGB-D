from moviepy.video.io.VideoFileClip import VideoFileClip

# Set the input file path
input_path = '' # Replace with your input file path

# set the start and end frame numbers
start_frame = 0 # Replace with your desired start frame number
end_frame = 100 # Replace with your desired end frame number

# read the video file
clip = VideoFileClip(input_path)

# get the duration of each frame
duration = 1/clip.fps

# calculate the start and end times in seconds
start_time = start_frame * duration
end_time = end_frame * duration

# extract the subclip between the start and end times
subclip = clip.subclip(start_time, end_time)

# set the output file path
output_path = '' # Replace with your output file path

# write the subclip to a new file
subclip.write_videofile(output_path)
