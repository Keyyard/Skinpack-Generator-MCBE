from pathlib import Path
import json
import os
import shutil
import uuid

skinpack_name = input('Enter skinpack name: ')

# start counting time
if skinpack_name == '':
    print("Invalid skinpack name")
else:
    print("Creating skinpack " + skinpack_name)
    skinpack_name = skinpack_name.lower()
    skinpack_name = skinpack_name.replace(' ', '_')
    start_timer = os.times()

input_dir = Path(os.getcwd() + '/input')
if not input_dir.exists():
    print("Input directory doesn't exist, do you want to create it? (y/n)")
    answer = input()
    if answer == 'y':
        input_dir.mkdir()
        print("Please put skin files in input directory and retry")
        input("Enter any key to exit...")
        exit()
    else:
        print("Exiting...")
        exit()
else:
    input_files = [f for f in input_dir.iterdir() if f.suffix == '.png']
    output_dir = Path(os.getcwd() + '/output')
    if not output_dir.exists():
        output_dir.mkdir()

    for file in input_files:
        shutil.copy(file, output_dir)

    manifest = {}
    manifest['format_version'] = 2  
    manifest['header'] = {}
    manifest['header']['name'] = "pack.name"
    manifest['header']['uuid'] = str(uuid.uuid4())
    manifest['header']['version'] = [ 1, 0, 0 ]
    manifest['modules'] = [{'type': 'skin_pack', 'uuid': str(uuid.uuid4()), 'version': [ 1, 0, 0 ]}]
    manifest_file = Path(os.getcwd() + '/output/manifest.json')
    f = open(manifest_file, 'w')
    f.write(json.dumps(manifest, indent=2))
        
    
    skins = {}
    skins['skins'] = []
    for file in input_files:
        skins['skins'].append({'localization_name': 'skin_' + file.stem, 'texture': file.stem + '.png', 'type': 'paid', 'geometry': 'geometry.humanoid.customSlim'})
    
    skins['serialize_name'] = skinpack_name
    skins['localization_name'] = skinpack_name
    skins_file = Path(os.getcwd() + '/output/skins.json')
    f = open(skins_file, 'w')
    f.write(json.dumps(skins, indent=2))

    texts_dir = Path(os.getcwd() + '/output/texts')
    if not texts_dir.exists():
        texts_dir.mkdir()
    lang_file = Path(os.getcwd() + '/output/texts/en_US.lang')
    f = open(lang_file, 'a')
    skinpack_name_text = skinpack_name.replace('_',' ')
    skinpack_name_text = skinpack_name_text.capitalize()
    f.write('pack.name=' + skinpack_name_text + '\n\n')
    f.write('skinpack.' + skinpack_name + '=' + skinpack_name_text + '\n')
    for file in input_files:
        name_skin=file.stem
        name_skin=name_skin.replace("_alex", "")
        name_skin=name_skin.capitalize()
        f.write('skin.' + skinpack_name + '.' + 'skin_' + file.stem + '=' + name_skin + '\n')
    languages = ['en_US']
    languages_file = Path(os.getcwd() + '/output/texts/languages.json')
    f = open(languages_file, 'w')
    f.write(json.dumps(languages))

    print('\nSkinpack created!')
    print('Time elapsed: ' + str(os.times()[1] - start_timer[1]))
    input("Enter any key to exit...")
    exit()