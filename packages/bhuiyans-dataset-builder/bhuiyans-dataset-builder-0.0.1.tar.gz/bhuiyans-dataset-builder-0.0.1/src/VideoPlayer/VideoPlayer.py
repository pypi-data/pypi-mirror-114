import cv2
from ffpyplayer.player import MediaPlayer
import config
from glob import glob
from Utilities import Utilities as util
from tqdm import tqdm


def play(fileName):
    video = cv2.VideoCapture(fileName)
    player = MediaPlayer(fileName)

    while True:
        grabbed, frame = video.read()
        audioFrame, val = player.get_frame()
        if not grabbed:
            break
        if cv2.waitKey(28) & 0xFF == ord("q"):
            break
        cv2.imshow("Video", frame)
        if val != 'eof' and audioFrame is not None:
            image, t = audioFrame
    video.release()
    cv2.destroyAllWindows()


def playAll(fileName):
    mergedVideoFilePath = util.getMergedVideoFilePath(fileName)

    for i in tqdm(range(config.WORDS_PER_BATCH)):
        play(mergedVideoFilePath % (i + 1))
