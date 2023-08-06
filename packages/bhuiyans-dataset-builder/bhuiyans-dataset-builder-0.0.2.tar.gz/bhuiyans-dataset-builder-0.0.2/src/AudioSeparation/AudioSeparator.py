from AudioDetection.WavAudio import WavAudio
import scipy.io.wavfile as wavfile
from numpy import genfromtxt
from Utilities import Utilities as util
from tqdm import tqdm


class AudioSeparator:
    def __init__(self, audioFileName):
        self.audioFileName = audioFileName

    def apply(self):
        samplingRate, audioData = WavAudio(self.audioFileName).read()

        intervalFileName = util.getIntervalPath(self.audioFileName)
        audioFilePath = util.getSeparatedAudioFilePath(self.audioFileName)

        intervals = genfromtxt(intervalFileName, delimiter=',')

        for i in tqdm(range(len(intervals)), desc='Audio separation in progress'):
            wavfile.write(audioFilePath % (i + 1), samplingRate, audioData[int(
                samplingRate * intervals[i][0]): int(samplingRate * intervals[i][1])])
