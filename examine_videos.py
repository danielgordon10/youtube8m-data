import pickle
import random

import cv2
import tqdm
from dg_util.python_utils import misc_util, video_utils, youtube_utils

subset = "val"
SCALE = 1
WIDTH = 224 // 2 ** (SCALE - 1)
HEIGHT = 224 // 2 ** (SCALE - 1)
SEED = random.randint(0, 2 ** 31)

dataset = pickle.load(open("parsed_dataset_renamed_%s.pkl" % subset, "rb"))

cv2.namedWindow("im", cv2.WINDOW_NORMAL)
for video, label in tqdm.tqdm(dataset.items()):
    labels_on = set(label)
    video_path = youtube_utils.download_video(video)
    if video_path is None:
        continue
    frames = video_utils.get_frames(video_path, remove_video=True, max_frames=100, sample_rate=10)
    for lab in label:
        print("id:", video, "type:", dataset["vocabulary"][lab])
    print("num frames", len(frames))
    frames = video_utils.remove_border(frames)
    for frame in frames:
        frame = misc_util.resize(frame, (WIDTH, HEIGHT))
        cv2.imshow("im", frame[:, :, ::-1])
        cv2.waitKey(0)
