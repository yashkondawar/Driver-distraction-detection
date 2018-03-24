import os

shape_predictor_path    = os.path.join('data','shape_predictor_68_face_landmarks.dat')
alarm_paths             = [os.path.join('data','audio_files','short_horn.wav'),
                           os.path.join('data','audio_files','long_horn.wav'),
                           os.path.join('data','audio_files','distraction_alert.wav')]

EYE_DROWSINESS_THRESHOLD    = 0.25
EYE_DROWSINESS_INTERVAL     = 2.0
MOUTH_DROWSINESS_THRESHOLD  = 0.37
MOUTH_DROWSINESS_INTERVAL   = 1.0
DISTRACTION_INTERVAL        = 3.0
