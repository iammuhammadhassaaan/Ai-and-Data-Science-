# import libraries
import numpy as np
import cv2 as cv 

# # read webcam using cv
# cap = cv.VideoCapture(0)

# if cap.isOpened():
#     ret, frame = cap.read()
# else:
#     ret = False

# while ret:
#     ret, frame = cap.read()
#     cv.imshow("webcam", frame)
#     if cv.waitKey(1) == 27:
#         break

# cap.release()

import cv2 as cv

# Open the default camera (index 0) or a specific camera (index 1, 2, etc.)
cap = cv.VideoCapture(1)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Display the grayscale frame
    cv.imshow('Grayscale Frame', gray_frame)

    # Exit on key press 'q'
    if cv.waitKey(25) & 0xFF == ord("q"):
        break

# Release resources
cap.release()
cv.destroyAllWindows()