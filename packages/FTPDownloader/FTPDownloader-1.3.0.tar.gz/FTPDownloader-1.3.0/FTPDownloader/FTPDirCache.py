import logging
import os.path

log = logging.getLogger("FTPDirCache")
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)


"""FTPDirCache
Author: tim.bleimehl@helmholtz-muenchen.de
Desc:
    This is a helper class for FTPDownloader. basicly it creates a local map of a filesystem on a remote ftp.
    This will increase the speed to find/walk files/directories on a remote ftp, if these dirs and files allready have been crawled before

    NOTES: 
        * TB Q2-2019: This was hacked together quickly and is way to complex, ugly and unmaintainable atm. YOU, fix this!

    The file system map in the self.cache attribute is nested dict, which can look like


{"path": "","name": "","type": "root","content": [
    {"path": "/","name": "DirA","type": "dir","content": [
        {"path": "/DirA","name": "DirB", "type": "dir","content": [
            {"path": "/DirA/DirB","name": "dirC","type": "dir", "content": [
                {"path": "/DirA/DirB/dirC","name": "dirD","type": "dir","content": [
                    {"path": "/DirA/DirB/dirC/dirD","name": "fileG","type": "file"}
                    ],
                }],
            }],
        },
        {"path": "/DirA","name": "DirF","type": "dir","content": [
            {"path": "/DirA/DirF","name": "dirG","type": "dir","content": [
                {"path": "/DirA/DirF/dirG","name": "fileX","type": "file"}
                ],
            }],
        }],
    }],
}
"""


