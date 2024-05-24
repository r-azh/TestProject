import shutil, os
import time
#Creating Source, Destination and Archive paths.
source = r'test/source'
destination = r'test\destination'
archive = r'test\archive'

#Current time in seconds
current_time = time.time()

sub_files = []
#First os.walk for the source folder itself
for root, dirs, files in os.walk(source):
    for folder in dirs:
        subdir = root+'\\'+folder
        #second os.walk for each folder in the source folder (A, B, and C)
        for subroot, subdirs, subfiles in os.walk(subdir):
            for file in subfiles:
                filePath = subroot+'\\'+file

                #Gets the file descriptor and stores it in fileStat
                fileStat = os.stat(filePath)
                #st_ctime is the files creation time.
                #current time in seconds - file creation would be the difference
                #between the current time and the file creation time.
                #Divide by 60 to convert that to minutes.
                ######################################
                ##If time passed greater than 5 minutes, send to a matching folder in destination
                if ((current_time-fileStat.st_ctime)/60) > 5:
                    shutil.move(filePath, destination+'\\'+folder)
                else:
                    shutil.move(filePath, archive+'\\'+folder)
