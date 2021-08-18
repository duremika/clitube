import curses
import cv2
import os
import sys
from moviepy.editor import *
from pytube import YouTube
import pyglet
from time import *


url = sys.argv[1]

mov = 'movie.mp4'
audio = 'audio.mp3'

try:
    os.remove(mov)
except:
    pass
try:
    os.remove(audio)
except:
    pass

yt = YouTube(url)
yt.streams.filter(file_extension='mp4').first().download(filename=mov)
video = VideoFileClip(os.path.join(mov))
video.audio.write_audiofile(os.path.join(audio))

curses.initscr()
curses.curs_set(0)

x, y = 5, 2
win = curses.newwin(y, x, 1, 1)
while True:
    x += 1
    try:
        win = curses.newwin(y, x, 1, 1)
        curses.endwin()
    except:
        break
x -= 1
while True:
    y += 1
    try:
        win = curses.newwin(y, x, 1, 1)
    except:
        break
    curses.endwin()

# win.border(5, 5, 6, 6, 1, 2, 3, 4)
win.border(0)
win.nodelay(True)

EXIT_KEY = list(map(ord, ['q', 'й', 'Q', 'Й']))
ESC = 27
EXIT_KEY.append(ESC)


cap = cv2.VideoCapture(mov)
FPS = int(cap.get(cv2.CAP_PROP_FPS))
FRAME_DELTA = 1 / FPS

retval, frame = cap.read()
number_frame = 1

x, y = len(frame[0]), len(frame)
ratio = (y / x) * 0.5
win_y, win_x = win.getmaxyx()

_x, _y = win_y // ratio, win_y

if _x > win_x:
    _x, _y = win_x, win_x * ratio

_x, _y = int(_x) - 2, int(_y) - 2

shift_x, shift_y = (win_x - 2 - _x) // 2, (win_y - 2 - _y) // 2

ASCII_ARRAY = ' .:гсохиэзёНСОЭБВШЖЁЙ'
ASCII_ARRAY2 = ' .:-=+*#%@'
# ASCII_ARRAY = ASCII_ARRAY2
KOEF_ASCII_ARRAY = 256 // len(ASCII_ARRAY) + 1


# retval = False # Debug flag


def to_ascii(string):
    return ASCII_ARRAY[int(string) // KOEF_ASCII_ARRAY]


start_time = time()
is_playing = False
while retval:
    key = win.getch()
    if not is_playing:
        is_playing = True
        sound = pyglet.media.load(audio, streaming=False)
        sound.play()
        # pyglet.app.run()
        # player.start()

    if key in EXIT_KEY or not retval:
        break
    frame = cv2.resize(frame, (_x, _y))
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    lines = []
    for line in gray_frame:
        lines.append(''.join(*[map(to_ascii, line)]))


    while True:
        now = time()
        if now < start_time + FRAME_DELTA * number_frame:
            sleep(0.001)
            continue
        if now - (start_time + FRAME_DELTA * number_frame) > 0.005:
            cap.read()
            number_frame += 1
            break

    for i in range(0, len(lines)):
        win.addstr(i + 1 + shift_y, 1 + shift_x, lines[i])

    retval, frame = cap.read()
    number_frame += 1
curses.endwin()

try:
    os.remove(mov)
except:
    pass
try:
    os.remove(audio)
except:
    pass