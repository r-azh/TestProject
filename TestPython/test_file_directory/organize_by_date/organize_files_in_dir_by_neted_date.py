import pprint
import re
import shutil
import os
from collections import defaultdict
from datetime import datetime

# source = r'test/source'
source = r'/Users/rez/Documents/'


def sort_files_by_date(files):
	files_by_date = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
	for full_path_file in files:
		# Gets the file descriptor and stores it in fileStat
		file_stat = os.stat(full_path_file)
		# st_ctime is the files creation time(if moved this will be the move time).
		# st_mtime is the files modified time.
		create_date = datetime.fromtimestamp(file_stat.st_mtime)
		year = create_date.strftime('%Y')
		month = create_date.strftime('%m')
		day = create_date.strftime('%d')
		files_by_date[year][month][day].append(full_path_file)
	return files_by_date


def move_files_to_dated_folders(folder, files_by_date):
	print("\t\t**********")
	for year in files_by_date:
		year_folder_name = os.path.join(folder, year)
		os.makedirs(year_folder_name, exist_ok=True)
		for month in files_by_date[year]:
			month_folder_name = os.path.join(year_folder_name, month)
			os.makedirs(month_folder_name, exist_ok=True)
			for day in files_by_date[year][month]:
				day_folder_name = os.path.join(month_folder_name, day)
				os.makedirs(day_folder_name, exist_ok=True)
				for f in files_by_date[year][month][day]:
					print(f"moving file from {f} to {day_folder_name}")
					shutil.move(f, day_folder_name)


sub_files = []
# First os.walk for the source folder itself
for root, dirs, files in os.walk(source):
	root_base_name = os.path.basename(root)
	full_path_files = [os.path.join(root, file) for file in files]
	print('='*50)
	print("root: ", root)
	print("root folder name: ", root_base_name)
	print("dirs:", dirs)
	print("files:")
	pprint.pprint(full_path_files)
	# if re.match(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', root_base_name):
	# 	print("Pass -> folder is already in date format: ", root_base_name)
	# 	continue
	if full_path_files:
		move_files_to_dated_folders(
			root,
			sort_files_by_date(full_path_files)
		)

