from pygame import mixer
import os
alarm_paths=[os.path.join('alarm_files','short_horn.wav'),
             os.path.join('alarm_files','long_horn.wav'),
             os.path.join('alarm_files','distraction_alert.wav')]

def audioplay(path):
    mixer.init()
    mixer.music.load(path)
    mixer.music.play()

def play_alarm(type=-1):
    if type != -1:
        audioplay(alarm_paths[type])
