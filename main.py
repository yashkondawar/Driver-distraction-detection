from audio import alarm_paths
from scipy.spatial import distance
from imutils.video import VideoStream as video
from imutils import face_utils as face
from threading import Thread
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
from pygame import mixer
import time
import gc

mixer.init()

#declaring constant parameters
EYE_THRESHOLD = 0.25
MOUTH_THRESHOLD=12
EYE_DROWSINESS_INTERVAL = 2.0
MOUTH_DROWSINESS_INTERVAL=1.0
DISTRACTION_INTERVAL = 3.0
thread=None

class SoundPlayer(Thread):
    def __init__(self,type):
        Thread.__init__(self)
        self.path=alarm_paths[type]
        self.path='audio.mp3'
    def run(self):
        mixer.init()
        print('sounding....')
        mixer.music.load(self.path)
        mixer.music.play()
    def stop(self):
        mixer.music.stop()



def get_aspect_ratio(eye):
    vertical_1 = distance.euclidean(eye[1], eye[5])
    vertical_2 = distance.euclidean(eye[2], eye[4])
    horizontal = distance.euclidean(eye[0], eye[3])
    return (vertical_1+vertical_2)/(horizontal*2) #aspect ratio of eye
 
def get_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--shape-predictor", required=True, help="path to facial landmark predictor")
    ap.add_argument("-a", "--alarm", type=str, default="", help="path alarm .WAV file")
    ap.add_argument("-w", "--webcam", type=int, default=0, help="index of webcam on system")
    return vars(ap.parse_args())


def get_max_area_rect(rects):
    if len(rects)==0: return
    areas=[]
    for rect in rects:
        areas.append(rect.area())
    return rects[areas.index(max(areas))]

def mouth_aspect_ratio(mouth):
    upper=mouth[1:4]
    lower=(mouth[5:8])[::-1]
    mars=[]
    for upper_coord , lower_coord in zip(upper,lower):
        mars.append(distance.euclidean(upper_coord,lower_coord))

    mar=sum(mars)/len(mars)
    return mar


eye_initialized=False
mouth_initialized=False
def  facial_processing(args):
    global eye_initialized,mouth_initialized
    interval_count = 0
    alarm_type = -1


    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(args["shape_predictor"])

    (lStart, lEnd) = face.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face.FACIAL_LANDMARKS_IDXS["right_eye"]

    vs = video(src=args["webcam"]).start()
    time.sleep(1.0)
    thread = None

    while True:
        frame = vs.read()
        frame = cv2.flip(frame, 1)
        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        rects = detector(gray, 0)
        rect=get_max_area_rect(rects)
        if rect!=None:

            shape = predictor(gray, rect)
            shape = face.shape_to_np(shape)

            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = get_aspect_ratio(leftEye)
            rightEAR = get_aspect_ratio(rightEye)

            inner_lips=shape[61:69]
            mar=mouth_aspect_ratio(inner_lips)

            eye_aspect_ratio = (leftEAR + rightEAR) / 2.0

            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (255, 255, 255), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (255, 255, 255), 1)

            if eye_aspect_ratio < EYE_THRESHOLD:
                if not eye_initialized:
                    eye_start_time= time.time()
                    eye_initialized=True
                if time.time()-eye_start_time >= EYE_DROWSINESS_INTERVAL:

                    alarm_type=0
                    if not mixer.music.get_busy():
                        cv2.putText(frame, "DONT SLEEP", (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                        mixer.music.load(alarm_paths[alarm_type])
                        mixer.music.play()


            else:
                eye_initialized=False
                if mixer.music.get_busy():
                    mixer.music.stop()
                #if thread!=None:thread.stop()

            if mar > MOUTH_THRESHOLD:
                if not mouth_initialized:
                    mouth_start_time= time.time()
                    mouth_initialized=True
                if time.time()-mouth_start_time >= MOUTH_DROWSINESS_INTERVAL:

                    alarm_type=0


                    print('mouth running..')

                    print('in if')
                    if not mixer.music.get_busy():
                        cv2.putText(frame, "STOP YAWNING!", (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                        mixer.music.load(alarm_paths[alarm_type])
                        mixer.music.play()


            else:
                mouth_initialized=False

                if  not eye_initialized and mixer.music.get_busy():
                    mixer.music.stop()
                #if thread!=None:thread.stop()




            for coor in shape:
                cv2.circle(frame,(coor[0],coor[1]),1,(255,0,0),-1)
            cv2.putText(frame, "EAR: {:.2f} MAR{:.2f}".format(eye_aspect_ratio,mar), (0, frame.shape[0]-3),\
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)&0xFF
        if key == ord("q"):
            break

    cv2.destroyAllWindows()
    vs.stop()


if __name__=='__main__':
	facial_processing(get_args())


