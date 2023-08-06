# AAT Downloader
> A package that helps download mobile AAT data.


## Install

`pip install aat_downloader`

```python
%R
print(6)
text = "text"
```

```python
R('''
print(6)
text = "text"


''')
```

## How to use

Fill me in please! Don't forget code examples:

```python
%load_ext autoreload
%autoreload 2
from aat_downloader.downloader import Downloader
# Initiate downloader with path to google services file (downloaded from Firebase)
downloader = Downloader("data/external/google-services.json")
```

    The autoreload extension is already loaded. To reload it, use:
      %reload_ext autoreload


```python
# Specify experiment name and storage folder and download data
downloader.download("eeg", "data/raw")
```

```python
downloader.delete_participants("fooddemo")
```

    Warning: Are you sure you want to delete participants of experiment: fooddemo?
     y

