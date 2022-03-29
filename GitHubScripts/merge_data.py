import os,  shutil
from distutils.dir_util import copy_tree
import numpy as np
import shutil 

path = "dataset"
split_path = "dataset_splits"
all_paths = []
for folder in os.listdir(split_path):
	folder_path = os.path.join(split_path, folder)
	print(folder_path)
	for project_folder in os.listdir(folder_path):
		# print(project_folder)
		project_folder_path = os.path.join(folder_path, project_folder)
		try:
			shutil.move(project_folder_path, path)
		except Exception as e:
			print(e)

