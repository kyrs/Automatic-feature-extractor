"""
__author__ : kumar shubham
__date__   : 26 Jan 2021
__desc__   : code to processspeech files 
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
import pandas as pd

class SpeechProcessing:
	def __init__(self, inputDir, openSmileFlag, praatFeatureFlag, praatBin, praatEec, opensmileBin, openSmileOSMExec, openSmileEneExc):
		self.inputDir = inputDir
		self.openSmileFlag = openSmileFlag
		self.praatFeatureFlag = praatFeatureFlag
		
		self.praatBin = praatBin
		self.praatEec = praatEec

		self.opensmileBin = opensmileBin
		
		self.openSmileOSMExec = openSmileOSMExec
		self.openSmileEneExc = openSmileEneExc

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

	def extractPraatFeature(self, inputWavFile, outputTxtFile) : 
		assert(list(Path(inputWavFile).parents) == list(Path(outputTxtFile).parents))

		cmd = "{0} --run {1} -25 2 0.3 1 {2} > {3}".format(self.praatBin, self.praatEec, dirname(inputWavFile), outputTxtFile)

		if not (isfile(outputTxtFile)):
			self.__callsubprocess(cmd)
		else:
			pass
		return True

	def extractOpenSmileFeature(self, inputWavFile, openSmileOSMFile, openSmileEnergFile):
		assert(list(Path(inputWavFile).parents) == list(Path(openSmileOSMFile).parents))
		assert(list(Path(inputWavFile).parents) == list(Path(openSmileEnergFile).parents))	

		cmd1 = "{0}  -C {1} -I {2}  -csvoutput  {3}".format(self.opensmileBin, self.openSmileOSMExec, inputWavFile, openSmileOSMFile )
		cmd2 = "{0}  -C {1} -I {2}  -O  {3}".format(self.opensmileBin, self.openSmileEneExc , inputWavFile, openSmileEnergFile)

		if not (isfile(openSmileOSMFile)):
			self.__callsubprocess(cmd1)
		else:
			pass



		if not (isfile(openSmileEnergFile)):
			self.__callsubprocess(cmd2)
		else:
			pass
		return True
		


	def RUN(self):

		fileList = glob.glob(join(self.inputDir, "*/*_trim.wav"))
		assert(len(fileList)>0)

		for speechFile in tqdm(fileList):			
			folderAdd = dirname(speechFile)
			wavFileName = basename(speechFile)
			baseWavFileName = wavFileName.split(".")[0]

			praatFeatureFile = join(folderAdd,baseWavFileName+"_PR.txt")
			openSmileOSMFile = join(folderAdd,baseWavFileName+"_OSM.csv")
			openSmileEnergFile = join(folderAdd,baseWavFileName+"_OSM_Ener.csv") 

			print(f"base wav file : {baseWavFileName}")
			
			if self.praatFeatureFlag:
				print(f"praatFeatureFile : {praatFeatureFile}")
				status = self.extractPraatFeature(speechFile, praatFeatureFile) 
			else:
				pass

			if self.openSmileFlag:
				print(f"opensmileFeatureFile : {openSmileOSMFile}")
				print(f"opensmileFeatureFile : {openSmileEnergFile}")
				self.extractOpenSmileFeature(speechFile, openSmileOSMFile, openSmileEnergFile)
				
			else:
				pass

if __name__ =="__main__":
	obj = SpeechProcessing(inputDir = "/mnt/hdd1/shubham/UNIL_ROUND_2_EXP/data/processedOutputDir", openSmileFlag = True, praatFeatureFlag = True, 
		praatBin = "/mnt/hdd1/shubham/UNIL_ROUND_2_EXP/soft/praat/praat", praatEec = "/mnt/hdd1/shubham/UNIL_ROUND_2_EXP/library/speechRateV3.praat", opensmileBin = "/mnt/hdd1/shubham/UNIL_ROUND_2_EXP/soft/opensmile-2.3.0/SMILExtract",
		 openSmileOSMExec = "/mnt/hdd1/shubham/UNIL_ROUND_2_EXP/soft/opensmile-2.3.0/config/prosodyShs.conf", openSmileEneExc = "/mnt/hdd1/shubham/UNIL_ROUND_2_EXP/soft/opensmile-2.3.0/config/demo/demo1_energy.conf")

	obj.RUN()