class FTPDirCache:
    def __init__(self, dir_list=None):
        self.cache = None
        if dir_list is None:
            # Init cache object / Create root obj
            self._create_dir_in_cache_if_not_exists(None)
        else:
            self._create_dir_in_cache_if_not_exists(dir_list["path"])
            self._mount_obj_to_cache(dir_list)

    def read_obj_from_cache(self, path=None):
        return self._get_from_cache_by_path(self._norm_path(path))

    def write_obj_to_cache(self, dir_obj):
        self._create_dir_in_cache_if_not_exists(dir_obj["path"])

        self._mount_obj_to_cache(dir_obj)

    def is_path_fully_recursive_cached(self, path=None):
        if not self.is_path_existend_in_cache(path, False):
            # Obj does not exists and consequently is not cached
            return False
        else:
            obj = self._get_from_cache_by_path(path)
            if obj["type"] in ["dir", "root"]:
                if "content" in obj:
                    for sub_obj in obj["content"]:

                        if not self.is_path_fully_recursive_cached(
                            os.path.join(sub_obj["path"], sub_obj["name"])
                        ):
                            return False
                    # All sub obj in obj content are fully cached. consequently path is full cached
                    return True
                else:
                    # obj is of content type, but there is no content, consequently it is not fully cached

                    return False
            else:
                return True

    def is_path_existend_in_cache(self, path=None, fully_recursive=False):
        if fully_recursive:

            return self.is_path_fully_recursive_cached(path)
        obj = None
        try:
            obj = self._get_from_cache_by_path(path)
        except PathDoesNotExists:
            return False
        if obj:
            return True

    def is_obj_existend_in_cache(self, path, name=None):
        if not self.is_path_existend_in_cache(path):
            return False
        else:
            if name is not None:
                return self.is_path_existend_in_cache(os.path.join(path, name))
            else:
                return True

    def create_cache_object(self, name, path=None, obj_type="file", content=None):
        if obj_type == "root":
            path = ""
            # if content == None:
            #    content = []
        else:
            path = self._norm_path(path)
        obj = {"path": path, "name": name, "type": obj_type}
        if content is None:
            return obj
        else:
            return self._add_content_to_obj(obj, content)

    def _norm_path(self, path, remove_trailing_slash=False):
        if path in [None, ""]:
            # is root objects path
            return ""
        else:
            path = os.path.normpath(path)
        if path in ["/", "."]:
            path = "/"
        if remove_trailing_slash and path.startswith("/", 0, 1):
            path = path[1:]
        return path

    def _add_content_to_obj(self, obj, content):
        if content is None:
            content = []
        if type(content) is not list:
            content = [content]
        if type(obj) is list:
            obj.extend(content)
        else:
            if obj["type"] not in ["root", "dir"]:
                raise NonContentType(
                    "You are trying to add content, to a wrong FTP Cache Object type. Expected type 'root' or 'dir', got '{}'".format(
                        obj["type"]
                    )
                )
            if "content" in obj:
                obj["content"].extend(content)
            else:
                obj["content"] = content
        return obj

    def _mount_obj_to_cache(self, obj):
        cache_target = self._get_from_cache_by_path(obj["path"])
        if "content" not in cache_target and cache_target["type"] in ["root", "dir"]:
            cache_target["content"] = []
        return self._add_content_to_obj(cache_target, obj)

    def _mount_content_to_cache(self, path, content, overwrite=False):
        if type(content) is not list:
            raise ValueError("Tried to mount non list as cache content")
        if self.is_path_existend_in_cache(path):
            mount_point = self._get_from_cache_by_path(path)

            if "content" in mount_point:
                if len(mount_point["content"]) == 0 or overwrite:
                    mount_point["content"] = content

                    return mount_point
                else:
                    # We need an update/merge function for this later
                    raise ValueError(
                        "Mountpoint for content is not empty. Use overwrite = True '_mount_content_to_cache(self,path,content,overwrite=True)' if you know what you are doing"
                    )
            else:
                return self._add_content_to_obj(mount_point, content)
        else:
            mount_point = self._create_dir_in_cache_if_not_exists(path)
            return self._add_content_to_obj(mount_point, content)

    def _get_from_cache_by_path(self, path=None, recursive_cache_part=None):
        if path in [None, "", "/"]:
            # return root obj
            return self.cache
        if recursive_cache_part is None:
            # Start at root object
            recursive_cache_part = self.cache
            current_path = ""
        else:
            current_path = self._norm_path(
                os.path.join(recursive_cache_part["path"], recursive_cache_part["name"])
            )
        # Check if we allready in target path, if yes return cache part
        if current_path == path:
            return recursive_cache_part
        # If its nested path, we want to know the name of the next dir we have to find

        next_target_dir_name = path.replace(
            os.path.commonpath([current_path if current_path != "" else "/", path]),
            "" if current_path != "" else "/",
            1,
        ).split("/")[1]

        # Lets check if our current dir object has any content, which we can drill for other directories
        if "content" not in recursive_cache_part:
            raise PathDoesNotExists(
                "Tried to retrieve '{}' from cache but this path has no content. cache only reaches till '{}'".format(
                    path, current_path
                )
            )
        # If it has content lets browse it for our next level dir
        next_target_dir_obj = list(
            filter(
                lambda dir_obj: dir_obj["type"] == "dir"
                and dir_obj["name"] == next_target_dir_name,
                recursive_cache_part["content"],
            )
        )

        # If there is not deeper dir:
        if len(next_target_dir_obj) == 0:
            # Maybe our target is a file in our obj
            for file_obj in list(
                filter(
                    lambda file_o: file_o["type"] == "file",
                    recursive_cache_part["content"],
                )
            ):
                if os.path.join(file_obj["path"], file_obj["name"]) == path:
                    return file_obj
            # Its not a file and there is no next level dir. So our goal does not exist
            raise PathDoesNotExists(
                "Tried to retrieve '{}' from cache but this path is not cached. cache only reaches till '{}'".format(
                    path, current_path
                )
            )

        elif len(next_target_dir_obj) > 1:
            raise ValueError(
                "Something gone wrong. Looks like there is more than one directory with the same name '{}' in '{}'.".format(
                    next_target_dir_name, current_path
                )
            )
        else:
            # iterate recursive into the cache
            return self._get_from_cache_by_path(path, next_target_dir_obj[0])

    def _create_dir_in_cache_if_not_exists(self, path):

        path = self._norm_path(path)
        res = None
        # Create root object if we start fresh
        if self.cache is None:

            self.cache = self.create_cache_object(name="", path="", obj_type="root")

        if not self.is_path_existend_in_cache(path):
            splitted_path = self._path_split_all(path)
            for i, dir_name in enumerate(splitted_path):
                if i == 0:
                    tmp_path = "/"
                else:
                    tmp_path = "/" + "/".join(splitted_path[:i])
                if self.is_path_existend_in_cache(os.path.join(tmp_path, dir_name)):
                    continue
                else:
                    obj = self.create_cache_object(
                        name=dir_name, path=tmp_path, obj_type="dir"
                    )
                    res = self._mount_obj_to_cache(obj)
        return res

    def _path_split_all(self, path):
        path = self._norm_path(path, remove_trailing_slash=True)
        return path.split("/")

    def get_flat_path_list(
        self, base_path=None, list_files=True, list_directories=False
    ):
        if not list_files and not list_directories:
            return []
        file_list = []
        cache_part = self.read_obj_from_cache(base_path)
        if "content" in cache_part:
            for sub_obj in cache_part["content"]:
                sub_obj_path = os.path.join(sub_obj["path"], sub_obj["name"])
                if sub_obj["type"] == "dir":
                    if list_directories:
                        file_list.append(sub_obj_path)
                    file_list.extend(self.get_flat_path_list(sub_obj_path))
                elif sub_obj["type"] == "file":
                    file_list.append(sub_obj_path)
        return file_list


# Custom errors
class NonContentType(Exception):
    pass


class PathDoesNotExists(Exception):
    pass
