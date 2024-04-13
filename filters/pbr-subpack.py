import os
import shutil
import sys
from pathlib import Path

if len(sys.argv)-1 < 2:
    print("Too few arguments")
    exit(1)

src = os.path.join(os.getcwd(), sys.argv[1])
dst = os.path.join(os.getcwd(), sys.argv[2])

print("Copying " + src + " to " + dst)

def copy_recursive(source_base_path, target_base_path):
    """
    Copy a directory tree from one location to another. This differs from shutil.copytree() that it does not
    require the target destination to not exist. This will copy the contents of one directory in to another
    existing directory without complaining.
    It will create directories if needed, but notify they already existed.
    If will overwrite files if they exist, but notify that they already existed.
    :param source_base_path: Directory
    :param target_base_path:
    :return: None
    """
    if not Path(source_base_path).is_dir() or not Path(target_base_path).is_dir():
        raise Exception("Source and destination directory and not both directories.\nSource: %s\nTarget: %s" % (
        source_base_path, target_base_path))
    for item in os.listdir(source_base_path):
        # Directory
        if os.path.isdir(os.path.join(source_base_path, item)):
            # Create destination directory if needed
            new_target_dir = os.path.join(target_base_path, item)
            try:
                os.mkdir(new_target_dir)
            except OSError:
                pass

            # Recurse
            new_source_dir = os.path.join(source_base_path, item)
            copy_recursive(new_source_dir, new_target_dir)
        # File
        else:
            # Copy file over
            source_name = os.path.join(source_base_path, item)
            target_name = os.path.join(target_base_path, item)
            if not Path(target_name).is_file():
                shutil.copy(source_name, target_name)

copy_recursive(src, dst)