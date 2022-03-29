import os,  shutil
# from distutils.dir_util import copy_tree
import numpy as np
import os, shutil
# def copytree(src, dst, symlinks=False, ignore=None):
#     for item in os.listdir(src):
#         s = os.path.join(src, item)
#         d = os.path.join(dst, item)
#         if os.path.isdir(s):
#             shutil.copytree(s, d, symlinks, ignore)
#         else:
#             shutil.copy2(s, d)


path = "dataset"
target_root = "dataset_splits"
all_paths = []
for folder in os.listdir(path):
	folder_path = os.path.join(path, folder)
	all_paths.append(folder_path)


parts = np.array_split(np.array(all_paths), 100)

# for p in parts:
# 	print(len
for i, folders in enumerate(parts):
	target_path = os.path.join(target_root, str(i))
	for f in folders:
		# print(folder)
		folder_name = f.split("/")[-1]
		target_folder_path = os.path.join(target_path, folder_name)
		print(f, target_folder_path)
		try:
			shutil.move(f, target_folder_path)
		except Exception as e:
			print(e)


