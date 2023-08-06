import pandas as pd
import os, glob
from datetime import datetime

DATA_FOLDER = '/Volumes/GoogleDrive/My Drive/GitHub/SimBA_troubleshooting/drop_bps/data'
FILE_FORMAT = 'csv'
POSE_TOOL = 'DLC'
NO_BP_TO_DROP = 2

files_found = glob.glob(DATA_FOLDER + '/*.' + FILE_FORMAT)
if FILE_FORMAT == 'h5':
    first_df = pd.read_hdf(files_found[0])
if FILE_FORMAT == 'csv':
    first_df = pd.read_csv(files_found[0], header=[0,1,2])
header_list = list(first_df.columns)[1:]

if 'individual' in list(first_df.columns)[0]:
    DLC_VERSION = 'maDLC'
else:
    DLC_VERSION = 'DLC'
body_part_names, animal_names = [], []

if DLC_VERSION == 'DLC':
    for header_entry in header_list:
        if header_entry[1] not in body_part_names:
            body_part_names.append(header_entry[1])

if DLC_VERSION == 'maDLC':
    for header_entry in header_list:
        if header_entry[1] not in body_part_names:
            animal_names.append(header_entry[1])
            body_part_names.append(header_entry[2])


TO_REMOVE = [('', 'Tail_end_1'), ('', 'Tail_end_2')]


date_time = datetime.now().strftime('%Y%m%d%H%M%S')
new_folder_name = 'Reorganized_bp_' + str(date_time)
new_directory = os.path.join(DATA_FOLDER, new_folder_name)
if not os.path.exists(new_directory):
    os.makedirs(new_directory)
print('Saving new pose-estimation files in ' + str(os.path.basename(new_directory)) + '...')

found_files = glob.glob(DATA_FOLDER + '/*.' + FILE_FORMAT)
if POSE_TOOL == 'DLC':
    for file in files_found:
        if FILE_FORMAT == 'csv':
            df = pd.read_csv(file, header=[0,1,2], index_col=0)
        if FILE_FORMAT == 'H5':
            df = pd.h5(file)
        for body_part in TO_REMOVE:
            if DLC_VERSION == 'DLC':
                df = df.drop(body_part[1], axis=1, level=1)
            if DLC_VERSION == 'maDLC':
                df = df.drop(body_part[2], axis=1, level=1)
        save_path = os.path.join(new_directory, os.path.basename(file))
        if FILE_FORMAT == 'csv':
            df.to_csv(save_path)
        if FILE_FORMAT == 'H5':
            df.to_hdf(save_path, key='re-organized', format='table', mode='w')
        print('Saved ' + str(os.path.basename(file)) + '...')
    print('All data with dropped body-parts saved in ' + new_directory)








