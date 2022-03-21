import os,  shutil
from distutils.dir_util import copy_tree
import numpy as np


path = "sample_data"
target_root = "sample_data_splits"
all_paths = []
for folder in os.listdir(path):
	folder_path = os.path.join(path, folder)
	all_paths.append(folder_path)


parts = np.split(np.array(all_paths), 5)

for i, folders in enumerate(parts):
	target_path = os.path.join(target_root, str(i))
	for folder in folders:
		# print(folder)
		folder_name = folder.split("/")[-1]
		target_folder_path = os.path.join(target_path, folder_name)
		copy_tree(folder, target_folder_path)


