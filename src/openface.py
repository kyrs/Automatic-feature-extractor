"""
__name__ : kumar shubham 
__date__ : 29 JAN 2021
__desc__ : code for running openface algorithms over the images 
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

class OpenFaceProcessing:
	def __init__(self, inputDir, openFaceBin ):
		## intitializing the flags
		self.inputDir = inputDir
		self.openFaceBin = openFaceBin


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



	def extractOpenFaceFeature(self, inputVideo, outputFolder) : 
		assert(list(Path(inputVideo).parents) == list(Path(outputFolder).parents))
		cmd = "{0} -f {1}  -out_dir {2} -nosimalig ".format(self.openFaceBin, inputVideo, outputFolder)
		self.__callsubprocess(cmd)
		return True

	def RUN(self):
		fileList = glob.glob(join(self.inputDir, "*/*_trim.mp4"))
		assert(len(fileList)>0)

		for videoFile in tqdm(fileList):
			folderAdd = dirname(videoFile)
			videoFileName = basename(videoFile)
			baseVideoFileName = videoFileName.split(".")[0]
			baseVideoFolderName = join(folderAdd, baseVideoFileName+"_openface")

			if not isdir(baseVideoFolderName):
				mkdir(baseVideoFolderName)

			print(f"processing the file : {videoFile}")
			print(f"output dir for file : {baseVideoFolderName}")

			self.extractOpenFaceFeature(videoFile, baseVideoFolderName)


if __name__ == "__main__":
	obj = OpenFaceProcessing(inputDir = "/mnt/hdd1/shubham/UNIL_ROUND_2_EXP/data/processedOutputDir",  openFaceBin = "/mnt/hdd1/shubham/openface2/OpenFace/build/bin/FeatureExtraction" )
	obj.RUN()