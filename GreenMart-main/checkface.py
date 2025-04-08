import face_recognition
import cv2
import numpy as np
import pickle
import os
def store_face_encoding(imgpath,name):
    face = face_recognition.load_image_file(imgpath)
    face_encodingg = face_recognition.face_encodings(face)[0]
    fname = name+".pickle"
    with open("face_encodings\\"+fname,"wb") as cache_face:
        pickle.dump(face_encodingg,cache_face)

def delete_face_encoding(name):
    os.remove(f"face_encodings//{name}.pickle")

def get_encodings():
    fe_list = os.listdir("face_encodings")
    known_faces = []
    for encoding in fe_list:
        f = open(f"face_encodings\\{encoding}","rb")
        known_faces.append(pickle.load(f))
    return known_faces
def get_names():
    fe_list = os.listdir("face_encodings")
    known_names = []
    for fname in fe_list:
        known_names.append(fname.removesuffix(".pickle"))
    return known_names

def identify():
    video_capture = cv2.VideoCapture(0)
    ret,frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    known_face_encodings = get_encodings()
    known_face_names = get_names()
    face_names = []
    for face_encoding in face_encodings:
    # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)
    video_capture.release()
    if len(face_names):
        return face_names[0]
    else:
        return "Unknown"