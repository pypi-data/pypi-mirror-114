from config import DEFAULT_SAMPLING_RATE, AUDIO_DIR, VIDEO_DIR
from interface import implements
from AudioExtraction.Video import Video
import subprocess
import os
from Utilities import Utilities as util


class Mp4Video(implements(Video)):
    def __init__(self, videoFileName, samplingRate=DEFAULT_SAMPLING_RATE):
        if len(videoFileName.split('/')) > 1:
            raise Exception(
                "Invalid video file name. Valid example: 001-01.mp4")

        if not videoFileName.endswith('.mp4'):
            raise TypeError(
                "{} is not a mp4 video format".format(videoFileName))

        self.videoFileName = videoFileName
        self.samplingRate = samplingRate
        self.videoFilePath = util.getVideoPath(self.videoFileName)
        self.audioFilePath = util.getAudioFilePath(self.videoFileName)

        if not os.path.isfile(self.videoFilePath):
            raise FileNotFoundError(
                "Video file '{}' not does not exists".format(self.videoFilePath))

    def extract(self):
        command = "ffmpeg -loglevel quiet -i {} -ab 160k -ac 2 -ar {} -vn {}".format(
            self.videoFilePath, self.samplingRate, self.audioFilePath)

        subprocess.call(command, shell=True)
