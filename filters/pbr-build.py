import colorsys
import json
import shutil
import sys
import os
from PIL import Image
from pathlib import Path

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

def tweak_mer(folder_name):
    for root, dirs, files in os.walk(f'data/{folder_name}/mer'):
        for file in files:
            if(file.endswith('.png')):
                im = Image.open(root+'/'+file)
                im_rgb = im.convert('RGB')
                im_new = Image.new(mode='RGB', size=(im.size[0],im.size[1]))
                for i in range(im.size[0]):  # for every pixel:
                    for j in range(im.size[1]):
                        value = im_rgb.getpixel((i,j))
                        im_new.load()[i, j] = (
                            int(value[0]),
                            round(int(value[1])/17),
                            int(value[2])
                        )
                im_new.save(root+'/'+file)

def find_file(name, path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file == name:
                return root
    return None

def create_texture_set(file_name, root, folder_name):
    texture_set={
        'format_version': '1.16.100',
        'minecraft:texture_set': {
            'color': file_name
        }
    }

    for key, value in config['mer']['array'].items():
        if file_name in value:
            texture_set['minecraft:texture_set']['metalness_emissive_roughness'] = list(map(int, key.split('-')))

    for key, value in config['mer']['string'].items():
        if file_name in value:
            texture_set['minecraft:texture_set']['metalness_emissive_roughness'] = key
            path = find_file(key + '.png', f'data/{folder_name}/mer')
            shutil.copy(f'{path}/{key}.png', f'RP/subpacks/main/textures/{root[10+len(folder_name):]}/{key}.png')

    for key, value in config['heightmap'].items():
        if file_name in value:
            texture_set['minecraft:texture_set']['heightmap'] = key
            shutil.copy(f'data/{folder_name}/heightmap/{key}.png', f'RP/subpacks/{folder_name}/textures/{root[10+len(folder_name):]}/{key}.png')

    for key, value in config['normal'].items():
        if file_name in value:
            texture_set['minecraft:texture_set']['normal'] = key
            shutil.copy(f'data/{folder_name}/normal/{key}.png', f'RP/subpacks/{folder_name}/textures/{root[10+len(folder_name):]}/{key}.png')

    with open(f'RP/subpacks/{folder_name}/textures/{root[10+len(folder_name):]}/{file_name}.texture_set.json', 'w') as file:
        json.dump(texture_set, file, sort_keys=True, ensure_ascii=False, indent=4)

src = os.path.join(os.getcwd(), 'data/main/src')
dst = os.path.join(os.getcwd(), 'RP/subpacks/main/textures')
print('Copying ' + src + ' to ' + dst)
copy_recursive(src, dst)

src = os.path.join(os.getcwd(), 'data/update_1_21/src')
dst = os.path.join(os.getcwd(), 'RP/subpacks/update_1_21/textures')
print('Copying ' + src + ' to ' + dst)
copy_recursive(src, dst)

tweak_mer('main')
tweak_mer('update_1_21')

with open('data/update_1_21/config.json') as data:
    config = json.load(data)

for root, directories, files in os.walk('data/update_1_21/src'):
    for file in files:
        file_name = file[:-4]
        create_texture_set(file_name, root, 'update_1_21')

with open('data/main/config.json') as data:
    config = json.load(data)

for root, directories, files in os.walk('data/main/src'):
    for file in files:
        file_name = file[:-4]
        create_texture_set(file_name, root, 'main')