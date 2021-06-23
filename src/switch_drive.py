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
			baseUrl = f"https://drive.switch.ch/remote.php/dav/{videoName}"
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
			"requesttoken": "",
			# 'Content-Disposition': 'attachment; filename="source_test.mp4"',
			"OCS-APIREQUEST": "true",
			"X-Requested-With": "XMLHttpRequest",
			"Content-Length": "1353360",
			"Origin": "https://drive.switch.ch",
			"Connection": "keep-alive",
			"Referer": "https://drive.switch.ch/index.php/apps/files/?dir=/test&fileid=2600133444",
			"Cookie": ""
				}


			with open(videoFile,"rb" ) as fileReader:
				response = requests.put(baseUrl, data=fileReader, headers = headers)
				print(response.content)


	def downloadFile(self, fileAdd):
		# 
		url = "https://drive.switch.ch/index.php/apps/files/ajax/download.php?dir="
		headers = {
		"Host": "drive.switch.ch",
		"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0",
		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		"Accept-Language": "en-US,en;q=0.5",
		"Accept-Encoding": "gzip, deflate, br",
		"Connection": "keep-alive",
		"Referer": "https://drive.switch.ch/index.php/apps/files/",
		"Cookie": ""
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

# Cookie: oc641cdd42e0=074582a0da068bc145cd35edcd6c7e15; oc_sessionPassphrase=lTENkODCB%2FOWmIjtJ1wSjKLwxYHJyS%2Bu8eclZyjKCvyLFgFT5KHDxeo3iClBwZnh%2BFvFwyA0R0ZrZ5CBbWjfAwRbaRRLqdx2Oz5Chxylk13bir5KJ%2BLx%2BMbTrn390B5t
