import dlib
import cv2
import os
import config
from Utilities import Utilities as util
from glob import glob
from tqdm import tqdm

faceDetector = dlib.get_frontal_face_detector()
landmarkDetector = dlib.shape_predictor(
    config.LANDMARK_DETECTOR_PATH
)


def shape2List(landmark):
    points = []
    for i in range(48, 68):  # 0, 68 for all, 48, 68 for lip
        points.append((landmark.part(i).x, landmark.part(i).y))
    return points


def readGrayFrames(filePath):
    frames = []
    capture = cv2.VideoCapture(filePath)

    while True:
        success, frame = capture.read()
        if not success:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frames.append(gray)
    capture.release()
    return frames


def detectLandmark(file, frames):
    landmarks = []
    for i, frame in enumerate(frames):
        faces = faceDetector(frame, 1)

        if len(faces) < 1:
            print('Skipping {}: No face detected.'.format(file))
            if len(landmarks) > 0:
                landmarks.append(landmarks[-1])
            continue

        if len(faces) > 1:
            print('Skipping {}: Too many face detected'.format(file))
            if len(landmarks) > 0:
                landmarks.append(landmarks[-1])
            continue

        face = faces[0]
        landmark = landmarkDetector(frame, face)
        landmark = shape2List(landmark)
        landmarks.append(landmark)
    return landmarks


def extractLip(frames, landmarks):
    lips = []
    for i, landmark in enumerate(landmarks):
        # Landmark corresponding to lip
        lip = landmark

        # Lip landmark sorted for determining lip region
        lip_x = sorted(lip, key=lambda pointx: pointx[0])
        lip_y = sorted(lip, key=lambda pointy: pointy[1])

        # Determine Margins for lip-only image
        x_add = int((-lip_x[0][0]+lip_x[-1][0]) * config.LIP_MARGIN)
        y_add = int((-lip_y[0][1]+lip_y[-1][1]) * config.LIP_MARGIN)

        crop_pos = (lip_x[0][0]-x_add, lip_x[-1][0]+x_add,
                    lip_y[0][1]-y_add, lip_y[-1][1]+y_add)   # Crop image

        cropped = frames[i][crop_pos[2]:crop_pos[3], crop_pos[0]:crop_pos[1]]
        cropped = cv2.resize(
            cropped, (config.LIP_CROP_SIZE[0], config.LIP_CROP_SIZE[1]), interpolation=cv2.INTER_CUBIC)        # Resize

        lips.append(cropped)
    return lips


def save(targetPath, lips):
    for i, lip in enumerate(lips):
        cv2.imwrite(targetPath + "%03d" % (i + 1) + ".jpg", lip)


def apply(speaker):
    filePath = '{}/S{}//*-03-*.mp4'.format(config.MERGE_SPLIT_DIR, speaker)
    allFiles = sorted(glob(filePath))

    for i in tqdm(range(len(allFiles)), desc='Lip extraction in progress'):
        file = allFiles[i]
        frames = readGrayFrames(file)
        landmarks = detectLandmark(file, frames)
        lips = extractLip(frames, landmarks)

        fileName = file.split('/')[-1]
        speaker, batch = util.getSpeakerBatch(fileName)
        filePrefix = fileName.split('.')[0]

        targetPath = '{}/S{}/B{}/{}/'.format(
            config.PROCESSED_VIDEO_DIR, speaker, batch, filePrefix)

        if not os.path.exists(targetPath):
            os.makedirs(targetPath)

        save(targetPath, lips)
