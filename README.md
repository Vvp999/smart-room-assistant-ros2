# Smart Room Assistant Robot (ROS 2)

A voice-controlled indoor mobile robot simulation built with ROS 2 Jazzy,
Gazebo, TurtleBot3, Nav2 and OpenCV. Say a room name, and the robot navigates
there, scans the room, and looks for a blue object.

## Features

- Voice-based room selection (Google Speech Recognition)
- Autonomous navigation with Nav2 on a saved map
- 360-degree room scan
- Blue-object detection with OpenCV (HSV thresholding, green bounding box)

## How it works

1. Voice command ("go to bedroom")
2. SpeechRecognition converts speech to text
3. Room name is matched to predefined X/Y coordinates
4. A NavigateToPose goal is sent to Nav2
5. The robot rotates 360 degrees while processing /camera/image_raw
6. OpenCV detects blue regions and reports the result

## Repository structure

- voice_navigation/: voice commands and room navigation goals
- object_detection/: room scan and blue-object detection
- worlds/: Gazebo house world
- maps/: saved map (.yaml and .pgm)
- experiments/: early YOLO tests (not used in the final pipeline)

## Requirements

- Ubuntu 24.04, ROS 2 Jazzy, Gazebo, Nav2
- TurtleBot3 packages
- Python 3: opencv-python, numpy, SpeechRecognition, PyAudio
- cv_bridge

## Running

1. Launch Gazebo with worlds/house_project.world and the TurtleBot3.
2. Start Nav2 with maps/new_house_map_final.yaml.
3. Run voice navigation:

       python3 voice_navigation/voice_room_navigator.py

4. Run the room scan:

       python3 object_detection/room_scan.py

## Limitations

- Detection is colour-based (blue), not general object recognition
- Room coordinates are predefined
- Simulation only

## Future work

- YOLO-based object recognition
- Object localization and manipulation
- Physical robot deployment
