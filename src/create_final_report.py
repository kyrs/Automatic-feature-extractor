"""
__name__ : kumar shubham 
__date__ : 29 JAN 2021
__desc__ : code for running final reprt over the images 
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
import pandas as pd


class createFinalReport:

	def __init__(self, processedDir, saveFile, processSpeechFlag, processOpenFaceFlag, processOpenPoseFlag, varFlag ):
		## flags for processing

		self.processedDir = processedDir
		self.saveFile = saveFile
		self.processSpeechFlag = processSpeechFlag 
		self.processOpenPoseFlag = processOpenPoseFlag
		self.processOpenFaceFlag = processOpenFaceFlag

		self.varFlag = varFlag


	def RUN(self):

		## creating a single CSV file

		allFeatureList = []
		
		for folder in  tqdm(glob.glob(join(self.processedDir, "*"))):

			if isdir(folder):
				pass
			else:
				continue

			featureInfoDetails = {}
			featureInfoDetails["id"] = basename(folder)

			if self.processSpeechFlag:

				praatFeatureFile = glob.glob(join(folder, "*_PR.txt"))[0]
				energFeatureFile = glob.glob(join(folder, "*_OSM_Ener.csv"))[0]
				osmFeatureFile = glob.glob(join(folder, "*_OSM.csv"))[0]

				assert(isfile(praatFeatureFile))
				assert(isfile(energFeatureFile))
				assert(isfile(osmFeatureFile))

				print(folder)
				print(praatFeatureFile)
				assert(list(Path(join(folder,"*")).parents) == list(Path(praatFeatureFile).parents))
				assert(list(Path(join(folder,"*")).parents) == list(Path(energFeatureFile).parents))
				assert(list(Path(join(folder,"*")).parents) == list(Path(osmFeatureFile).parents))

				## processing PraatFile
				dfPaart = pd.read_csv(praatFeatureFile)
				dfPaart = dfPaart.set_index('soundname')
				speechRow = praatFeatureFile.split("/")[-1].split("_PR.txt")[0]
				articulationRate = dfPaart.loc[speechRow,' articulation rate (nsyll / phonationtime)']
				timeSpoken = dfPaart.loc[speechRow,' phonationtime (s)']
				totalTime = dfPaart.loc[speechRow,' dur (s)']
				speakingRate = dfPaart.loc[speechRow,' speechrate (nsyll/dur)']
				featureInfoDetails["spoken_time"]=timeSpoken
				featureInfoDetails["articulation_rate"]=articulationRate
				featureInfoDetails["speaking_rate"]=speakingRate
				featureInfoDetails["total_time"]=totalTime



				## processing OSM files 
				dfOSM= 	pd.read_csv(osmFeatureFile, sep = ";")
				dfEnergy = 	pd.read_csv(energFeatureFile, sep = ";")
				featureInfoDetails["mean_pitch"] = dfOSM["F0final_sma"].mean()
				featureInfoDetails["mean_loudness"] = dfOSM["pcm_loudness_sma"].mean()
				featureInfoDetails["mean_energy"] = dfEnergy["pcm_LOGenergy"].mean()

				if self.varFlag:
					featureInfoDetails["var_pitch"] = dfOSM["F0final_sma"].var()
					featureInfoDetails["var_loudness"] = dfOSM["pcm_loudness_sma"].var()
					featureInfoDetails["var_energy"] = dfEnergy["pcm_LOGenergy"].var()

			if self.processOpenFaceFlag:
				openFaceFeatureFile = glob.glob(join(folder, "*_openface/*.csv"))[0]
				assert(isfile(openFaceFeatureFile))
				assert(list(Path(join(folder,"*")).parents) == list(Path(dirname(openFaceFeatureFile)).parents))
				dfOpenFace = pd.read_csv(openFaceFeatureFile)
				
				featureInfoDetails["head_rotation_x_mean"] = dfOpenFace["pose_Rx"].mean()
				featureInfoDetails["head_rotation_y_mean"] = dfOpenFace["pose_Ry"].mean()
				featureInfoDetails["head_rotation_z_mean"] = dfOpenFace["pose_Rz"].mean()
				featureInfoDetails["gaze_angle_x_mean"] = dfOpenFace["gaze_angle_x"].mean()
				featureInfoDetails["gaze_angle_y_mean"] = dfOpenFace["gaze_angle_y"].mean()

				if self.varFlag:
					featureInfoDetails["head_rotation_x_var"] = dfOpenFace["pose_Rx"].var()
					featureInfoDetails["head_rotation_y_var"] = dfOpenFace["pose_Ry"].var()
					featureInfoDetails["head_rotation_z_var"] = dfOpenFace["pose_Rz"].var()
					featureInfoDetails["gaze_angle_x_var"] = dfOpenFace["gaze_angle_x"].var()
					featureInfoDetails["gaze_angle_y_var"] = dfOpenFace["gaze_angle_y"].var()


					
			if self.processOpenPoseFlag:
				print(join(folder, "*_openpose/*_openpose_feature.csv"))
				openposeFeatureFile = glob.glob(join(folder, "*_openpose/*.csv"))[0]
				assert(isfile(openposeFeatureFile))
				assert(list(Path(join(folder,"*")).parents) == list(Path(dirname(openposeFeatureFile)).parents))
				dfOpenPose = pd.read_csv(openposeFeatureFile)

				featureInfoDetails["left_hand_motion_angle_mean"] = dfOpenPose["left_hand_angle"].mean()
				featureInfoDetails["right_hand_motion_angle_mean"] = dfOpenPose["right_hand_angle"].mean()
				

				if self.varFlag:
					featureInfoDetails["left_hand_motion_angle_var"] = dfOpenPose["left_hand_angle"].var()
					featureInfoDetails["right_hand_motion_angle_var"] = dfOpenPose["right_hand_angle"].var()
			
			allFeatureList.append(featureInfoDetails)

		## column formatting for the dataframe		
		 
		columnListToSave = ["id"]

		if self.processSpeechFlag:
			columnListToSave += ["total_time", "speaking_rate", "articulation_rate","spoken_time","mean_pitch", "mean_loudness", "mean_energy"]
			if self.varFlag: 
				columnListToSave += ["var_pitch", "var_loudness", "var_energy"]


		if self.processOpenFaceFlag:
			columnListToSave += ["head_rotation_x_mean", "head_rotation_y_mean", "head_rotation_z_mean", "gaze_angle_x_mean", "gaze_angle_y_mean"]
			if self.varFlag: 
				columnListToSave += ["head_rotation_x_var", "head_rotation_y_var", "head_rotation_z_var", "gaze_angle_x_var", "gaze_angle_y_var"]


		if self.processOpenPoseFlag :
			columnListToSave += ["left_hand_motion_angle_mean", "right_hand_motion_angle_mean"]
			if self.varFlag: 
				columnListToSave += ["left_hand_motion_angle_var", "right_hand_motion_angle_var"]

		# print(featureInfoDetails)
		dfToSave =  pd.DataFrame(allFeatureList, columns = columnListToSave)
		dfToSave.to_csv(self.saveFile, index = False)


if __name__ == "__main__":
	obj = createFinalReport(processedDir = "/home/ubuntu/Automatic-feature-extractor/processed_video/set_test", saveFile = "/home/ubuntu/Automatic-feature-extractor/results/report_part1.csv",
	 processSpeechFlag = True, processOpenFaceFlag = True, processOpenPoseFlag = True, varFlag = True)
	obj.RUN()