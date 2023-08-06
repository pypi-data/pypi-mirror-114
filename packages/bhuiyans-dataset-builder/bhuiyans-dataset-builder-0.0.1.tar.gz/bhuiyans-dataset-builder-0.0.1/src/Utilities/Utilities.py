import config
import os


def getSpeakerBatch(fileName):
    speaker = fileName[0:config.SPEAKER_ID_LENGTH]
    batch = fileName[config.SPEAKER_ID_LENGTH +
                     1: config.SPEAKER_ID_LENGTH + config.BATCH_ID_LENGTH + 1]
    return speaker, batch


def getIntervalPath(fileName):
    return os.path.join(config.INTERVAL_DIR, fileName.split('.')[0] + '.csv')


def getVideoPath(fileName):
    return os.path.join(config.VIDEO_DIR, fileName.split('.')[0] + '.mp4')


def getAudioFilePath(fileName):
    return os.path.join(config.AUDIO_DIR, fileName.split('.')[0] + '.wav')


def getUncompressedVideoPath(fileName):
    return os.path.join(config.UNCOMPRESSED_VIDEO_DIR, fileName.split('.')[0] + '.mp4')


def getSeparatedAudioFilePath(fileName):
    speaker, batch = getSpeakerBatch(fileName)

    audioFilePath = "S{}/B{}/{}-%02d.wav".format(speaker, batch,
                                                 speaker + '-' + batch)

    audioFilePath = os.path.join(
        config.AUDIO_SPLIT_DIR, audioFilePath)

    return audioFilePath


def getSeparatedVideoFilePath(fileName):
    speaker, batch = getSpeakerBatch(fileName)

    videoFilePath = "S{}/B{}/{}-%02d.mp4".format(speaker, batch,
                                                 speaker + '-' + batch)

    videoFilePath = os.path.join(
        config.VIDEO_SPLIT_DIR, videoFilePath)

    return videoFilePath


def getMergedVideoFilePath(fileName):
    speaker, batch = getSpeakerBatch(fileName)

    videoFilePath = "S{}/B{}/{}-%02d.mp4".format(speaker, batch,
                                                 speaker + '-' + batch)

    videoFilePath = os.path.join(
        config.MERGE_SPLIT_DIR, videoFilePath)

    return videoFilePath
