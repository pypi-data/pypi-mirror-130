if __name__ == "__main__" and __package__ is None:
    import os, sys

    print("Running test standalone")
    # import parent package
    os.sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    )

# from FTPDownloader.FTPDirCache import FTPDirCache

import importlib.util

spec = importlib.util.spec_from_file_location(
    "FTPDirCache",
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../..")
        + "/FTPDownloader/FTPDirCache.py"
    ),
)
FTPDirCache_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(FTPDirCache_module)
FTPDirCache = FTPDirCache_module.FTPDirCache


# Quickly hacked manual tests
# TODO: Transfer to real test framework

# test start with init cache

print("Test1: Init with existing cache obj")
test_cache_obj = {
    "path": "/DirA",
    "name": "DirB",
    "type": "dir",
    "content": [
        {"path": "/DirA/DirB", "name": "fileD", "type": "file"},
        {
            "path": "/DirA/DirB",
            "name": "dirC",
            "type": "dir",
            "content": [{"path": "/DirA/DirB/dirC", "name": "fileE", "type": "file"}],
        },
    ],
}

cache = FTPDirCache(test_cache_obj)
result = cache.read_obj_from_cache()
expected_result = {
    "path": "",
    "name": "",
    "type": "root",
    "content": [
        {
            "path": "/",
            "name": "DirA",
            "type": "dir",
            "content": [
                {
                    "path": "/DirA",
                    "name": "DirB",
                    "type": "dir",
                    "content": [
                        {"path": "/DirA/DirB", "name": "fileD", "type": "file"},
                        {
                            "path": "/DirA/DirB",
                            "name": "dirC",
                            "type": "dir",
                            "content": [
                                {
                                    "path": "/DirA/DirB/dirC",
                                    "name": "fileE",
                                    "type": "file",
                                }
                            ],
                        },
                    ],
                }
            ],
        }
    ],
}
assert result == expected_result
print("Test1: Cool? : {}".format(result == expected_result))
print("Test2: Add object to cache")
result = cache.read_obj_from_cache("/DirA/DirB")
expected_result = {
    "path": "/DirA",
    "name": "DirB",
    "type": "dir",
    "content": [
        {"path": "/DirA/DirB", "name": "fileD", "type": "file"},
        {
            "path": "/DirA/DirB",
            "name": "dirC",
            "type": "dir",
            "content": [{"path": "/DirA/DirB/dirC", "name": "fileE", "type": "file"}],
        },
    ],
}
assert result == expected_result
print("Test2: Cool? : {}".format(result == expected_result))


print("Test3: Start empty")
# test start with empty cache
cache = FTPDirCache()
result = cache.read_obj_from_cache()
expected_result = {"path": "", "name": "", "type": "root"}
print(result)
assert result == expected_result
print("Test3: Cool? : {}".format(result == expected_result))

