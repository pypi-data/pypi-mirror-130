import os.path, sys

print(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
if __name__ == "__main__" and __package__ is None:
    print("Running test standalone")
    # import parent package
    os.sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    )

import importlib.util

spec = importlib.util.spec_from_file_location(
    "FTPDownloader",
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../..")
        + "/FTPDownloader/FTPDownloader_main.py"
    ),
)
FTPDownloader_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(FTPDownloader_module)
FTPDownloader = FTPDownloader_module.FTPDownloader

import inspect

# Quickly hacked manual tests
# TODO: Transfer to real test framework
print("###START TESTING FTPDownloader")
print(inspect.getfile(FTPDownloader))
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

config = {
    "url": "ftp.afthd.tu-darmstadt.de",
    "port": 21,
    "user": "anonymous",
    "pw": "anonymous",
    "base_path": "/",
    "dest_path": "/tmp/download",
    "not_to_save_extentions": ["md5", "txt"],
    "overwrite_existing": True,
    "verify_file": True,
    "verify_throw_error_when_failed": True,
    "verify_fallback_to_size_comparison": True,
}
"""
config = {
    "url": "ftp.ncbi.nlm.nih.gov",
    "port": 21,
    "user": "anonymous",
    "pw": "anonymous",
    "base_path": "/pubmed/baseline/",
    "dest_path": base_dir + "/data/raw/",
    "not_to_save_extentions": ["md5", "txt"],
    "overwrite_existing": False,
    "verify_file": True,
    "verify_throw_error_when_failed": True,
    "verify_fallback_to_size_comparison": True,
}
"""
dl = FTPDownloader.from_config_dict(config)
try:
    dl.enable_progress_bar()
    print(dl.get_remote_file_list())
    # dl.download_sample(seed=None)

    # print("FINAL RESULT", dl.cache.cache)
    # dl.download_all()
except:
    dl.close()
    raise
