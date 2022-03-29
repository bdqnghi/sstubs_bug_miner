from git import Repo
from git import RemoteProgress
import json
import os
import concurrent.futures
import csv

class CloneProgress(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        if message:
            print(message)

def git_clone(project_url, repo_folder):
	if not os.path.isdir(repo_folder):
		Repo.clone_from(project_url, repo_folder, progress=CloneProgress(), branch="master", no_single_branch=True)
		print(f"[Process ID]:{os.getpid()} Cloning..")

if __name__ == '__main__':
	path = "../topProjects.csv"
	limit = 10000

	all_projects = []
	all_folders = []
	with open(path, newline='') as csvfile:
		top_project_reader = csv.reader(csvfile, delimiter=',')
		next(top_project_reader, None)  # skip the headers
		for row in top_project_reader:
			if len(row) > 0:
				url_split = row[0].split("/")
				project_path = f"https://:@github.com/{url_split[-2]}/{url_split[-1]}"
				project_name = f"{url_split[-2]}.{url_split[-1]}"
				repo_folder = "dataset/" + project_name
				
				if len(all_projects) < limit:
					all_projects.append(project_path)
					all_folders.append(repo_folder)
	
	print(len(all_projects))
	print(len(all_folders))
	with concurrent.futures.ProcessPoolExecutor(40) as exe:
		exe.map(git_clone, all_projects, all_folders)