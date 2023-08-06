import ftplib

from FTPDownloader.FTPDownloader_exc import (
    VerificationError,
    VerificationFailed,
    HashSumFileNotFound,
    InstanceFTPIsClosed,
)

from tqdm import tqdm

import logging
import os.path
from FTPDownloader.FTPDirCache import FTPDirCache

log = logging.getLogger("FTPDownloader")
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)

"""FTPDownloader

This class helps to bulk-download whole FTP servers or subdirectories.
It comes with a file structure caching feature which will improve file crawling times.

Author: tim.bleimehl@helmholtz-muenchen.de

TODO: Refactoring: This was quickly hacked together when i started with python and this is a mess. ~~I guess~~ a lot of improvement and simplyfication can be made in this class

Usage:
    config = {
        "url": "ftp.ncbi.nlm.nih.gov",
        "port": 21,
        "user": "anonymous",
        "pw": "anonymous",
        "base_path": "/pubmed/baseline/",
        "dest_path": /tmp/download",
        "not_to_save_extentions": ["md5", "txt"],
        "overwrite_existing": False,
        "verify_file": True,
        "verify_throw_error_when_failed": True,
        "verify_fallback_to_size_comparison": False,
    }
    dl = FTPDownloader.from_config_dict(config)
    try:
        dl.enable_progress_bar()
        dl.download_all()
    except:
        dl.close()
        raise
"""


