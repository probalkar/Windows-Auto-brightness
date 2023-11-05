import cv2
import time
import pygetwindow as gw
from screen_brightness_control import get_brightness, set_brightness

# Function to calculate average brightness from webcam frames
def get_ambient_light_level():
    cap = cv2.VideoCapture(0)  # 0 indicates the default webcam (change it if you have multiple cameras)

    total_brightness = 0
    num_frames = 10  # Number of frames to consider for calculating average brightness

    for _ in range(num_frames):
        ret, frame = cap.read()
        if ret:
            # Convert the frame to grayscale and calculate average brightness
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            total_brightness += cv2.mean(gray_frame)[0]

    # Release the webcam and return the average brightness
    cap.release()
    return total_brightness / num_frames

# Get the current screen brightness level
current_brightness = get_brightness(display=0)[0]  # Extract brightness value from the list

while True:
    # Get ambient light level from webcam frames
    ambient_light_level = get_ambient_light_level()

    # Calculate brightness level based on average ambient light
    brightness = (ambient_light_level / 255) * 100  # Map 0-255 to 0-100

    # Adjust screen brightness if there's a significant change
    if abs(brightness - current_brightness) > 5:  # Adjust brightness if it changes by more than 5%
        set_brightness(display=0,value=int(brightness))
        current_brightness = brightness  # Update current brightness

    # Adjust the delay time based on your preference
    time.sleep(1)