import gdown
import json
import tqdm

for path, url in tqdm.tqdm(json.load(open("drive_urls.json")).items()):
    gdown.download(url, path, quiet=False)
