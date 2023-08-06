# AAT Downloader
> A package that helps download mobile AAT data.


## Install

`pip install aat_downloader`

## How to use

Fill me in please! Don't forget code examples:

```python
from aat_downloader.downloader import Downloader
# Initiate downloader with path to google services file (downloaded from Firebase)
downloader = Downloader("data/external/google-services.json")

# Specify experiment name and storage folder and download data
downloader.download("eeg", "data/raw")
```
