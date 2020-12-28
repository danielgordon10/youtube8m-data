# youtube8m-data
## Extracted YouTube 8M URLs and Labels without all the TF Record parsing/features.

[YouTube8M](https://research.google.com/youtube8m/index.html) is nice, but it comes with a lot of extra stuff that you might not want. 
If you just want the video urls and the labels, then you're in luck.

Video ids and labels can be downloaded from:
- [parsed_dataset_renamed_train.json](https://drive.google.com/uc?id=1YfhT3EcbzMGgE3skkyYyGSu-YgXh0CSn)
- [parsed_dataset_renamed_train.pkl](https://drive.google.com/uc?id=1N5bbgkHwHfIVqekimEzmDRQM_4E88qFc)
- [parsed_dataset_renamed_val.json](https://drive.google.com/uc?id=1ad23TmeGa-dUgYdbxRN44erOjbp9L1Bh)
- [parsed_dataset_renamed_val.pkl](https://drive.google.com/uc?id=1P5jpF20U6R8chNCBm0dY_R5xU-y_2buP)

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
