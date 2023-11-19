# youtube8m-data
## Extracted YouTube 8M URLs and Labels without all the TF Record parsing/features.

[YouTube8M](https://research.google.com/youtube8m/index.html) is nice, but it comes with a lot of extra stuff that you might not want.
If you just want the video urls and the labels, then you're in luck.

Video ids and labels can be downloaded from:
- [parsed_dataset_renamed_train.json](https://drive.google.com/uc?id=1V0bBAIY5HHNHFy-LQof4E2o58fpbF7z0)
- [parsed_dataset_renamed_train.pkl](https://drive.google.com/uc?id=1Cz5CoRzrHznqj4ahtTSYAeQMk1_rRS_0)
- [parsed_dataset_renamed_val.json](https://drive.google.com/uc?id=1B7Hik4rO_h-a9bXLu7cfbGecTufUbghz)
- [parsed_dataset_renamed_val.pkl](https://drive.google.com/uc?id=1w5jwhxVFzcRwZ3RUwu5-gnptkG7sjwyz)

Alternatively, run this script: `python download_dataset.py`

You can look at the videos and labels easily using the provided script:
```bash
pip install -r requirements.txt
python examine_videos.py
```

The script used to generate the files is also included in the repo.

If for whatever reason you want to regenerate the data, you can run something like the following (modifying paths until they make sense).
```bash
mkdir -p ~/data/yt8m/video; cd ~/data/yt8m/video
pip install tensorflow==1.14.0

curl data.yt8m.org/download.py | partition=2/video/train mirror=us python
curl data.yt8m.org/download.py | partition=2/video/validate mirror=us python
curl data.yt8m.org/download.py | partition=2/video/test mirror=us python
python parse_tfrecord.py
```
