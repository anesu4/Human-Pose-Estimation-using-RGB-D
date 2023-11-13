
# Human Pose Estimation Capstone Project

## Introduction
This repository contains all the materials related to the capstone project titled "Human Pose Estimation" by Anesu Chakaingesu. The project focuses on the analysis and application of human pose estimation using RGB-D cameras, particularly in the healthcare sector.

## Project Overview
The project aims to evaluate the efficacy of RGB-D technology in human pose estimation, benchmarking against the OptiTrack Flex 13 system. It explores the advancements in RGB-D camera technology and deep learning algorithms for accurate human pose detection.

### Key Objectives:
- Compare the accuracy of RGB-D technology against OptiTrack Flex 13.
- Develop algorithms for precise human pose estimation.
- Assess the practicality and potential applications in healthcare.

## Repository Contents

### `extract_2d_pose.ipynb`
Jupyter Notebook containing the code for extracting 2D human poses from video data using state-of-the-art algorithms like OpenPose and BlazePose.

### `comparison.py`
A Python script for comparing the performance and accuracy of different pose estimation models.

### `comprehensive_comparison.py`
An extended version of `comparison.py` providing more detailed comparative analysis between models.

### `cut_video.py`
Script for segmenting video into smaller clips for easier processing and analysis.

### `export_all_xdf_to_csv.m`
MATLAB script to convert XDF files (commonly used in motion capture systems like OptiTrack) to CSV format for analysis.

### `realsense_capture.py`
Python script for capturing RGB and depth data using the Intel RealSense camera.

## Research Documentation
- `Human Pose Estimation.pdf`: Detailed documentation of the project, including methodology, experiments, results, and conclusions.

## Setup and Installation
### Setup requires cloning of following repositories:
- https://github.com/IntelRealSense/librealsense

- https://github.com/CMU-Perceptual-Computing-Lab/openpose

- https://github.com/vietanhdev/tf-blazepose

- https://github.com/Cecilimon/video2bag


### Installation
python scripts require the following packages:
- numpy
- pandas
- matplotlib
- seaborn
- opencv-python
- pyrealsense2

## Usage
Install all packages and libraries and run python scripts with the appropriate arguments.

## License
Many thanks to RealSense Library, David Cecilio, David Pagnon and the OpenPose team for their open-source contributions. Links to their repositories are provided below:

- https://github.com/davidpagnon
- https://github.com/IntelRealSense

## Contact
Anesu Chakaingesu 
LinkedIn: https://www.linkedin.com/in/anesu-chakaingesu/
