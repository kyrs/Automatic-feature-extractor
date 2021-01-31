"""
__name__ : kumar shubham 
__date__ : 29 JAN 2021
__desc__ : code for running openpose algorithms over the images 
"""
from os import listdir, mkdir
from os.path import isfile, join, isdir, dirname, basename
import shutil 
from shutil import copyfile
import subprocess
from pathlib import Path
from tqdm import tqdm 
import sys 
import glob 


class OpenPoseProcessing:
	def __init__(self, inputDir,  openPoseDir):
		## intitializing the flags
		self.inputDir = inputDir
		self.openPoseDir = openPoseDir


	def __callsubprocess(self,cmd, cwd=None):
		try:
			if cwd is None:
				output = subprocess.check_output(cmd, shell=True,
                                     stderr=subprocess.STDOUT)
			else:
				output = subprocess.check_output(cmd, cwd=cwd, shell=True,
                                     stderr=subprocess.STDOUT)

		except subprocess.CalledProcessError as e:
			print ('Execution of "%s" failed!\n' % cmd)
			print (e.output)	
			sys.exit(1)



	def runOpenPose(self, inpFilePth, imgSavePth, outFileOpenpose):
		## runOpenPose for the input data
		assert(list(Path(inpFilePth).parents) == list(Path(imgSavePth).parents))

		binOpenPose =  "CUDA_VISIBLE_DEVICES=0 ./build/examples/openpose/openpose.bin"
		print(imgSavePth)
		cmd = "{0} --video {1} --write_json {2} -write_video {3} --display 0   --hand  --face".format(binOpenPose, inpFilePth, imgSavePth, outFileOpenpose)
		self.__callsubprocess(cmd, cwd = self.openPoseDir)
		return True

	def RUN(self):
		fileList = glob.glob(join(self.inputDir, "*/*_trim.mp4"))
		assert(len(fileList)>0)

		for videoFile in tqdm(fileList):
			folderAdd = dirname(videoFile)
			videoFileName = basename(videoFile)
			baseVideoFileName = videoFileName.split(".")[0]
			baseVideoFolderName = join(folderAdd, baseVideoFileName+"_openpose")
			videoOutFileOpenpose =  join(baseVideoFolderName, baseVideoFileName+"_openpose.avi")

			if not isdir(baseVideoFolderName):
				mkdir(baseVideoFolderName)

			print(f"processing the file : {videoFile}")
			print(f"output dir for file : {baseVideoFolderName}")

			self.runOpenPose(videoFile, baseVideoFolderName, videoOutFileOpenpose)

if __name__ =="__main__":
	obj = OpenPoseProcessing(inputDir = "/mnt/hdd1/shubham/UNIL_ROUND_2_EXP/data/processedOutputDir",  openPoseDir = "/mnt/hdd1/shubham/unil_swiss_access/openpose/openpose")
	obj.RUN()