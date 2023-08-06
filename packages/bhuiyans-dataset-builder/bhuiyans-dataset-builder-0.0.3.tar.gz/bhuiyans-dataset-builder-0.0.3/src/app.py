import argparse
from pathlib import Path
from Compression.Compressor import Compressor
from AudioVideoMerge.AudioVideoMerger import AudioVideoMerger
from VideoSeparation.VideoSeparator import VideoSeparator
from config import AUDIO_SPLIT_DIR, VIDEO_SPLIT_DIR, MERGE_SPLIT_DIR
from AudioExtraction.AudioExtractor import AudioExtractor
from AudioExtraction.Mp4Video import Mp4Video
from AudioDetection.AudioDetector import AudioDetector
from AudioDetection.WavAudio import WavAudio
from AudioSeparation.AudioSeparator import AudioSeparator
import Utilities.Utilities as util
import VideoPlayer.VideoPlayer as player
from FaceDetection import FaceDetector as detector

parser = argparse.ArgumentParser()

parser.add_argument('--fileName')
parser.add_argument('--extractAudio')
parser.add_argument('--detectAudio')
parser.add_argument('--plot')
parser.add_argument('--separateAudio')
parser.add_argument('--separateVideo')
parser.add_argument('--mergeAudioVideo')
parser.add_argument('--playAll')
parser.add_argument('--compressBySize')
parser.add_argument('--execute')
parser.add_argument('--detectLip')
parser.add_argument('--speaker')


def extractAudio(videoFileName):
    audioExtractor = AudioExtractor(Mp4Video(videoFileName))
    audioExtractor.apply()


def detectAudio(audioFileName, plot):
    if plot == None:
        plot = False
    audioDetector = AudioDetector(WavAudio(audioFileName))
    audioDetector.apply(plot=plot)


def separateAudio(audioFileName):
    audioSeparator = AudioSeparator(audioFileName)
    audioSeparator.apply()


def separateVideo(videoFileName):
    videoSeparator = VideoSeparator(videoFileName)
    videoSeparator.apply()


def mergeAudioVideo(videoFileName):
    audioVideoMerger = AudioVideoMerger(videoFileName)
    audioVideoMerger.apply()


def playAll(fileName):
    print("playing..")
    player.playAll(fileName)


def compressBySize(fileName, factor):
    compressor = Compressor(fileName)
    compressor.applySizeCompression(factor)


def detectLip(speaker):
    detector.apply(speaker)


def addPadding():
    # add small time to front and back of asset/time/ files for smoothing
    pass


def createDirectories(fileName):
    speaker, batch = util.getSpeakerBatch(fileName)

    Path("{}/S{}/B{}".format(AUDIO_SPLIT_DIR, speaker, batch)
         ).mkdir(parents=True, exist_ok=True)

    Path("{}/S{}/B{}".format(VIDEO_SPLIT_DIR, speaker, batch)
         ).mkdir(parents=True, exist_ok=True)

    Path("{}/S{}/B{}".format(MERGE_SPLIT_DIR, speaker, batch)
         ).mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    args = parser.parse_args()

    if(args.fileName == None):
        raise Exception(
            'Missing: Requires filename.')

    createDirectories(args.fileName)

    if args.extractAudio == 'yes':
        extractAudio(args.fileName)

    if args.detectAudio == 'yes':
        detectAudio(args.fileName, args.plot)

    if args.separateAudio == 'yes':
        separateAudio(args.fileName)

    if args.separateVideo == 'yes':
        separateVideo(args.fileName)

    if args.mergeAudioVideo == 'yes':
        mergeAudioVideo(args.fileName)

    if args.playAll == 'yes':
        playAll(args.fileName)

    if args.compressBySize != None:
        compressBySize(args.fileName, args.compressBySize)

    if args.execute == 'all':
        extractAudio(args.fileName)
        detectAudio(args.fileName, args.plot)
        separateAudio(args.fileName)
        separateVideo(args.fileName)
        mergeAudioVideo(args.fileName)
        playAll(args.fileName)

    if args.detectLip == 'yes':
        if args.speaker == None:
            raise Exception('Requires speaker id for detecting lip regions.')
        detectLip(args.speaker)
