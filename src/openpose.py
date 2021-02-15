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
import json
import numpy as np
import cv2 
import pandas as pd


class OpenPoseProcessing:
	def __init__(self, inputDir,  openPoseDir, runOpenPoseFlag, runCsvFeatFlag):
		## intitializing the flags
		self.inputDir = inputDir
		self.openPoseDir = openPoseDir
		self.runOpenPoseFlag = runOpenPoseFlag
		self.runCsvFeatFlag = runCsvFeatFlag


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
		
		cmd = "{0} --video {1} --write_json {2} -write_video {3} --display 0   --hand  --face".format(binOpenPose, inpFilePth, imgSavePth, outFileOpenpose)
		self.__callsubprocess(cmd, cwd = self.openPoseDir)
		return True

	def extractAngleBasedFet(self, inputJsonFolder, outputFileSave):
		frameId = 0
		assert(list(Path(inputJsonFolder).parents) == list(Path(dirname(outputFileSave)).parents))
		jsonFileList = glob.glob(join(inputJsonFolder, "*_keypoints.json"))
		assert( len(jsonFileList) > 100 )
		angleInfoList = []
		for fileName in sorted(jsonFileList):
			frameId += 1 
			with open(fileName, "r") as fileNameReader:
				outJson = json.load(fileNameReader)
				keypointList = outJson['people'][0]['pose_keypoints_2d']  
			handAngle = self.angleHandGesture(valList = keypointList)
			out = {}
			out["id"] = frameId
			out["left_hand_angle"] = handAngle["left"]["angle"]
			out["left_hand_conf"] = handAngle["left"]["conf"]

			out["right_hand_angle"] = handAngle["right"]["angle"]
			out["right_hand_conf"] =  handAngle["right"]["conf"]

			angleInfoList.append(out)
		df = pd.DataFrame(angleInfoList)
		df.to_csv(outputFileSave, index = False, sep = ',')

	def angle(self, shoulder, elbow, hand):
		shoulder_elbow = np.array(shoulder) - np.array(elbow)
		hand_elbow = np.array(hand) - np.array(elbow)

		cosine_angle = np.dot(shoulder_elbow, hand_elbow) / (np.linalg.norm(shoulder_elbow) * np.linalg.norm(hand_elbow))
		angle = np.arccos(cosine_angle)
		
		return np.degrees(angle)

	def floatToInt(self,value):
		return tuple([int(i) for i in value ])


	def saveImage(self):
		matImg = 255 * np.ones((1000,2000,3), np.uint8)
		matImg = cv2.circle(matImg, self.floatToInt(leftShoulder), radius=3, color=(0, 0, 255), thickness=-1)
		matImg = cv2.circle(matImg, self.floatToInt(rightShoulder), radius=3, color=(0, 0, 255), thickness=-1)

		matImg = cv2.circle(matImg, self.floatToInt(rightElbow), radius=3, color=(0, 255, 0), thickness=-1)
		matImg = cv2.circle(matImg, self.floatToInt(rightElbow), radius=3, color=(0,255, 0), thickness=-1)

		matImg = cv2.circle(matImg, self.floatToInt(rightHand), radius=3, color=(255,0 , 0), thickness=-1)
		matImg = cv2.circle(matImg, self.floatToInt(leftElbow), radius=3, color=(0,255, 0), thickness=-1)
		matImg = cv2.circle(matImg, self.floatToInt(leftHand), radius=3, color=(255,0 , 0), thickness=-1)

		cv2.imwrite("img.jpg", matImg)
		input()


	def angleHandGesture(self, valList):
		# Result for BODY_25 (25 body parts consisting of COCO + foot){
   		#   {0,  "Nose"}, #   {1,  "Neck"},#   {2,  "RShoulder"}, #   {3,  "RElbow"},#   {4,  "RWrist"},#   {5,  "LShoulder"},
   		#   {6,  "LElbow"},#   {7,  "LWrist"},#   {8,  "MidHip"},
   		#   {9,  "RHip"}, #   {10, "RKnee"}, #  
   		# {11, "RAnkle"},  #   {12, "LHip"}, #   {13, "LKnee"},#   {14, "LAnkle"}, #   {15, "REye"},#   {16, "LEye"},#   {17, "REar"},
   		#   {18, "LEar"},#   {19, "LBigToe"},#   {20, "LSmallToe"},#   {21, "LHeel"},#   {22, "RBigToe"},#   {23, "RSmallToe"},#   {24, "RHeel"},#   {25, "Background"} ;

		keypointList = [valList[i:i+3] for i in range(0,75,3)]
		leftShoulderVal = keypointList[5]
		leftElbowVal = keypointList[6]
		leftHandVal = keypointList[7]

		leftShoulder = leftShoulderVal[:2]
		leftElbow = leftElbowVal[:2]
		leftHand = 	leftHandVal[:2]

		leftSideConf = [leftShoulderVal[2], leftElbowVal[2], leftHandVal[2]]
		leftMinConf = min(leftSideConf)

		rightShoulderVal = keypointList[2]
		rightElbowVal = keypointList[3]
		rightHandVal = keypointList[4]

		rightShoulder = rightShoulderVal[:2]
		rightElbow    = rightElbowVal[:2]
		rightHand 	  =  rightHandVal[:2]

		rightSideConf = [rightShoulderVal[2], rightElbowVal[2], rightHandVal[2]]
		rightMinConf = min(rightSideConf)
		
		
		leftHandAngle = self.angle(shoulder = leftShoulder, elbow = leftElbow, hand = leftHand)
		rightHandAngle = self.angle(shoulder = rightShoulder, elbow = rightElbow, hand = rightHand)

		return {"left":{"angle": leftHandAngle, "conf" : leftMinConf}, "right":{"angle": rightHandAngle, "conf" : rightMinConf}}


	def RUN(self):
		fileList = glob.glob(join(self.inputDir, "*/*_trim.mp4"))
		assert(len(fileList)>0)

		for videoFile in tqdm(fileList):
			folderAdd = dirname(videoFile)
			videoFileName = basename(videoFile)
			baseVideoFileName = videoFileName.split(".")[0]
			baseVideoFolderName = join(folderAdd, baseVideoFileName + "_openpose")
			videoOutFileOpenpose =  join(baseVideoFolderName, baseVideoFileName + "_openpose.avi")
			outputCsvFileSave = join(baseVideoFolderName, baseVideoFileName + "_opnepose_feature.csv")

			if not isdir(baseVideoFolderName):
				mkdir(baseVideoFolderName)

			print(f"processing the file : {videoFile}")
			print(f"output dir for file : {baseVideoFolderName}")

			if self.runOpenPoseFlag:
				print("openpose flag : ON")
				self.runOpenPose(videoFile, baseVideoFolderName, videoOutFileOpenpose)
			else:
				pass


			if self.runCsvFeatFlag:
				print("csv Feat Flag : ON")
				self.extractAngleBasedFet(inputJsonFolder = baseVideoFolderName,outputFileSave = outputCsvFileSave)

if __name__ =="__main__":
	obj = OpenPoseProcessing(inputDir = "/home/ubuntu/Automatic-feature-extractor/processed_video/set_test",  openPoseDir = "/home/ubuntu/soft/openpose/openpose", runOpenPoseFlag = True, runCsvFeatFlag = True)
	obj.RUN()