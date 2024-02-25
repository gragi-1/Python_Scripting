# Python
# opencv-python, dlib, numpy
import cv2
import dlib
import numpy as np

# Load the detector and predictor from dlib
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Load the face recognition model
face_rec_model = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

# Define a function to compute the face descriptor
def compute_face_descriptor(img, shape):
    face_descriptor = face_rec_model.compute_face_descriptor(img, shape)
    return np.array(face_descriptor)

# Load an image and convert it to grayscale
img = cv2.imread("face.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = detector(gray)

# For each face
for face in faces:
    # Predict the landmarks
    shape = predictor(gray, face)

    # Compute the face descriptor
    face_descriptor = compute_face_descriptor(img, shape)

    # Draw a bounding box around the face
    cv2.rectangle(img, (face.left(), face.top()), (face.right(), face.bottom()), (0, 255, 0), 2)

    # Draw a label with the face descriptor
    cv2.putText(img, str(face_descriptor), (face.left(), face.top()-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

# Display the image
cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()