print("Test4: Add obj to empty")
new_cache_obj = {
    "path": "/DirA/DirB/dirC",
    "name": "dirD",
    "type": "dir",
    "content": [{"path": "/DirA/DirB/dirC/dirD", "name": "fileG", "type": "file"}],
}
expected_result = {
    "path": "",
    "name": "",
    "type": "root",
    "content": [
        {
            "path": "/",
            "name": "DirA",
            "type": "dir",
            "content": [
                {
                    "path": "/DirA",
                    "name": "DirB",
                    "type": "dir",
                    "content": [
                        {
                            "path": "/DirA/DirB",
                            "name": "dirC",
                            "type": "dir",
                            "content": [
                                {
                                    "path": "/DirA/DirB/dirC",
                                    "name": "dirD",
                                    "type": "dir",
                                    "content": [
                                        {
                                            "path": "/DirA/DirB/dirC/dirD",
                                            "name": "fileG",
                                            "type": "file",
                                        }
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ],
        }
    ],
}
cache.write_obj_to_cache(new_cache_obj)
result = cache.read_obj_from_cache()
assert result == expected_result
print("Test4: Cool? : {}".format(result == expected_result))
print("Test5: Add single file to new dir")
new_file_obj = {"path": "/DirA/DirF/dirG", "name": "fileY", "type": "file"}
cache.write_obj_to_cache(new_file_obj)

expected_result = {
    "path": "",
    "name": "",
    "type": "root",
    "content": [
        {
            "path": "/",
            "name": "DirA",
            "type": "dir",
            "content": [
                {
                    "path": "/DirA",
                    "name": "DirB",
                    "type": "dir",
                    "content": [
                        {
                            "path": "/DirA/DirB",
                            "name": "dirC",
                            "type": "dir",
                            "content": [
                                {
                                    "path": "/DirA/DirB/dirC",
                                    "name": "dirD",
                                    "type": "dir",
                                    "content": [
                                        {
                                            "path": "/DirA/DirB/dirC/dirD",
                                            "name": "fileG",
                                            "type": "file",
                                        }
                                    ],
                                }
                            ],
                        }
                    ],
                },
                {
                    "path": "/DirA",
                    "name": "DirF",
                    "type": "dir",
                    "content": [
                        {
                            "path": "/DirA/DirF",
                            "name": "dirG",
                            "type": "dir",
                            "content": [
                                {
                                    "path": "/DirA/DirF/dirG",
                                    "name": "fileY",
                                    "type": "file",
                                }
                            ],
                        }
                    ],
                },
            ],
        }
    ],
}
result = cache.read_obj_from_cache()
assert result == expected_result
print("Test5: Cool? : {}".format(result == expected_result))
print(result)

print("Test6: get file from cache")
result = cache.read_obj_from_cache("/DirA/DirF/dirG/fileY")
expected_result = {"path": "/DirA/DirF/dirG", "name": "fileY", "type": "file"}
assert result == expected_result
print("Test6: Cool? : {}".format(result == expected_result))

print("Test7: is_path_fully_recursive_cached")
result = cache.is_path_fully_recursive_cached("/DirA/DirB/dirC/dirD")
expected_result = True
assert result == expected_result
print("Test7a: Cool? : {}".format(result == expected_result))


result = cache.is_path_fully_recursive_cached("/DirA/DirF/dirG/fileY")
expected_result = True
assert result == expected_result
print("Test7b: Cool? : {}".format(result == expected_result))


non_fully_cached_obj = {"path": "/DirA/DirF/dirG", "name": "dirX", "type": "dir"}
cache.write_obj_to_cache(non_fully_cached_obj)
result = cache.is_path_fully_recursive_cached("/DirA/DirF/dirG")
expected_result = False
assert result == expected_result
print("Test7c: Cool? : {}".format(result == expected_result))
"""
result = cache.is_path_fully_recursive_cached("/DirA/DirF/dirG/dirX")
expected_result = False
assert result == expected_result
print("Test7c: Cool? : {}".format(result == expected_result))

result = cache.is_path_fully_recursive_cached("/DirA/DirF/NonExistet")
expected_result = False
assert result == expected_result
print("Test7d: Cool? : {}".format(result == expected_result))

print("Test8: Overlaying insert")
test_cache_obj = {
    "path": "/DirA",
    "name": "DirB",
    "type": "dir",
    "content": [
        {"path": "/DirA/DirB", "name": "fileD", "type": "file"},
        {
            "path": "/DirA/DirB",
            "name": "dirC",
            "type": "dir",
            "content": [
                {"path": "/DirA/DirB/dirC", "name": "fileE", "type": "file"},
                {"path": "/DirA/DirB/dirC", "name": "fileP", "type": "file"},
            ],
        },
    ],
}

cache.write_obj_to_cache(new_cache_obj)
result = cache.read_obj_from_cache()
print("result1", result)
expected_result = {
    "path": "",
    "name": "",
    "type": "root",
    "content": [
        {
            "path": "/",
            "name": "DirA",
            "type": "dir",
            "content": [
                {
                    "path": "/DirA",
                    "name": "DirB",
                    "type": "dir",
                    "content": [
                        {
                            "path": "/DirA/DirB",
                            "name": "dirC",
                            "type": "dir",
                            "content": [
                                {
                                    "path": "/DirA/DirB/dirC",
                                    "name": "dirD",
                                    "type": "dir",
                                    "content": [
                                        {
                                            "path": "/DirA/DirB/dirC/dirD",
                                            "name": "fileG",
                                            "type": "file",
                                        }
                                    ],
                                },
                                {
                                    "path": "/DirA/DirB/dirC",
                                    "name": "dirD",
                                    "type": "dir",
                                    "content": [
                                        {
                                            "path": "/DirA/DirB/dirC/dirD",
                                            "name": "fileG",
                                            "type": "file",
                                        }
                                    ],
                                },
                            ],
                        }
                    ],
                },
                {
                    "path": "/DirA",
                    "name": "DirF",
                    "type": "dir",
                    "content": [
                        {
                            "path": "/DirA/DirF",
                            "name": "dirG",
                            "type": "dir",
                            "content": [
                                {
                                    "path": "/DirA/DirF/dirG",
                                    "name": "fileX",
                                    "type": "file",
                                },
                                {
                                    "path": "/DirA/DirF/dirG",
                                    "name": "fileX",
                                    "type": "file",
                                },
                            ],
                        }
                    ],
                },
            ],
        }
    ],
}

test = {
    "path": "",
    "name": "",
    "type": "root",
    "content": [
        {
            "path": "/",
            "name": "DirA",
            "type": "dir",
            "content": [
                {
                    "path": "/DirA",
                    "name": "DirB",
                    "type": "dir",
                    "content": [
                        {
                            "path": "/DirA/DirB",
                            "name": "dirC",
                            "type": "dir",
                            "content": [
                                {
                                    "path": "/DirA/DirB/dirC",
                                    "name": "dirD",
                                    "type": "dir",
                                    "content": [
                                        {
                                            "path": "/DirA/DirB/dirC/dirD",
                                            "name": "fileG",
                                            "type": "file",
                                        }
                                    ],
                                }
                            ],
                        }
                    ],
                },
                {
                    "path": "/DirA",
                    "name": "DirF",
                    "type": "dir",
                    "content": [
                        {
                            "path": "/DirA/DirF",
                            "name": "dirG",
                            "type": "dir",
                            "content": [
                                {
                                    "path": "/DirA/DirF/dirG",
                                    "name": "fileX",
                                    "type": "file",
                                },
                                {
                                    "path": "/DirA/DirF/dirG",
                                    "name": "fileX",
                                    "type": "file",
                                },
                            ],
                        }
                    ],
                },
            ],
        }
    ],
}


"""

print(cache.cache)
print(cache.get_flat_path_list())
