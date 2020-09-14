import face_recognition
import cv2
import numpy as np
import pyttsx3
import time

engine = pyttsx3.init()
engine.setProperty('rate', 110)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def video_capture():
    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)

    # Load a sample picture and learn how to recognize it.
    Aref_image = face_recognition.load_image_file("Aref.jpg")
    Aref_face_encoding = face_recognition.face_encodings(Aref_image)[0]

    # Load a second sample picture and learn how to recognize it.
    ArefWithGlass_image = face_recognition.load_image_file("ArefWithGlass.jpg")
    ArefWithGlass_face_encoding = face_recognition.face_encodings(ArefWithGlass_image)[0]
    
    # Load a second sample picture and learn how to recognize it.
    # Amirreza_image = face_recognition.load_image_file("Amirreza.jpg")
    # Amirreza_face_encoding = face_recognition.face_encodings(Amirreza_image)[0]

    # Load a second sample picture and learn how to recognize it.
    # Father_image = face_recognition.load_image_file("father.jpg")
    # Father_face_encoding = face_recognition.face_encodings(Father_image)[0]

    # Load a second sample picture and learn how to recognize it.
    # Mother_image = face_recognition.load_image_file("mother.jpg")
    # Mother_face_encoding = face_recognition.face_encodings(Mother_image)[0]
    
    # Create arrays of known face encodings and their names
    known_face_encodings = [
        Aref_face_encoding,
        ArefWithGlass_face_encoding,
        Amirreza_face_encoding,
        # Father_face_encoding,
        # Mother_face_encoding,
    ]
    known_face_names = [
        "Aref",
        "Aref",
        "Amirreza",
    ]

    # Initialize some variables
    count = 1
    said_name = []
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    try:
            
        while True:
            # Grab a single frame of video
            ret, frame = video_capture.read()

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknow!"

                    # If a match was found in known_face_encodings, just use the first one.
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = known_face_names[first_match_index]

                    # Or instead, use the known face with the smallest distance to the new face
                    # face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    # best_match_index = np.argmin(face_distances)
                    # if matches[best_match_index]:
                    #     name = known_face_names[best_match_index]

                    face_names.append(name)

            process_this_frame = not process_this_frame


            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (255, 0, 0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                
                if name in face_names:
                    if name in said_name:
                        break
                    else:
                        say_name = "You are " + name
                        engine.say(say_name)
                        engine.runAndWait()
                        said_name.append(name)
                
                for i in range(len(said_name)):
                    if said_name[i] == "Unknow!":
                        del said_name[i]
                        time.sleep(5)
            # Display the resulting image
            cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit!
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break
    except:
        engine.say('Try Again')
        engine.runAndWait()
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
