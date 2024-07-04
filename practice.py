import cv2
import pytesseract
import time
import threading

# Configure pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust path based on your installation

# Define the license plate to detect
target_plate = "KA 19 P 8488"

# Timer duration in seconds (5 minutes)
TIMER_DURATION = 300

# Function to perform OCR on a frame and check for the target license plate
def detect_license_plate(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    print(f"Detected text: {text.strip()}")
    return target_plate in text

# Function to run the timer
def start_timer(duration, stop_event):
    time.sleep(duration)
    stop_event.set()

# Initialize the stop event
stop_event = threading.Event()

# Start the timer in a separate thread
timer_thread = threading.Thread(target=start_timer, args=(TIMER_DURATION, stop_event))
timer_thread.start()

# Open the camera
cap = cv2.VideoCapture(0)

detected = False

while not stop_event.is_set():
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame from camera.")
        break

    # Check for the license plate in the frame
    if detect_license_plate(frame):
        detected = True
        stop_event.set()
        break

    # Display the frame
    cv2.imshow('Camera', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Check the result
if detected:
    print("yay")
else:
    print("nay")
