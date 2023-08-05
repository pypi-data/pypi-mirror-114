TikUp
=====

An auto downloader and uploader for TikTok videos.

**Requirements**  
[TikTok-Api](https://github.com/davidteather/TikTok-Api), [internetarchive](https://archive.org/services/docs/api/internetarchive/index.html), [youtube-dl](https://github.com/ytdl-org/youtube-dl), and [playwright](https://github.com/Microsoft/playwright-python) on Python 3.

**How to Install**  
Install with `pip install tikup`.
Update with `pip install -U tikup`.

**How to Use**
```
usage: tikup [-h] [--no-delete] [--hashtag] [--limit LIMIT] [--use-download-archive] [--id] [--liked]
             [--folder FOLDER] [--no-upload]
             user

An auto downloader and uploader for TikTok videos.

positional arguments:
  user

optional arguments:
  -h, --help            show this help message and exit
  --no-delete           don't delete files once uploaded to the Internet Archive
  --hashtag             download this hashtag
  --limit LIMIT         set limit on amount of TikToks to download
  --use-download-archive
                        record the video url to the download archive. This will download only videos not listed in the
                        archive file. Record the IDs of all downloaded videos in it.
  --id                  download this video ID
  --liked               download this user's liked posts
  --folder FOLDER       set download destination (default: ~/.tikup)
  --no-upload           turn off uploading to the Internet Archive
```
