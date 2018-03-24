from audio import play_alarm
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
<<<<<<< HEAD
from pygame import mixer
=======
>>>>>>> 031a33a8a0aa541712e58d0cdecd23a4f86c5c95

#declaring constant parameters
THRESHOLD = 0.25
DROWSINESS_INTERVAL = 48
DISTRACTION_INTERVAL = 48
<<<<<<< HEAD
thread=None

class SoundPlayer(Thread):
    def __init__(self,path):
        Thread.__init__(self)
        self.path=path
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

print('main ...')
def facial_processing(args):

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

        for rect in rects:
            shape = predictor(gray, rect)
            shape = face.shape_to_np(shape)

            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = get_aspect_ratio(leftEye)
            rightEAR = get_aspect_ratio(rightEye)

            eye_aspect_ratio = (leftEAR + rightEAR) / 2.0

            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (255, 255, 255), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (255, 255, 255), 1)

            if eye_aspect_ratio < THRESHOLD:
                interval_count += 1

                if interval_count >= DROWSINESS_INTERVAL:
                    if alarm_type==-1:
                        alarm_type=0

                        if args["alarm"] != "":
                            print('running..')

                            print('in if')
                            thread = SoundPlayer(args["alarm"])
                            thread.deamon = True
                            thread.start()

                cv2.putText(frame, "DONT SLEEP!", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            else:
                interval_count = 0
                alarm_type = -1
                if thread!=None:thread.stop()
#			cv2.putText(frame, "EAR: {:.2f}".format(eye_aspect_ratio), (300, 30),
#						cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)&0xFF
        if key == ord("q"):
            break

    cv2.destroyAllWindows()
    vs.stop()

if __name__=='__main__':
    facial_processing(get_args())
=======

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

def facial_processing(args):

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

		for rect in rects:
			shape = predictor(gray, rect)
			shape = face.shape_to_np(shape)

			leftEye = shape[lStart:lEnd]
			rightEye = shape[rStart:rEnd]
			leftEAR = get_aspect_ratio(leftEye)
			rightEAR = get_aspect_ratio(rightEye)

			eye_aspect_ratio = (leftEAR + rightEAR) / 2.0

			leftEyeHull = cv2.convexHull(leftEye)
			rightEyeHull = cv2.convexHull(rightEye)
			cv2.drawContours(frame, [leftEyeHull], -1, (255, 255, 255), 1)
			cv2.drawContours(frame, [rightEyeHull], -1, (255, 255, 255), 1)

			if eye_aspect_ratio < THRESHOLD:
				interval_count += 1

				if interval_count >= DROWSINESS_INTERVAL:
					if alarm_type==-1:
						alarm_type=0

						if args["alarm"] != "":
							play_alarm(int(args['alarm']))

					cv2.putText(frame, "DONT SLEEP!", (10, 30),
								cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

			else:
				interval_count = 0
				alarm_type = -1

#			cv2.putText(frame, "EAR: {:.2f}".format(eye_aspect_ratio), (300, 30),
#						cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1)&0xFF
		if key == ord("q"):
			break

	cv2.destroyAllWindows()
	vs.stop()

if __name__=='__main__':
	facial_processing(get_args())
>>>>>>> 031a33a8a0aa541712e58d0cdecd23a4f86c5c95