class FTPDownloader:
    def __init__(
        self,
        url,
        dest_path,
        base_path="",
        user="anonymous",
        pw="anonymous",
        port=21,
        overwrite_existing=True,
        verify_file=True,
        verify_throw_error_when_failed=True,  # If True, script will abort download and exit, otherwise it will just warn in the logs
        verify_fallback_to_size_comparison=True,
        not_to_save_extentions=["md5"],
        verbose=False,
    ):

        self.url = url
        self.port = port
        self.base_path = base_path
        self.dest_path = dest_path
        self.user = user
        self.pw = pw
        self.not_to_save_extentions = not_to_save_extentions
        self.overwrite_existing = overwrite_existing
        self.verify_throw_error_when_failed = verify_throw_error_when_failed
        self.verify_file = verify_file
        self.verify_fallback_to_size_comparison = verify_fallback_to_size_comparison
        self.custom_get_hash_func = None
        self.hashlib_method = None

        self.ftp = None
        self.interval = 0.05
        self.cache = FTPDirCache()
        self.progress_bar = None
        self.per_file_func = None

        self.closed = False
        if verbose:
            log.setLevel(logging.DEBUG)
        else:
            log.setLevel(logging.INFO)
        self._connect()

    @classmethod
    def from_config_dict(cls, config_dict) -> "FTPDownloader":
        return cls(
            url=config_dict["url"],
            port=config_dict["port"],
            dest_path=config_dict["dest_path"],
            base_path=config_dict["base_path"],
            user=config_dict["user"],
            pw=config_dict["pw"],
            not_to_save_extentions=config_dict["not_to_save_extentions"],
            overwrite_existing=config_dict["overwrite_existing"],
            verify_file=config_dict["verify_file"],
            verify_throw_error_when_failed=config_dict[
                "verify_throw_error_when_failed"
            ],
            verify_fallback_to_size_comparison=config_dict[
                "verify_fallback_to_size_comparison"
            ],
        )

    def _connect(self):
        import socket

        self.ftp = ftplib.FTP(self.url)
        self.ftp.connect(self.url, self.port)
        self.ftp.login(self.user, self.pw)
        self.ftp.cwd(self.base_path)
        # optimize socket params for download task
        self.ftp.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.ftp.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 60)
        self.ftp.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 50)

    def _mkdir_local(self, path):
        import errno

        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

                # list(alg_map.values()).index(hashlib.md5)

    def _browse_for_remote_hash_file_alg(self, remote_file_path):
        import hashlib

        alg_map = {}
        alg_map["md5"] = hashlib.md5
        alg_map["sha1"] = hashlib.sha1
        alg_map["sha224"] = hashlib.sha224
        alg_map["sha256"] = hashlib.sha256
        alg_map["sha512"] = hashlib.sha512

        found_hash_meth = None
        hash_file_path = None
        if self.hashlib_method is None:
            hash_method_names = list(alg_map.keys())
        else:
            hash_method_names = [
                list(alg_map.keys())[list(alg_map.values()).index(self.hashlib_method)]
            ]  # get the name mapped name of the hash method..not sure if python is ugly or am i too stupid
        for hash_meth_name in hash_method_names:
            # lets try to find, files with hashes on the fpt. e.g. for the remote file "/pup/file1.txt" we try to find "/pup/file1.txt.md5" or "/pup/file1.txt.sha_224" and so on
            if self.obj_exists_on_ftp(remote_file_path + "." + hash_meth_name):
                found_hash_meth = getattr(hashlib, hash_meth_name)
                hash_file_path = remote_file_path + "." + hash_meth_name
            if self.obj_exists_on_ftp(remote_file_path + "." + hash_meth_name.upper()):
                found_hash_meth = alg_map[hash_meth_name]
                hash_file_path = self.obj_exists_on_ftp(
                    remote_file_path + "." + hash_meth_name.upper()
                )

        if found_hash_meth is not None and self.hashlib_method is None:
            # First time we found the matching hash alg. Lets save that for later...
            self.hashlib_method = found_hash_meth
        return self.hashlib_method, hash_file_path

    def default_get_hash(self, remote_file_path):
        # We are trying to get a hash of the file from server with some "standard" methods

        import hashlib
        import ftplib

        # first method is to just ask the server for the hash
        # check if ftp supports the HASH command (most ftp wont) https://tools.ietf.org/id/draft-bryan-ftp-hash-05.html
        try:
            # TODO: https://tools.ietf.org/id/draft-bryan-ftp-hash-05.html#rfc.section.3.2 atm we only ask for the currently selected hash-alg. we could get a list
            # of all supported alg and match them to hashlib.algorithms_available. When there are matches we need to weight the algs and select the best, tell the server
            # via OPTS HASH <alg> to activate it.
            lines = []
            self.ftp.retrlines("OPTS HASH", lines.append)
            hash_method_name = lines[0]
            if hash_method_name.lower() in hashlib.algorithms_available:
                hash_method = getattr(hashlib, hash_method_name.lower())
                return hash_method, self.ftp.retrlines("HASH " + remote_file_path)
        except ftplib.error_perm as e:
            pass
        # Second method is to try to find a file with the hash on the server
        # Try to find a hash file on the server
        alg, hash_file_path = self._browse_for_remote_hash_file_alg(remote_file_path)
        if hash_file_path is not None:
            lines = []
            # download the hash file to memory. line by line to a list
            self.ftp.retrlines(
                "RETR " + os.path.normpath(self.base_path + "/" + hash_file_path),
                lines.append,
            )
            # crawl the lines

            import re

            for line in lines:
                # try to find a hash
                # TODO: Extend the alg_map with hash lengths and use this information here
                hash = None
                if alg == hashlib.md5:
                    hash = re.findall(r"\b[0-9a-f]{32}\b", line)
                elif alg == hashlib.sha1:
                    hash = re.findall(r"\b[0-9a-f]{40}\b", line)
                elif alg == hashlib.sha224:
                    hash = re.findall(r"\b[0-9a-f]{56}\b", line)
                elif alg == hashlib.sha256:
                    hash = re.findall(r"\b[0-9a-f]{64}\b", line)
                elif alg == hashlib.sha512:
                    hash = re.findall(r"\b[0-9a-f]{128}\b", line)
                else:
                    raise ValueError(
                        "Tried to validate file {} with hash method '{}'. Sorry atm only md5,sha1,sha224,sha256,sha512 are supported.".format(
                            alg.__name__, remote_file_path
                        )
                    )
                if hash is not None and len(hash) == 1:
                    return alg, hash[0]
        return None, None

    def _compare_file_to_hash(
        self, local_path_source_file, comparison_hash, comparison_hash_hashlib_method
    ):
        import hashlib

        hash_inst = comparison_hash_hashlib_method()

        with open(local_path_source_file, "rb") as file_to_check:
            # Read and update hash in chunks of 4K
            for byte_block in iter(lambda: file_to_check.read(4096), b""):
                hash_inst.update(byte_block)
            hash_source = hash_inst.hexdigest()

        # with open(local_path_hash_file) as file_with_hash:
        #    hash_verify = file_with_hash.read()
        if hash_source == comparison_hash:
            return True
        else:
            return False

    def _generate_absolute_remote_path(self, path):
        if path.startswith("/"):
            path = path[1:]
        return os.path.join(self.base_path, path)

    def _verify_file_by_hash(self, local_file_path, remote_file_path):

        if self.custom_get_hash_func is not None:
            hash_method, hash = self.custom_get_hash_func(
                self._generate_absolute_remote_path(remote_file_path)
            )
        else:
            hash_method, hash = self.default_get_hash(remote_file_path)
            if hash is None:
                raise VerificationError(
                    "Could not get a hash for {}".format(remote_file_path)
                )
        return self._compare_file_to_hash(local_file_path, hash, hash_method)

    def _verify_file_by_size(self, local_file_path, remote_file_path):

        remote_size = self._get_remote_file_size(remote_file_path)
        local_size = self._get_local_file_size(local_file_path)
        if remote_size is None:
            msg = (
                "Verification by size error: Cant get remote file size for '{}'".format(
                    remote_file_path
                )
            )
            raise VerificationError(msg)
        elif self._get_local_file_size(local_file_path) == remote_size:
            return True
        else:
            msg = "Verification by size failed: Local filesize for '{}' ({}) differs from remote file '{}' size ({})".format(
                local_file_path, local_size, remote_file_path, remote_size
            )
            if self.verify_throw_error_when_failed:
                raise VerificationFailed(msg)
            else:
                log.warn(msg)
                return False

    def _verify_file(self, local_file_path, remote_file_path):
        result = None
        try:
            result = self._verify_file_by_hash(local_file_path, remote_file_path)
        except VerificationError:
            if self.verify_fallback_to_size_comparison:
                log.debug(
                    "Hash verification Failed for '{}'. Fallback to size comparison...".format(
                        local_file_path
                    )
                )
                result = self._verify_file_by_size(local_file_path, remote_file_path)
            else:
                pass
        return result

    def _get_remote_file_size(self, remote_file_path):
        currentDir = self.ftp.pwd()
        self.ftp.cwd(
            os.path.dirname(self._generate_absolute_remote_path(remote_file_path))
        )
        try:
            size = self.ftp.size(os.path.basename(remote_file_path))
            self.ftp.cwd(currentDir)
            return size
        except:
            self.ftp.cwd(currentDir)
            raise
            return None

    def _get_local_file_size(self, local_file_path):
        return os.path.getsize(local_file_path)

    def _count_files_on_ftp(
        self, base_path=None, recursive=False, count_ignored_files_too=False
    ):
        file_count = 0
        if base_path is None:
            base_path = "/"
        base_obj = self.list_ftp_directory(base_path, recursive)
        if base_obj["type"] == "file":
            raise ValueError(
                "Cant count files in file. Expected path for directory got '{}'".format(
                    base_path
                )
            )
        for obj in base_obj["content"]:
            if obj["type"] == "dir" and recursive:
                file_count += self._count_files_on_ftp(
                    os.path.join(obj["path"], obj["name"]),
                    recursive=recursive,
                    count_ignored_files_too=count_ignored_files_too,
                )
            elif obj["type"] == "file" and (
                not self._ignore_file(obj["name"]) or count_ignored_files_too
            ):
                file_count += 1
        return file_count

    def obj_exists_on_ftp(self, path, no_cache=False):
        import ftplib, os.path

        base_path = os.path.dirname(path)
        base_name = os.path.basename(path)
        if not no_cache:
            if self.cache.is_obj_existend_in_cache(path):
                # cache says object is existent, fine
                return True
            else:
                # Lets check if base_path is in cache
                if self.cache.is_path_existend_in_cache(base_path):
                    # Was this path content cached?
                    if "content" in self.cache._get_from_cache_by_path(base_path):
                        # Yes, this directory content was crawled and we did not find the obj. Now we can asume that this file does not exists
                        return False
        # From the cache we could not determine if the object exists or not. We have to look at the remote server. This is much slower, but our last resort
        for obj in list_ftp_directory(
            base_path=base_path, recursive=False, no_cache=True
        )["content"]:
            if obj["name"] == base_name:
                return True
        return False

    def list_ftp_directory(self, base_path=None, recursive=False, no_cache=False):
        if not no_cache and self.cache.is_path_existend_in_cache(base_path, recursive):
            # Queried dir is cached, lets return result from cache
            return self.cache.read_obj_from_cache(base_path)
        else:

            result_list = self._drill_ftp_dir(
                base_path=base_path, recursive=recursive, no_cache=no_cache
            )
            tmp = self.cache._mount_content_to_cache(base_path, result_list)
            return tmp

    def _drill_ftp_dir(self, base_path=None, recursive=False, no_cache=False):
        import ftplib, os.path

        if base_path == None:
            base_path = "/"
        try:
            result = []
            for name, facts in self.ftp.mlsd(
                self._generate_absolute_remote_path(base_path), ["type"]
            ):
                obj_path = os.path.join(base_path)
                obj = None
                if facts["type"] == "dir":

                    obj = self.cache.create_cache_object(
                        name=name, path=base_path, obj_type="dir"
                    )

                    if recursive:
                        obj_content = self._drill_ftp_dir(
                            os.path.join(base_path, name), recursive
                        )
                        obj = self.cache._add_content_to_obj(obj, obj_content)
                    result.append(obj)
                elif facts["type"] == "file":
                    obj = self.cache.create_cache_object(
                        name=name, path=base_path, obj_type="file"
                    )
                    result.append(obj)

            return result
        except ftplib.error_perm as e:
            log.warn("Could not drill in {}. Error:".format(os.path.join(base_path)))
            if str(e.__str__).startswith("500"):
                log.warn("Continue with legacy method list_ftp_directory_legacy()")
                return self.list_ftp_directory_legacy(base_path, recursive)
            else:
                raise

    ## Todo for FTPs with no mlsd support. Pubmed ftp (for which this file was created) does support mlsd, so no prio atm
    # https://stackoverflow.com/questions/38129981/python3-ftplib-check-if-dir-exists-via-mlsd
    def list_ftp_directory_legacy(self, path=None, recursive=False):
        raise NotImplementedError(
            "File listing for non MLSD capable FTP is not implemeted yet"
        )
        """
        items = []
        ftp.retrlines('LIST', items.append ) 
        items = map( str.split, items )
        dirlist = [ item.pop() for item in items if item[0][0] == 'd' ]
        #print( "directrys", directorys )
        #print( 'remote_ftp' in directorys )
        if not (remotefoldername in dirlist):
        ftp.mkd(remotefoldername)
        logging.debug("folder does not exitst, ftp.mkd: " + remotefoldername)
        else:
        logging.debug("folder did exist: " + remotefoldername)
        """

    def _ignore_file(self, filename):
        if filename.startswith(".", 0, 1):
            return True
        if os.path.splitext(filename)[1][1:].lower() in self.not_to_save_extentions:
            return True
        else:
            return False

    def _post_file_download(
        self, local_file_path, remote_file_path, progress_bar: tqdm
    ):
        # Verification
        if self.verify_file:
            if progress_bar is not None:
                progress_bar.set_description(
                    f"Verify '{os.path.basename(local_file_path)}'"
                )
                progress_bar.update()
                if not self._verify_file(local_file_path, remote_file_path):
                    log.warn("Verification for '{}' failed!".format(local_file_path))
                else:
                    progress_bar.progress(0, "OK: '{}'".format(local_file_path))
        # Post process defined by caller
        if self.per_file_func is not None:
            if progress_bar is not None:
                progress_bar.progress(0, "Post Process '{}'".format(local_file_path))
            if hasattr(self.per_file_func, "__call__"):
                try:
                    self.per_file_func(local_file_path)
                except Exception as e:
                    log.error(
                        "Error. Could not run custom per file function (set_per_file_function) on {}".format(
                            local_file_path
                        ),
                        e,
                    )
            else:
                log.warn(
                    "Skipped call of set_per_file_function as its not a 'callable' type. Try to use a function with one parameter for the local file path."
                )

    def _is_file_allready_downloaded(self, remote_path, verify=True):
        local_file_path = os.path.normpath(self.dest_path + remote_path)
        if os.path.isfile(local_file_path):
            if self.verify_file and verify:
                return self._verify_file(local_file_path, remote_path)
            return True

    def _get_sample_selection(self, file_list, sample_size, seed):
        file_count = len(file_list)
        indices = self._sample_distribution_index_selection(
            file_count, sample_size, seed=seed
        )
        return [file_list[i] for i in indices]

    def _get_last_files(self, file_list, file_count):
        return sorted(file_list)[-file_count:]

    def _sample_distribution_index_selection(
        self, list_length, sample_size=0.1, distr_alpha=5, distr_beta=1, seed=None
    ):
        import numpy as np

        if seed is not None:
            np.random.seed(seed=seed)
        selected = []
        if sample_size < 1:
            sample_size = int(list_length * sample_size)
        while len(selected) < sample_size:
            new_rand = (
                np.random.beta(distr_alpha, distr_beta, sample_size) * list_length
            )
            new_rand = [int(round(i)) for i in new_rand]
            selected.extend(new_rand)
            selected = list(set(selected))
        return selected[0:sample_size]

    def download_file(self, source_path, progress_bar: tqdm = None):
        local_file_path = os.path.normpath(self.dest_path + source_path)
        local_file_name = os.path.basename(local_file_path)
        local_file_dir = os.path.dirname(local_file_path)
        if self._ignore_file(local_file_name):
            return None
        else:
            if self.closed:
                raise InstanceFTPIsClosed(
                    "This FTPDownloader instances is allready closed. You can not use it anymore. Remove your close() call or create a new instance..."
                )
            if not self.overwrite_existing:
                if self._is_file_allready_downloaded(source_path):
                    return local_file_path

            # Save current server path
            currentDir = self.ftp.pwd()

            self._mkdir_local(local_file_dir)
            try:
                # Change dir on server to dir where target file is
                progress_bar.set_description("Downloading " + local_file_name)
                progress_bar.update()
                # progress_bar.progress(amount=0, suffix="Downloading " + local_file_name)
                # self.ftp.cwd(os.path.dirname(self._generate_absolute_remote_path(source_path)) + "/")
                self.ftp.retrbinary(
                    "RETR " + self._generate_absolute_remote_path(source_path),
                    open(local_file_path, "wb").write,
                )
                # change back to server current path
                # self.ftp.cwd(currentDir)
            except Exception as e:
                self.ftp.cwd(currentDir)
                log.error(
                    "Error: File ('{}') could not be downloaded to '{}'".format(
                        source_path, self.dest_path
                    ),
                    e,
                )
                raise e

            self._post_file_download(local_file_path, source_path, progress_bar)
            return local_file_path

    def download_files(self, source_path_list, progress_bar=None):
        downloaded_files_local_pathes = []
        if progress_bar == None and progress_bar != False:
            progress_bar = tqdm(total=len(source_path_list))

        for file_path in source_path_list:
            downloaded_files_local_pathes.append(
                self.download_file(file_path, progress_bar)
            )
            progress_bar.update()
        return downloaded_files_local_pathes

    def download_directory(self, path, recursive=True, progress_bar=None):
        downloaded_files = []
        if (
            progress_bar is None
            and progress_bar != False
            and self.progress_bar is not None
        ):
            file_count = self._count_files_on_ftp(path, recursive) + 1
            progress_bar = tqdm(total=file_count)
        if progress_bar.total == 0:
            progress_bar.total = self._count_files_on_ftp(path, recursive)
        for dir_obj in self.list_ftp_directory(path, recursive)["content"]:
            dir_obj_path = os.path.join(dir_obj["path"], dir_obj["name"])
            if dir_obj["type"] == "dir" and recursive:
                downloaded_files.extend(
                    self.download_directory(dir_obj_path, recursive, progress_bar)
                )
            if dir_obj["type"] == "file":
                if not self._ignore_file(dir_obj["name"]):
                    # progress_bar.progress(suffix=dir_obj_path)
                    progress_bar.set_description(desc=dir_obj_path)
                    progress_bar.update()
                    downloaded_files.append(
                        self.download_file(dir_obj_path, progress_bar)
                    )
        return downloaded_files

    def download_all(self):
        path = "/"

        if self.progress_bar is not None:
            downloaded_files_local_pathes = self.download_directory(
                path, True, self.progress_bar
            )
        else:
            downloaded_files_local_pathes = self.download_directory(path, True, False)

        log.info("Download Finished")
        return downloaded_files_local_pathes

    def download_sample(self, base_path=None, sample_size=0.05, seed=None):
        """[summary]

        Arguments:
                    base_path {string} -- Which directory is the home of all files, if none the init base_path attribute of this instance will be taken
                    sample_size {float or int} -- How many files should be downloaded. If 0-0.99 the number will be interpreted as a share of the total file count. 0.1 will download 10% of all files. if param is <= 1 the number will be interpreted as a plain filecount
                    seed {int} -- Seed for random file selection. If None selected files for sample will be truely random. if seed is set, sample filelist will be deterministic

        Returns:
            [string] -- A list if local pathes of the downloaded files
        """
        sample_file_list = self._get_sample_selection(
            file_list=self.get_remote_file_list(base_path),
            sample_size=sample_size,
            seed=seed,
        )
        if self.progress_bar.total in [None, 0]:
            self.enable_progress_bar()

        log.info(
            "Download samples: {} files of {}".format(
                len(sample_file_list), self.progress_bar.total
            )
        )
        return self.download_files(sample_file_list)

    def download_last_files(self, base_path=None, file_count=10):
        last_files = self._get_last_files(
            file_list=self.get_remote_file_list(base_path), file_count=file_count
        )
        if self.progress_bar and self.progress_bar.total in [None, 0]:
            self.enable_progress_bar()

        log.info(
            "Download last {} files (alphabetical) of {} files total.".format(
                file_count, len(self.get_remote_file_list(base_path))
            )
        )
        return self.download_files(last_files)

    def get_remote_file_list(
        self, base_path=None, include_ignored_files=False, include_full_url=False
    ):
        if base_path in [None, "", "/"]:
            base_path = "/"
        # init caching
        self.list_ftp_directory(base_path=base_path, recursive=True)
        # read list from cache
        files = self.cache.get_flat_path_list(base_path)
        files_cleaned = []
        if not include_ignored_files:
            for index, file_path in enumerate(files):
                if not self._ignore_file(os.path.basename(file_path)):
                    files_cleaned.append(files[index])
        else:
            files_cleaned = files
        if include_full_url:
            url_base = "ftp://{}:{}{}".format(
                self.url, self.port, os.path.normpath(self.base_path)
            )
            for index, file_path in enumerate(files_cleaned):
                files_cleaned[index] = url_base + files_cleaned[index]
        return files_cleaned

    def enable_progress_bar(self, enable=True, skip_counting_files=False):
        """Call this if you want to have a progress bar while downloading. But(!) this will count all files on the remote FTP-Server. This can loop some time, if you are crawling a big directory!

        Keyword Arguments:
            enable {bool} -- If you want to have a progress bar while downloading set this to true(default: {True})
            skip_counting_files {bool} -- Set this to True if you just want to download a subdirectory with download_directory(). Counting will happen later, just on the subdir then. This will save you some time.
        """
        path = "/"
        if enable and self.progress_bar is None:
            if skip_counting_files:
                self.progress_bar = tqdm(total=0)
            else:
                log.info("Indexing and counting files for progress bar rendering...")
                self.progress_bar = tqdm(
                    total=self._count_files_on_ftp(base_path=path, recursive=True)
                )
                log.info(
                    "...indexing and counting files finished. Counted {} files in total on remote server.".format(
                        self.progress_bar.total
                    )
                )
        else:
            self.progress_bar = None

    def set_per_file_post_download_func(self, func):
        self.per_file_func = func

    def set_get_custom_hash_func(self, func):
        """Define function to get the hash of a file for verifiying the file
            Use this if you have an idea how to obtain hashes from your server as the default function has to make a lot assumptions and browsing which is slow and can not guarante to find a solution

            simple example:
            ```
            def myCustomgetHashFunction(remote_file_path, ftp):
                import hashlib

                    hash = super_cool_get_md5_hash_from_server(remote_file_path)
                    # some ftp provide a hash api via HASH command https://tools.ietf.org/id/draft-bryan-ftp-hash-05.html#rfc.section.3.2
                    # like ftp.retrlines('OPTS HASH', lines.apped)
                    return hashlib.md5, hash
            ftpDownloader_instance.set_get_custom_hash_func(myCustomgetHashFunction)
            ```
        Arguments:
            func {function} -- a function with 2 params for the source file path and the ftp instance. have a look at this classes method "default_get_hash" to get an idea

        """
        self.custom_get_hash_func = func

    def close(self):
        try:
            self.ftp.quit()
        except:
            self.ftp.close()
        self.closed = True
