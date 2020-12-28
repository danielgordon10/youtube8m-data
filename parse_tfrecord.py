import glob
import itertools
import multiprocessing as mp
import os
import pickle
import urllib.request

import numpy as np
import tensorflow as tf
import tqdm

DATA_PATH = "shards/v2"

subset = "train"
TF_PARALLEL_SIZE = 1
record_names = sorted(glob.glob(os.path.join(DATA_PATH, subset, "*.tfrecord")))
batch_size = 1


def get_session():
    return tf.Session(config=tf.ConfigProto(gpu_options=tf.GPUOptions(allow_growth=True), allow_soft_placement=True))


def _parse_function(example_proto):
    features = {"id": tf.FixedLenFeature([], tf.string), "labels": tf.VarLenFeature(tf.int64)}
    parsed_features = tf.parse_single_example(example_proto, features)
    return parsed_features["id"], parsed_features["labels"]


# Creates a dataset that reads all of the examples from two files, and extracts
# the image and label features.
def get_dataset(batch_size, path):
    def get_data_generator(ind):
        dataset = tf.data.TFRecordDataset(path)
        dataset = dataset.map(_parse_function)
        return dataset

    dataset = tf.data.Dataset.from_tensor_slices(list(range(TF_PARALLEL_SIZE))).interleave(
        get_data_generator, cycle_length=TF_PARALLEL_SIZE
    )

    dataset = dataset.batch(batch_size)
    dataset_iterator = dataset.make_one_shot_iterator()
    return dataset_iterator


def get_ids(path):
    sess = get_session()
    all_ids = []
    all_labels = []
    data_iterator = get_dataset(batch_size, path)
    ids, labels = data_iterator.get_next()

    try:
        while True:
            result = sess.run([ids, labels])
            all_ids.append(result[0][0].decode("utf-8"))
            all_labels.append(result[1].values.astype(np.int32).tolist())
    except:
        sess.close()
        dataset = {"ids": all_ids, "labels": all_labels}
        pickle.dump(dataset, open(os.path.join("labels", subset, "pickles", os.path.basename(path) + ".pkl"), "wb"))

        return all_ids, all_labels


# translate fake ids into actual youtube video ids
def get_real_id(video_id):
    try:
        fp = urllib.request.urlopen("http://data.yt8m.org/2/j/i/%s/%s.js" % (video_id[:2], video_id))
        mybytes = fp.read()
        mystr = mybytes.decode("utf8")
        fp.close()
        new_id = mystr.split('"')[3]
        assert len(new_id) == 11
    except:
        return None
    return new_id


def main():
    pool = mp.Pool(500)
    if not os.path.exists(os.path.join("labels", subset, "pickles")):
        os.makedirs(os.path.join("labels", subset, "pickles"))
    new_ids = list(tqdm.tqdm(pool.imap(get_ids, record_names), total=len(record_names)))
    all_ids, all_labels = zip(*new_ids)
    all_ids = list(itertools.chain(*all_ids))
    all_labels = list(itertools.chain(*all_labels))
    dataset = {"ids": all_ids, "labels": all_labels}
    print("initial length", len(dataset["ids"]))

    new_ids = list(tqdm.tqdm(pool.imap(get_real_id, dataset["ids"]), total=len(dataset["ids"])))
    new_labels = dataset["labels"]

    existing_vals = [(id, label) for id, label in zip(new_ids, new_labels) if id is not None]
    new_ids, new_labels = zip(*existing_vals)

    dataset = {vid_id: vid_label for vid_id, vid_label in zip(new_ids, new_labels)}

    csv_reader = csv.reader(open("vocabulary.csv", "r"))
    headers = next(csv_reader, None)
    rows = {key: [] for key in headers}
    for row in csv_reader:
        for ii, item in enumerate(row):
            rows[headers[ii]].append(item)

    vocabulary = {int(row["Index"]): row["Name"] for row in rows}
    dataset = {"videos": dataset, "vocabulary": vocabulary}
    print("final length", len(new_ids))
    pickle.dump(dataset, open("parsed_dataset_renamed_%s.pkl" % subset, "wb"))
    print("done")


if __name__ == "__main__":
    main()
