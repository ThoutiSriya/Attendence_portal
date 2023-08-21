import cv2

# Load the pre-trained Haar cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Open the webcam
webcam = cv2.VideoCapture(0)
if not webcam.isOpened():
    print("Failed to open webcam")
    exit()

while True:
    # Read the frame from the webcam
    check, frame = webcam.read()
    if not check:
        print("Error capturing frame from webcam")
        break

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Perform face detection
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the frame with detected faces
    cv2.imshow("Capturing", frame)

    # Check for the 'space' key press to exit the loop
    key = cv2.waitKey(1)
    if key == 32:
        break

# Release the webcam and close any open windows
webcam.release()
cv2.destroyAllWindows()
