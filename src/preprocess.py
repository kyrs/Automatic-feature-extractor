"""
__author__ : kumar shubham
__desc__ : main preprocess file 
__Date__ : 24 Jan 2021
"""
from os import listdir, mkdir
from os.path import isfile, join, isdir
import shutil 
from shutil import copyfile
import subprocess
from pathlib import Path
from tqdm import tqdm 
import sys 
import pandas as pd 
import glob
import os

class MainFeatureExt:
	def __init__(self, foldBfProcess,foldAftProcess, trimdetailCSV, copyFlag = True, trimFlag = True, wavExtFlag = True,  videoFormatFlag = True, videoFormat = "mp4" ):
		self.foldBfProcess = foldBfProcess
		self.foldAftProcess = foldAftProcess
		self.trimFileFlag = trimFlag
		self.trimdetailCSV = trimdetailCSV
		self.videoFormat = videoFormat
		self.copyFlag = copyFlag
		self.trimFlag  = trimFlag
		self.wavExtFlag = wavExtFlag
		self.videoFormatFlag = videoFormatFlag
		self.defVideoExt = videoFormat
		self.copyFromExt = ["mkl", "vlc", "mts" ]

		self.trimDataJson = self.__parseTrimCsv(trimdetailCSV)



	def createFolAndCopy(self, listInpFile):
		## code to create folder to save the processed File
		outputList = []

		for datInfo in tqdm(listInpFile):
			orgName = datInfo["org"]
			file  = datInfo["file"]
			ext = datInfo["ext"]
			inpFilePath = datInfo["inpFullPath"]
			newFoldPath = join(self.foldAftProcess, file)

			## check no folder like that exist##########
			# assert(not isdir(newFoldPath))


			###########################################
			print(f"FileName : {file}")
			print(f"Ext : {ext}" )
			print(f"Input Path : {inpFilePath}")
			print(f"New path : {newFoldPath}")
			print("===================")
			
			if not(isdir(newFoldPath)):
				mkdir(newFoldPath)
			else:
				pass

			
			savFileName = join(newFoldPath,orgName)

			# print(savFileName)
			# input()
			if not isfile(savFileName):
				print(inpFilePath)
				copyfile(inpFilePath, savFileName)
			else:
				pass

			outDict = {}
			outDict["file"] = file
			outDict["ext"] = ext
			outDict["inpfilePth"] = inpFilePath
			outDict["savFoldPth"] = newFoldPath
			outDict["org"] = orgName
			outputList.append(outDict)

		return outputList


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


	def changeVideoFormat(self, inpFilePth, outFilePth):
		## changeVideoFormat
		assert(list(Path(inpFilePth).parents) == list(Path(outFilePth).parents))
		cmd = "ffmpeg -i {0}  {1}".format(inpFilePth,outFilePth)
		if not (isfile(outFilePth)):
			self.__callsubprocess(cmd)
		else:
			pass
		return True


	def trimVideo(self, inputVideoPath, outVideoPath, startTime, endTime):
		## code for trimming the video 
		assert(list(Path(inputVideoPath).parents) == list(Path(outVideoPath).parents))
		cmd = "ffmpeg -i {0} -ss {1} -to {2}  {3}".format(inputVideoPath, startTime, endTime, outVideoPath)

		if not (isfile(outVideoPath)):
			self.__callsubprocess(cmd)
		else:
			pass
		return True


	def __parseTrimCsv(self, baseFileName):
		### Yet to be implemented !! 
		df = pd.read_csv(baseFileName)
		dictOut = {}

		for ind in df.index:

			key       = df["video_name"][ind]
			startTime = df["Start_time"][ind]
			endTime   = df["End_time"][ind]

			if key not in dictOut:
				dictOut[key] = {"start_time" : startTime, "end_time" : endTime}
			else:
				raise Exception("Duplicate Keys in CSV.")
		return dictOut
		

	def readCsvTrim(self, videoName):

		assert(self.trimDataJson is not None)
		startTime = self.trimDataJson[videoName]["start_time"]
		endTime = self.trimDataJson[videoName]["end_time"]

		return startTime,endTime

		


	def wavConverter(self, fileAdd, saveFileAdd):
		print(fileAdd)
		print(saveFileAdd)
		assert(list(Path(fileAdd).parents) == list(Path(saveFileAdd).parents))
		cmd = "ffmpeg -i {0} -ac 2 -f wav {1}".format(fileAdd, saveFileAdd)

		if not (isfile(saveFileAdd)):
			self.__callsubprocess(cmd)
		else:
			pass

	def RUN(self):

		assert(len(listdir(self.foldBfProcess))>0)

		

		if self.copyFlag:
			listInpFile = []
			for fileName in listdir(self.foldBfProcess):
				file,ext =  fileName.split(".")
				listInpFile.append({"org": fileName,"file": file, "ext": ext, "inpFullPath": join(self.foldBfProcess, fileName)})

			print(f"Total Files : {len(listInpFile)}")
			print("Starting Data Copy...")
			########## creating folders and copy the file ###############
			dirInfo = self.createFolAndCopy(listInpFile)
		else:
			dirInfo = []

			for r, dirName, fileList in os.walk(self.foldAftProcess):
				for fileName in fileList:
					file,ext =  fileName.split(".")
					dirInfo.append({"org": fileName,"file": file, "ext": ext, "savFoldPth": dirName})

		## converting the files in the defined ext
		if self.videoFormatFlag:
			print("starting video fomrmatting flag....")

			for elm in tqdm(dirInfo):
				orginalName = elm["org"]
				newFoldPath = elm["savFoldPth"]
				file = elm["file"]
				ext = elm["ext"]

				if ext.lower() in self.copyFromExt:
					pass
				else:
					continue

				outFilePth = join(newFoldPath,file + "." + self.defVideoExt)
				inpfilePth = join(newFoldPath,orginalName)

				
				print(f"input file format : {inpfilePth}")
				print(f"output file format : {outFilePth}")
				print("changing format")
				if ext.lower() != self.defVideoExt:
					out = self.changeVideoFormat(inpfilePth, outFilePth )
				else:
					outFilePth = inpFilePath
					print(f"file with defined ext : {inpFilePath}")


		if self.trimFlag:
			print("Trimming the file...")
			pathForMp4 = glob.glob(join(self.foldAftProcess, "*/*.mp4"))
			assert(len(pathForMp4) > 0)

			for mp4fileAdd in tqdm(pathForMp4):
				splitFile  = mp4fileAdd.split("/")
				baseAdd = "/".join(splitFile[:-1])
				fileName = splitFile[-1]
				baseName = fileName.split(".")[0]
				ext = fileName.split(".")[1]
				# print(baseAdd)
				trimfileToSave = join(baseAdd, baseName+"_trim.mp4")
				print (f"mp4 file name : {mp4fileAdd}")
				print (f"ext file name : {ext}")
				print(f"baseName  : {baseName}")
				print(f"trim file to save : {trimfileToSave}")

				startTime, endTime = self.readCsvTrim(baseName)

				### trimming the files for further processing 
				self.trimVideo(inputVideoPath = mp4fileAdd, outVideoPath = trimfileToSave, startTime = startTime, endTime = endTime)



		if self.wavExtFlag:
			## make sure that trimming has been performed before hand  <Note : function can be modified based on specific requirements>
			pathofTrimMp4 = glob.glob(join(self.foldAftProcess, "*/*_trim.mp4"))
			assert(len(pathofTrimMp4) > 0)
			print("exptracting wav file...")
			for mp4fileAdd in tqdm(pathofTrimMp4):
				splitFile  = mp4fileAdd.split("/")
				baseAdd = "/".join(splitFile[:-1])
				fileName = splitFile[-1]
				baseName = fileName.split(".")[0]
				ext = fileName.split(".")[1]

				trimfileToSave = join(baseAdd, baseName+".wav")

				print (f"mp4 file name : {mp4fileAdd}")
				print (f"ext file name : {ext}")
				print(f"baseName  : {baseName}")
				print(f"trim file to save : {trimfileToSave}")
				self.wavConverter(fileAdd = mp4fileAdd, saveFileAdd = trimfileToSave)

if __name__ == "__main__":
	obj = MainFeatureExt(foldBfProcess = "/home/ubuntu/Automatic-feature-extractor/base_video/set_test", foldAftProcess = "/home/ubuntu/Automatic-feature-extractor/processed_video/set_test",
	 trimdetailCSV = "/home/ubuntu/Automatic-feature-extractor/library/testFile.csv", copyFlag = True, trimFlag = True, wavExtFlag = True,  
	 videoFormatFlag = True, videoFormat = "mp4")

	obj.RUN()