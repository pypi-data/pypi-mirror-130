# FTPDownloader

**DEPRACATED** / **NOT MAINTAINED** I am only here for some downstream dependecies

This is a wrapper for "ftplib" to help bulk downloading directories on a FTP Server

## Install

`pip3 install git+https://git.connect.dzd-ev.de/dzdpythonmodules/ftpdownloader`

## How to use

```python
from FTPDownloader import FTPDownloader

config = {
    "url": "ftp.ncbi.nlm.nih.gov",
    "port": 21,
    "user": "anonymous",
    "pw": "anonymous",
    "base_path": "/bioproject/Schema.v.1.2/",
    "dest_path": "/tmp/data/",
    "not_to_save_extentions": ["md5", "txt"],
    "overwrite_existing": True,
    "verify_file": True,
    "verify_throw_error_when_failed": True,
    "verify_fallback_to_size_comparison": False,
}
dl = FTPDownloader.from_config_dict(config)
# Optional list all files and dirs
dl.get_remote_file_list()
print(dl.list_ftp_directory())
# Download all files with a progress bar
dl.enable_progress_bar()
dl.download_all()
```
