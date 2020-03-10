# youtube8m-data
## Extracted YouTube 8M URLs and Labels without all the TF garbage.

[YouTube8M](https://research.google.com/youtube8m/index.html) is nice, but it comes with a lot of extra stuff that you might not want. 
If you just want the video urls and the labels, then you're in luck.

The script used to generate the files is also included in the repo.

The JSON and Pickle files are laid out a little differently, but I'm sure you can figure them both out if you need to.

If for whatever reason you want to regenerate the data, you can run something like the following (modifying paths until they make sense).
```bash
mkdir -p ~/data/yt8m/video; cd ~/data/yt8m/video 

curl data.yt8m.org/download.py | partition=2/video/train mirror=us python 
curl data.yt8m.org/download.py | partition=2/video/validate mirror=us python 
curl data.yt8m.org/download.py | partition=2/video/test mirror=us python
python parse_tfrecord.py
```
