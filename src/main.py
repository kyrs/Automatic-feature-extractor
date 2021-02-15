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

	parser.add_argument("--FolderProcessFlag", type = bool, default = False)
	parser.add_argument("--SpeechProcessFlag", type = bool, default = False)
	parser.add_argument("--OpenPoseProcessFlag", type = bool, default = False)
	parser.add_argument("--OpenFaceProcessFlag", type = bool, default = False)

	output = parser.parse_args()
	assert(output.input_dir != output.processed_dir)

	print(f"input dir : {output.input_dir}")
	print(f"output dir : {output.processed_dir}")
	## folder process argument
	
	if output.FolderProcessFlag:
		print("RUNNING FFOLDER FILE...")
		FoldObj = MainFeatureExt(foldBfProcess = output.input_dir, foldAftProcess = output.processed_dir,
		 trimdetailCSV = output.csvFile, copyFlag = True, trimFlag = True, wavExtFlag = True,  
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


if __name__ == "__main__":
	parseInput()