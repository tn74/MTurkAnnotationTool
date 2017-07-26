"""
This program publishes collects annotations for images in large batches from Amazon Mechanical Turk. 
All information relevant to this batch will be stored inside folders/[batchName and TimeStamp]
Use ASCRIPT_begin.py to publish the image annotations FIRST before using this script to collect the results

Author: Trishul Nagenalli (tn74@duke.edu)
Organization: Duke Energy Data Analytics Lab
"""

import retrieveFolder 
import jsonReader
import usefulImageFunc as uif
import postProcessing
from PIL import Image

"""
Variable Information: 
user 					- 	the name of the user under which an AWS access and secret access keys are listed inside the config.ini file

folder 					- 	the directory name inside 'folders' that has a hitList to work with

serverType 				- 	specifies if these images should be pulled off of the development or production server
							note: valid values are only 'production' or 'development'

processingOneLargeImage -	True if this folder contains hits for a large satellite image that was cut up before being posted online, 
							indicating that the images on Turk are connected to one another
							False if this folder contains hits for images that are disconnected from one another (they do not come from 
							the same satellite image)

Set the variables below before you run the script
"""
user = 'trishul3'
folder = 'Norfolk_01_training20170725-230110' 
serverType = 'developer'
processingOneLargeImage = True 


retrieveFolder.retrieve(user, folder, serverType) 
if (processingOneLargeImage):
	jsonReader.condense(folder)
	uif.annImageWholeJSON(folder)
else:
	jr.condenseUnconnected(folder)
	if not os.path.exists('folders/'+folder+'/annotatedImages'):
		os.mkdirs('folders/'+folder+'/annotatedImages')
	for line in open('folders/'+folder+'/condenseIndiJSONS.txt').readlines():
		pilimage = uif.annImageIndi(line)
		js = json.loads(line)
		print(line)
		pilimage.save('folders/'+folder+'/annotatedImages/'+js['fileName'].split('/')[1].split('.')[0]+'ANN.jpg')


# Make geojson with ke as proeprty to last image 