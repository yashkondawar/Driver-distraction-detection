# Driver-distraction-detection
Detects and alarms the driver when he/she is distracted while driving.
It works on three checks->
1.Checks if the driver's eye is closed.
2.Checks if the driver is yawning.
3.Checks if the driver is watching somewhere else and his face is not detected in the camera.

# How to run the program
Clone the directory in your PC and make sure you have a working webcam.
Open a terminal in this folder.
Make sure the PC has python3 installed.
Now run it using the command
> python3 main.py

The window with webcam feed will open and the algorithm will alert you if drowsiness or distraction is detected.

# Custom notifications
The data folder contains the audio files folder.
Here you can place your own audio clips that you want to use as alert tones.
This gives a personal touch to the user.
