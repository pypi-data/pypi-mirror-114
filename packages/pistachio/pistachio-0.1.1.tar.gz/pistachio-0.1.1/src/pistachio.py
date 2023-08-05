from pathlib import Path


import errno
import hashlib
import os


def describe(path_str):
    """
    Method to describe the type of resources.
    """
    return {
        "path": path_str,
        "exists": exists(path_str),
        "is_directory": is_directory(path_str),
        "is_file": is_file(path_str),
        "is_symlink": is_symlink(path_str),
        "name": path_str.split("/")[-1]
    }


def exists(path_str):
    """
    Method to return True or False whether a resource exists.
    """
    return Path(path_str).exists()


def get_md5_hash(path_str):
    """
    Method to return the MD5 hash of a file.
    """
    if exists(path_str) is True and is_file(path_str) is True:
        md5_hash = hashlib.md5()
        with open(path_str, "rb") as fh:
            for block in iter(lambda: fh.read(4096), b""):
                md5_hash.update(block)
            fh.close()
        return md5_hash.hexdigest()
    else:
        return None


def is_directory(path_str):
    """
    Method to return True or False whether a resource is a directory.
    """
    return Path(path_str).is_dir()


def is_file(path_str):
    """
    Method to return True or False whether a resource is a file.
    """
    return Path(path_str).is_file()


def is_symlink(path_str):
    """
    Method to return True or False whether a resource is a symbolic link.
    """
    return Path(path_str).is_symlink()


def touch(path_str):
    """
    Method to generated an empty file.
    """
    if exists(path_str) is False:
        try:
            open(path_str, "a").close()
            return True
        except FileNotFoundError:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), path_str
            )
    else:
        return False


def tree(path_str):
    """
    Method to walk through a directory tree and discover all files
    and directories on the file system.
    """
    results_lst = []
    
    if exists(path_str) and is_directory(path_str):
        initial_path_str = os.getcwd()
        os.chdir(path_str)

        for root, directories, filenames in os.walk("."):
            for directory in directories:
                results_lst.append(
                    describe(f"""{root}/{directory}""")
                )
            for filename in filenames:
                results_lst.append(
                    describe(f"""{root}/{filename}""")
                )

        os.chdir(initial_path_str)

        return {
            "path": path_str,
            "results": sorted(results_lst, key=lambda d: d['path'])
        }
    else:
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), path_str
        )
