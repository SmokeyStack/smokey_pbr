import colorsys
import json
import shutil
import sys
import os
from PIL import Image
from pathlib import Path

for root, dirs, files in os.walk('data/main/mer'):
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

for root, dirs, files in os.walk('data/update_1_21/mer'):
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

def make_directories(source_base_path, target_base_path):
    '''
    Copy a directory tree from one location to another. This differs from shutil.copytree() that it does not
    require the target destination to not exist. This will copy the contents of one directory in to another
    existing directory without complaining.
    It will create directories if needed, but notify they already existed.
    If will overwrite files if they exist, but notify that they already existed.
    :param source_base_path: Directory
    :param target_base_path:
    :return: None
    '''
    if not Path(source_base_path).is_dir() or not Path(target_base_path).is_dir():
        raise Exception('Source and destination directory and not both directories.\nSource: %s\nTarget: %s' % (
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
            make_directories(new_source_dir, new_target_dir)

def find_file(name, path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file == name:
                return root
    return None

src = os.path.join(os.getcwd(), 'data/main/src')
dst = os.path.join(os.getcwd(), 'RP/subpacks/main/textures')
print('Copying ' + src + ' to ' + dst)
make_directories(src, dst)

src = os.path.join(os.getcwd(), 'data/update_1_21/src')
dst = os.path.join(os.getcwd(), 'RP/subpacks/update_1_21/textures')
print('Copying ' + src + ' to ' + dst)
make_directories(src, dst)

with open('data/update_1_21/config.json') as json_data:
    config = json.load(json_data)

for root, dirs, files in os.walk('data/update_1_21/src'):
    for file in files:
        json_data ={}
        json_data['format_version'] = '1.16.100'
        json_data['minecraft:texture_set'] = {}
        name = file[:-4]
        json_data['minecraft:texture_set']['color'] = name
        for attribute, value in config['mer']['array'].items():
            for element in config['mer']['array'][attribute]:
                if element == name:
                    json_data['minecraft:texture_set']['metalness_emissive_roughness'] = list(map(int, attribute.split('-')))
        for attribute, value in config['mer']['string'].items():
            for element in config['mer']['string'][attribute]:
                if element == name:
                    json_data['minecraft:texture_set']['metalness_emissive_roughness'] = attribute
                    shutil.copy('data/update_1_21/mer/'+root[21:] + '/' + attribute+'.png', 'RP/subpacks/update_1_21/textures/'+ root[21:] + '/' + attribute + '.png')
        for attribute, value in config['heightmap'].items():
            for element in config['heightmap'][attribute]:
                if element == name:
                    json_data['minecraft:texture_set']['heightmap'] = attribute
                    shutil.copy('data/update_1_21/heightmap/'+attribute+'.png', 'RP/subpacks/update_1_21/textures/'+ root[21:] + '/' + attribute + '.png')
        with open('RP/subpacks/update_1_21/textures/'+ root[21:] + '/' + name + '.texture_set.json', 'w') as fh:
            json.dump(json_data, fh, sort_keys=True, ensure_ascii=False, indent=4)

def create_texture_set(file_name, root):
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
            path = find_file(key + '.png', 'data/main/mer')
            shutil.copy(f'{path}/{key}.png', f'RP/subpacks/main/textures/{root[14:]}/{key}.png')

    for key, value in config['heightmap'].items():
        if file_name in value:
            texture_set['minecraft:texture_set']['heightmap'] = key
            shutil.copy(f'data/main/heightmap/{key}.png', f'RP/subpacks/main/textures/{root[14:]}/{key}.png')

    with open(f'RP/subpacks/main/textures/{root[14:]}/{file_name}.texture_set.json', 'w') as file:
        json.dump(texture_set, file, sort_keys=True, ensure_ascii=False, indent=4)

with open('data/main/config.json') as data:
    config = json.load(data)

for root, directories, files in os.walk('data/main/src'):
    for file in files:
        file_name = file[:-4]
        create_texture_set(file_name, root)