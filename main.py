from parameters import *
from scipy.spatial import distance
from imutils import face_utils as face
from pygame import mixer
import imutils
import time
import dlib
import cv2

# Some supporting functions for facial processing

def get_max_area_rect(rects):
    if len(rects)==0: return
    areas=[]
    for rect in rects:
        areas.append(rect.area())
    return rects[areas.index(max(areas))]

def get_eye_aspect_ratio(eye):
    vertical_1 = distance.euclidean(eye[1], eye[5])
    vertical_2 = distance.euclidean(eye[2], eye[4])
    horizontal = distance.euclidean(eye[0], eye[3])
    return (vertical_1+vertical_2)/(horizontal*2) #aspect ratio of eye

def get_mouth_aspect_ratio(mouth):
    horizontal=distance.euclidean(mouth[0],mouth[4])
    vertical=0
    for coord in range(1,4):
        vertical+=distance.euclidean(mouth[coord],mouth[8-coord])
    return vertical/(horizontal*3) #mouth aspect ratio


# Facial processing

def facial_processing():
    mixer.init()
    distracton_initlized = False
    eye_initialized      = False
    mouth_initialized    = False

    detector    = dlib.get_frontal_face_detector()
    predictor   = dlib.shape_predictor(shape_predictor_path)

    ls,le = face.FACIAL_LANDMARKS_IDXS["left_eye"]
    rs,re = face.FACIAL_LANDMARKS_IDXS["right_eye"]

    cap=cv2.VideoCapture(0)

    fps_couter=0
    fps_to_display='initializing...'
    fps_timer=time.time()
    while True:
        _ , frame=cap.read()
        fps_couter+=1
        frame = cv2.flip(frame, 1)
        if time.time()-fps_timer>=1.0:
            fps_to_display=fps_couter
            fps_timer=time.time()
            fps_couter=0
        cv2.putText(frame, "FPS :"+str(fps_to_display), (frame.shape[1]-100, frame.shape[0]-10),\
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)


        #frame = imutils.resize(frame, width=900)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        rects = detector(gray, 0)
        rect=get_max_area_rect(rects)

        if rect!=None:

            distracton_initlized=False

            shape = predictor(gray, rect)
            shape = face.shape_to_np(shape)

            leftEye = shape[ls:le]
            rightEye = shape[rs:re]
            leftEAR = get_eye_aspect_ratio(leftEye)
            rightEAR = get_eye_aspect_ratio(rightEye)

            inner_lips=shape[60:68]
            mar=get_mouth_aspect_ratio(inner_lips)

            eye_aspect_ratio = (leftEAR + rightEAR) / 2.0

            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (255, 255, 255), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (255, 255, 255), 1)
            lipHull = cv2.convexHull(inner_lips)
            cv2.drawContours(frame, [lipHull], -1, (255, 255, 255), 1)

            cv2.putText(frame, "EAR: {:.2f} MAR{:.2f}".format(eye_aspect_ratio,mar), (10, frame.shape[0]-10),\
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            if eye_aspect_ratio < EYE_DROWSINESS_THRESHOLD:

                if not eye_initialized:
                    eye_start_time= time.time()
                    eye_initialized=True

                if time.time()-eye_start_time >= EYE_DROWSINESS_INTERVAL:
                    alarm_type=0
                    cv2.putText(frame, "YOU ARE SLEEPY...\nPLEASE TAKE A BREAK!", (10, 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                    if  not distracton_initlized and not mouth_initialized and not mixer.music.get_busy():
                        mixer.music.load(alarm_paths[alarm_type])
                        mixer.music.play()
            else:
                eye_initialized=False
                if not distracton_initlized and not mouth_initialized and mixer.music.get_busy():
                    mixer.music.stop()


            if mar > MOUTH_DROWSINESS_THRESHOLD:

                if not mouth_initialized:
                    mouth_start_time= time.time()
                    mouth_initialized=True

                if time.time()-mouth_start_time >= MOUTH_DROWSINESS_INTERVAL:
                    alarm_type=0
                    cv2.putText(frame, "YOU ARE YAWNING...\nDO YOU NEED A BREAK?", (10, 40),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                    if not mixer.music.get_busy():
                        mixer.music.load(alarm_paths[alarm_type])
                        mixer.music.play()
            else:
                mouth_initialized=False
                if not distracton_initlized and not eye_initialized and mixer.music.get_busy():
                    mixer.music.stop()


        else:

            alarm_type=1
            if not distracton_initlized:
                distracton_start_time=time.time()
                distracton_initlized=True

            if time.time()- distracton_start_time> DISTRACTION_INTERVAL:

                cv2.putText(frame, "EYES ON ROAD", (10, 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                if not eye_initialized and not mouth_initialized and not  mixer.music.get_busy():
                    mixer.music.load(alarm_paths[alarm_type])
                    mixer.music.play()

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(5)&0xFF
        if key == ord("q"):
            break

    cv2.destroyAllWindows()
    cap.release()


if __name__=='__main__':
	facial_processing()


