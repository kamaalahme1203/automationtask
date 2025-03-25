import cv2
import sqlite3
from datetime import datetime

# Connect to SQLite database
conn = sqlite3.connect('people_count.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS people_count (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        count INTEGER,
        timestamp TEXT
    );
''')
conn.commit()

# Open the camera (use 0 for default camera)
cap = cv2.VideoCapture(0)

# Background subtractor for people detection
bg_subtractor = cv2.createBackgroundSubtractorMOG2()

# Initialize variables
people_count = 0
frame_number = 0

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Apply background subtraction
    fg_mask = bg_subtractor.apply(frame)

    # Threshold the foreground mask
    _, thresh = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)

    # Find contours in the binary mask
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Count people based on contour area
    for contour in contours:
        if cv2.contourArea(contour) > 500:
            people_count += 1

    # Display the frame with people count
    cv2.putText(frame, f'People Count: {people_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('People Count', frame)

    # Store people count in the database every 30 frames
    if frame_number % 30 == 0:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('INSERT INTO people_count (count, timestamp) VALUES (?, ?)', (people_count, timestamp))
        conn.commit()

    frame_number += 1

    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()

# Close the SQLite connection
conn.close()
