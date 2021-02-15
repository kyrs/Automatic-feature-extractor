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
		mp4Files = glob.glob(join(dirAdd,"*.mp4"))
		for videoFile in mp4Files:
			videoName = os.path.basename(videoFile)
			print(f"video name : {videoName}")
			print(f"video file : {videoFile}")
			# https://drive.switch.ch/remote.php/dav/files/kumar.shubham%40unil.ch/pose_transfer_PIV_output/24oct/ppo2_A2c_1e7.png
			baseUrl = f"https://drive.switch.ch/remote.php/dav/files/kumar.shubham%40unil.ch/pose_transfer_PIV_output/compressed/{videoName}"
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
			"Cookie": "oc641cdd42e0=0d771469bc868f390f345bb7c0f1824e; oc_sessionPassphrase=Mi4fk7TrfPdGk%2FGzmz%2F2qVQwls79eJqI74sUrFN5jjOgEKug9TL7rtujC2kJS%2BrVaYa%2BpkUd%2FR1lkYEneqUqiAA347FJectGmcQd1ZwfsO24UTSw2V7NOPC3ic0c3OwM"
				}


			with open(videoFile,"rb" ) as fileReader:
				response = requests.put(baseUrl, data=fileReader, headers = headers)
				print(response.content)


	def downloadFile(self, fileAdd):
		url ="https://drive.switch.ch/index.php/apps/files/ajax/download.php?dir=%2FPoseTransfer_PIV%2FDemoUncompressed&files[]=PTspeech_demo_PT001.mp4&files[]=PTspeech_demo_PT000control.mp4&downloadStartSecret=6oewin09peh"
		headers = {
		"Host": "drive.switch.ch",
		"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0",
		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		"Accept-Language": "en-US,en;q=0.5",
		"Accept-Encoding": "gzip, deflate, br",
		"Connection": "keep-alive",
		"Referer": "https://drive.switch.ch/index.php/apps/files/?dir=/PoseTransfer_PIV&fileid=2779422448",
		"Cookie": "oc641cdd42e0=0d771469bc868f390f345bb7c0f1824e; oc_sessionPassphrase=Mi4fk7TrfPdGk%2FGzmz%2F2qVQwls79eJqI74sUrFN5jjOgEKug9TL7rtujC2kJS%2BrVaYa%2BpkUd%2FR1lkYEneqUqiAA347FJectGmcQd1ZwfsO24UTSw2V7NOPC3ic0c3OwM"
		}
		print("DOWNLOADING THE FILE !!")
		r = requests.get(url, headers = headers, stream=True)
		print("FETCHED !!")
		# print(r.content)
		z = zipfile.ZipFile(io.BytesIO(r.content))
		z.extractall(fileAdd)



if __name__ =="__main__":
	obj = SwitchDrive()
	obj.uploadFile("/home/ubuntu/UNIL-PROJECT_PROCESS/BASE_VIDEO/new_demo_file/uploadFile")
	# obj.downloadFile("/home/ubuntu/UNIL-PROJECT_PROCESS/BASE_VIDEO/new_demo_file")
