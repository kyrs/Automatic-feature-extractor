"""
__author__ : kumar shubham
__date__ : 16 Feb 2021
"""
import argparse

from preprocess import MainFeatureExt
from speech_process import SpeechProcessing
from openpose import OpenPoseProcessing
from openface import OpenFaceProcessing

def parseInput():
	parser = argparse.ArgumentParser()

	parser.add_argument("--input_dir", type = str, default = "")
	parser.add_argument("--processed_dir", type = str, default = "")
	parser.add_argument("--csvFile", type = str, default = "")

	parser.add_argument("--FolderProcessFlag", type = bool, default = True)
	parser.add_argument("--SpeechProcessFlag", type = bool, default = True)
	parser.add_argument("--OpenPoseProcessFlag", type = bool, default = True)
	parser.add_argument("--OpenFaceProcessFlag", type = bool, default = True)

	output = parser.parse_args()
	assert(output.input_dir != output.processed_dir)

	print(f"input dir : {output.input_dir}")
	print(f"output dir : {output.processed_dir}")
	## folder process argument
	
	if output.FolderProcessFlag:
		print("RUNNING FFOLDER FILE...")
		FoldObj = MainFeatureExt(foldBfProcess = output.input_dir.strip(), foldAftProcess = output.processed_dir,
		 trimdetailCSV = "/home/ubuntu/Automatic-feature-extractor/library/allVideosInfo.csv", copyFlag = True, trimFlag = True, wavExtFlag = True,  
		 videoFormatFlag = True, videoFormat = "mp4")
		FoldObj.RUN()

	else:
		pass


	if output.SpeechProcessFlag:
		print("RUNNING  SPEECH FILE...")
		speechObj = SpeechProcessing(inputDir = output.processed_dir, openSmileFlag = True, praatFeatureFlag = True, 
		praatBin = "/home/ubuntu/soft/praat/praat/praat", praatEec = "/home/ubuntu/Automatic-feature-extractor/library/speechRateV3.praat", opensmileBin = "/home/ubuntu/soft/opensmile/opensmile-2.3.0/SMILExtract",
		 openSmileOSMExec = "/home/ubuntu/soft/opensmile/opensmile-2.3.0/config/prosodyShs.conf", openSmileEneExc = "/home/ubuntu/soft/opensmile/opensmile-2.3.0/config/demo/demo1_energy.conf")

		speechObj.RUN()
	else:
		pass


	if output.OpenFaceProcessFlag:
		print("RUNNING OPENFACE...")
		faceObj = OpenFaceProcessing(inputDir = output.processed_dir,  openFaceBin = "/home/ubuntu/soft/openface/OpenFace/build/bin/FeatureExtraction" )
		faceObj.RUN()
	else:
		pass

	if output.OpenPoseProcessFlag:
		print("RUNNING OPENPOSE...")
		poseObj = OpenPoseProcessing(inputDir = output.processed_dir,  openPoseDir = "/home/ubuntu/soft/openpose/openpose", runOpenPoseFlag = True, runCsvFeatFlag = True)
		poseObj.RUN()

if __name__ == "__main__":
	parseInput()
	#python main.py --input_dir /home/ubuntu/Automatic-feature-extractor/base_video/unil_dataset/session1/set1/  --processed_dir /home/ubuntu/Automatic-feature-extractor/processed_video/session1/set1 