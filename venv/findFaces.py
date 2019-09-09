import face_recognition
from pydub import AudioSegment
from pydub import playback
from PIL import Image, ImageDraw
import cv2
import os
import numpy


def create_face_encoding(ldpath):
    img = face_recognition.load_image_file(ldpath)
    return face_recognition.face_encodings(img)

def face_locations(ldpath):
    img = face_recognition.load_image_file(ldpath)
    return face_recognition.face_locations(img)

class LabelAndEncoding:
    def __init__(self, encoding, label):
        self.encoding = encoding
        self.label = label


#path = './img/craig.jpg'

#for face_location in face_locations(path):
#    top, right, bottom, left = face_location
#    face_image = face_recognition.load_image_file(path)[top:bottom, left:right]
#    pil_image = Image.fromarray(face_image)
#    pil_image.save(f'./img/{top}.jpg')


known_encodings = [
    create_face_encoding('./img/zaza.jpg')[0],
    create_face_encoding('./img/g2.jpeg')[0]
]
known_names = [
    "Craig Goodspeed",
    "Gwynneth Goodspeed"
]
sounds = [
    '/home/craig/PycharmProjects/faceRecognition/venv/sound/Howsit.m4a'
]



#anotherEncoding = create_face_encoding('./img/zaza.jpg')[0]
#print(face_recognition.compare_faces([craigEncoding], anotherEncoding));

## --> check ls -ltrh /dev/video* to get all cameras




def show_webcam():
    print(cv2.getBuildInformation())

    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
    cam = cv2.VideoCapture("rtsp://admin:password123@192.168.88.28:554/onvif1", cv2.CAP_FFMPEG)

    process_this_frame = True
    counter = 0
    while True:
        ret_val, img = cam.read()
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        if counter % 2 == 0:

            face_names = []
            counter = 0
            for face_encoding in face_encodings:
                match = face_recognition.compare_faces(known_encodings, face_encoding)
                name = "unknown"
                #the most likely will have the smallest distance
                face_distances = face_recognition.face_distance(known_encodings, face_encoding)
                best_match_index = numpy.argmin(face_distances)
                if match[best_match_index]:
                    name=known_names[best_match_index]
                    if sounds[best_match_index] is not None:
                        #TODO thread this piece of code, no need to slow the image recognition down. should also only play once per n minutes
                        playback.play(AudioSegment.from_file(sounds[best_match_index]))
                face_names.append(name)

        counter = counter + 1
        process_this_frame = not process_this_frame

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(img, (left,top), (right,bottom), (0,255,0), 1)

            font = cv2.FONT_HERSHEY_DUPLEX
            addOn = cv2.getTextSize(name, font, 1, 1 )
            rightPos = 0
            if(left + addOn[0][0]) > right:
                rightPos = (left + addOn[0][0])
            else:
                rightPos = right
            cv2.rectangle(img, (left, bottom - 35), (rightPos, bottom), (255, 0, 0), cv2.FILLED)
            cv2.putText(img, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('video0', img)
        if cv2.waitKey(1) == 27:
            break  # esc to quit
    cam.release()
    cv2.destroyAllWindows()

show_webcam()
