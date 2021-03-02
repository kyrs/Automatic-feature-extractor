"""
 __name__ : Kumar Shubham
__date__ : 19 Auguust 2020
__Desc__ : file to upload videso to switchDrive


"""
import requests, zipfile,io

from os.path import join, basename, isfile
import glob
from pathlib import Path
import os
class SwitchDrive(object):

	def __init__(self):
		pass


	def uploadFile(self, dirAdd):
		print("UPLOADING THE FILE !!! ")
		mp4Files = glob.glob(join(dirAdd,"*.avi"))
		for videoFile in mp4Files:
			videoName = os.path.basename(videoFile)
			print(f"video name : {videoName}")
			print(f"video file : {videoFile}")
			#https://drive.switch.ch/remote.php/dav/files/kumar.shubham%40unil.ch/PT_AE/openpose_video/session1/test.txt
			# https://drive.switch.ch/remote.php/dav/files/kumar.shubham%40unil.ch/pose_transfer_PIV_output/24oct/ppo2_A2c_1e7.png
			baseUrl = f"https://drive.switch.ch/remote.php/dav/files/kumar.shubham%40unil.ch/PT_AE/openpose_video/session2/{videoName}"
			print(f"baseUrl : {baseUrl}")
			headers = {
			"Host": "drive.switch.ch",
			"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0",
			"Accept": "*/*",
			"Accept-Language": "en-US,en;q=0.5",
			"Accept-Encoding": "gzip, deflate, br",
			"Content-Type": "video/mp4",
			"If-None-Match": "*",
			"X-OC-Mtime": "1586339909",
			"requesttoken": "DgNRPREFD0NYAFEPWlEmARQSe1YuDwRuAzQ6LRgVLCo=:OVfWDNC/jkf6bbk7lK0ykfmWMlreMotYosDjDkA9Xug=",
			# 'Content-Disposition': 'attachment; filename="source_test.mp4"',
			"OCS-APIREQUEST": "true",
			"X-Requested-With": "XMLHttpRequest",
			"Content-Length": "1353360",
			"Origin": "https://drive.switch.ch",
			"Connection": "keep-alive",
			"Referer": "https://drive.switch.ch/index.php/apps/files/?dir=/test&fileid=2600133444",
			"Cookie": "oc641cdd42e0=074582a0da068bc145cd35edcd6c7e15; oc_sessionPassphrase=lTENkODCB%2FOWmIjtJ1wSjKLwxYHJyS%2Bu8eclZyjKCvyLFgFT5KHDxeo3iClBwZnh%2BFvFwyA0R0ZrZ5CBbWjfAwRbaRRLqdx2Oz5Chxylk13bir5KJ%2BLx%2BMbTrn390B5t"
				}


			with open(videoFile,"rb" ) as fileReader:
				response = requests.put(baseUrl, data=fileReader, headers = headers)
				print(response.content)


	def downloadFile(self, fileAdd):
		# url ="https://drive.switch.ch/index.php/apps/files/ajax/download.php?dir=%2FPT_AE&files=original&downloadStartSecret=cogvjezea5c"
		url = "https://drive.switch.ch/index.php/apps/files/ajax/download.php?dir=%2FPT_AE%2Foriginal%2Fsession2&files[]=PT084_task2.mp4&files[]=PT087_task2.mp4&files[]=PT085_task2.mov&files[]=PT089_task2.mp4&files[]=PT092_task2.mp4&files[]=PT093_task2.mp4&files[]=PT096_task2.mp4&files[]=PT090_task2.mp4&files[]=PT095_task2.mp4&files[]=PT083_task2.mov&files[]=PT100_task2.mp4&files[]=PT102_task2.mov&files[]=PT104_task2.mp4&files[]=PT105_task2.mov&files[]=PT108_task2.mov&files[]=PT110_task2.mov&files[]=PT103_task2.mov&files[]=PT107_task2.MOV&files[]=PT109_task2.mov&files[]=PT113_task2.MOV&files[]=PT120_task2.mp4&files[]=PT116_task2.mp4&files[]=PT111_task2.mov&files[]=PT112_task2.mp4&files[]=PT123_task2.mov&files[]=PT118_task2.mov&files[]=PT124_task2.mp4&files[]=PT126_task2.mov&files[]=PT129_task2.mp4&files[]=PT127_task2.mov&downloadStartSecret=ny1pjlr8hk"
		headers = {
		"Host": "drive.switch.ch",
		"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0",
		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		"Accept-Language": "en-US,en;q=0.5",
		"Accept-Encoding": "gzip, deflate, br",
		"Connection": "keep-alive",
		"Referer": "https://drive.switch.ch/index.php/apps/files/?dir=/PoseTransfer_PIV&fileid=2779422448",
		"Cookie": "oc641cdd42e0=15e13bf3b80f8c9c62b05d0ae8998eda; oc_sessionPassphrase=lTENkODCB%2FOWmIjtJ1wSjKLwxYHJyS%2Bu8eclZyjKCvyLFgFT5KHDxeo3iClBwZnh%2BFvFwyA0R0ZrZ5CBbWjfAwRbaRRLqdx2Oz5Chxylk13bir5KJ%2BLx%2BMbTrn390B5t"
		}
		print("DOWNLOADING THE FILE !!")
		r = requests.get(url, headers = headers, stream=True)
		print("FETCHED !!")
		# print(r.content)
		z = zipfile.ZipFile(io.BytesIO(r.content))
		z.extractall(fileAdd)



if __name__ =="__main__":
	obj = SwitchDrive()
	obj.uploadFile("/home/ubuntu/Automatic-feature-extractor/results/session2/openpose/compressed")
	# obj.downloadFile("/home/ubuntu/Automatic-feature-extractor/base_video/unil_dataset/session2/set3")
# Host: drive.switch.ch
# User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0
# Accept: */*
# Accept-Language: en-US,en;q=0.5
# Accept-Encoding: gzip, deflate, br
# Content-Type: text/plain
# If-None-Match: *
# X-OC-Mtime: 1613507999
# requesttoken: cBJiDiZhNlwcQytVMHFRVTEXZycBECZUGAwKKCAWEQQ=:5k2XmNG3y4GbF9eataQSFUvd/FCQnedwf0Di+0IvcYU=
# Content-Disposition: attachment; filename="test.txt"
# OCS-APIREQUEST: true
# X-Requested-With: XMLHttpRequest
# Content-Length: 0
# Origin: https://drive.switch.ch
# Connection: keep-alive
# Referer: https://drive.switch.ch/index.php/apps/files/?dir=/PT_AE/openface_video/session2&fileid=3149476695
# Cookie: oc641cdd42e0=074582a0da068bc145cd35edcd6c7e15; oc_sessionPassphrase=lTENkODCB%2FOWmIjtJ1wSjKLwxYHJyS%2Bu8eclZyjKCvyLFgFT5KHDxeo3iClBwZnh%2BFvFwyA0R0ZrZ5CBbWjfAwRbaRRLqdx2Oz5Chxylk13bir5KJ%2BLx%2BMbTrn390B5t