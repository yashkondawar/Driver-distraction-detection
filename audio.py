from pygame import mixer

alarm_paths=['alarm_files\\short_horn.wav',
             'alarm_files\\long_horn.wav',
             'alarm_files\\distraction_alert.wav']

def audioplay(path):
    mixer.init()
    mixer.music.load(path)
    mixer.music.play()

def play_alarm(type=-1):
    if type != -1:
        audioplay(alarm_paths[type])
