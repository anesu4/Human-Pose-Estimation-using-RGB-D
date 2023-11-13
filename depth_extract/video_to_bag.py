from __future__ import print_function
import argparse
import os
import sys
import cv2
import rosbag
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import rospy

def parser():
    basic_desc = "Convert video file(.mp4) to rosbag(.bag) file with keypoint extraction"
    main_parser = argparse.ArgumentParser(description=basic_desc)
    options = main_parser.add_argument_group("Options")

    options.add_argument("input_file", help="Path to the video file to convert")
    options.add_argument("--output_file", default="output.bag", help="Name of output bag file")
    options.add_argument("--output_dir", default="./", help="Directory of output bag file")
    options.add_argument("--sleep_rate", type=float, default=0.1, help="Time interval between video frames")
    options.add_argument("--div_num", type=int, default=1, help="Skip cycle of video frames")

    return main_parser

def extract_keypoints(frame):
    # Implement or call your keypoint extraction algorithm here
    # For simplicity, this function currently just returns the original frame
    return frame

def convert_to_rosbag(input_file, output_file, args):
    cap = cv2.VideoCapture(input_file)
    bridge = CvBridge()
    with rosbag.Bag(output_file, 'w') as bag:
        count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if count % args['div_num'] == 0:
                keypoints_frame = extract_keypoints(frame)
                ros_image = bridge.cv2_to_imgmsg(keypoints_frame, encoding="bgr8")
                bag.write('camera/image', ros_image, rospy.Time.from_sec(float(count) * args['sleep_rate']))
            count += 1
    cap.release()

def run(args):
    input_file = args.input_file
    output_dir = args.output_dir
    output_file = os.path.join(output_dir, args.output_file)
    convert_to_rosbag(input_file, output_file, vars(args))

if __name__ == "__main__":
    main_parser = parser()
    args = main_parser.parse_args()
    run(args)
