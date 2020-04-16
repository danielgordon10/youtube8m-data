import csv
import pickle
import random

import cv2
import tqdm
from dg_util.python_utils import misc_util
from dg_util.python_utils import video_utils
from dg_util.python_utils import youtube_utils

subset = "val"
SCALE = 1
WIDTH = 224 // 2 ** (SCALE - 1)
HEIGHT = 224 // 2 ** (SCALE - 1)
SEED = random.randint(0, 2 ** 31)


csv_reader = csv.reader(open("vocabulary.csv", "r"))
headers = next(csv_reader, None)
rows = {key: [] for key in headers}
for row in csv_reader:
    for ii, item in enumerate(row):
        rows[headers[ii]].append(item)


dataset = pickle.load(open("parsed_dataset_renamed_%s.pkl" % subset, "rb"))
videos = dataset["ids"]
labels = dataset["labels"]
videos = list(videos)
labels = list(labels)

random.seed(SEED)
random.shuffle(videos)
random.seed(SEED)
random.shuffle(labels)

cv2.namedWindow("im", cv2.WINDOW_NORMAL)
for video, label in tqdm.tqdm(zip(videos, labels), total=len(videos)):
    labels_on = set(label)
    video_path = youtube_utils.download_video(video)
    if video_path is None:
        continue
    frames = video_utils.get_frames(video_path, remove_video=True, max_frames=100, sample_rate=10)
    for lab in label:
        print("id:", video, "type:", rows["Name"][lab])
    print("num frames", len(frames))
    frames = video_utils.remove_border(frames)
    for frame in frames:
        frame = misc_util.resize(frame, (WIDTH, HEIGHT))
        cv2.imshow("im", frame[:, :, ::-1])
        cv2.waitKey(0)
