"""
This program publishes collects annotations for images in large batches from Amazon Mechanical Turk. 
All information relevant to this batch will be stored inside hitBatchs/[batchName and TimeStamp]
Use ASCRIPT_begin.py to publish the image annotations FIRST before using this script to collect the results

Author: Trishul Nagenalli (tn74@duke.edu)
Organization: Duke Energy Data Analytics Lab

Variable Information: 
user 					- 	the name of the user under which an AWS access and secret access keys are listed inside the config.ini file

hitBatch 				- 	the folder name inside 'hitBatches' that has a hitList to work with

serverType 				- 	specifies if these images should be pulled off of the development or production server
							note: valid values are only 'production' or 'development'

processingOneLargeImage -	True if this hitBatch contains hits for a large satellite image that was cut up before being posted online, 
							indicating that the images on Turk are connected to one another
							False if this hitBatch contains hits for images that are disconnected from one another (they do not come from 
							the same satellite image)
"""
#===================================== Set the variables below before you run the script
user = 'Bradbury'
hitBatch = 'StolenFromGPU' 
serverType = 'production'
#=====================================


import retrieveFolder 
import jsonReader as jr
import usefulImageFunc as uif
import postProcessing
from PIL import Image
import os
import json
import postProcessing as pp

topLevelDir = 'HITBatches'
outputDir = topLevelDir + '/' +  hitBatch
retrieveFolder.retrieve(user, hitBatch, serverType) 
allSubmittedCondensedDir = 'allSubmittedCondensedImages'
acceptedCondensedDir = 'acceptedCondensedImages'
jr.condense(hitBatch, 'all_submitted.txt')

if not os.path.exists(outputDir + '/' + allSubmittedCondensedDir):
	os.mkdir(outputDir +'/' + allSubmittedCondensedDir)


print ('Making condensed images from all_submitted.txt')
imgCount = 0
totalLines = len(open(outputDir +'/all_submitted.txt').readlines())
for line in open(outputDir +'/all_submitted.txt').readlines():
	imgCount += 1
	js = json.loads(line)
	outImgPath = outputDir + '/' + allSubmittedCondensedDir + '/' + js['fileName'].split('/')[1].split('.')[0]+'ANN.jpg'
	if (os.path.exists(outImgPath)): continue
	pilimage = uif.annImageIndi(line)
	pilimage.save(outImgPath)
	print ("Images Made: " + str(imgCount) + ", " + str(totalLines-imgCount) + " lines to go", end = "\r")
print ("Images Made: " + str(imgCount) + ", " + str(totalLines-imgCount) + " lines to go")
print('Completed making condensed images')
print()

if os.path.exists(outputDir + '/accepted.txt'):
	print ('Making Condensed Images from accepted.txt')
	imgCount = 0
	totalLines = len(open(outputDir +'/accepted.txt').readlines())
	jr.condense(hitBatch, 'accepted.txt')
	if not os.path.exists(outputDir + '/' + acceptedCondensedDir):
		os.mkdir(outputDir + '/' + acceptedCondensedDir)
	for line in open(outputDir +'/accepted.txt').readlines():
		imgCount += 1
		js = json.loads(line)
		outImgPath = outputDir +'/'+ acceptedCondensedDir + '/' + js['fileName'].split('/')[1].split('.')[0]+'ANN.jpg'
		if (os.path.exists(outImgPath)): continue
		pilimage = uif.annImageIndi(line)
		pilimage.save(outImgPath)
		print ("Images Made: " + str(imgCount) + ", " + str(totalLines-imgCount) + " lines to go", end = "\r")
	print ("Images Made: " + str(imgCount) + ", " + str(totalLines-imgCount) + " lines to go")
	print('Completed making condensed images')
	print()

	pp.genConfArrays(hitBatch, 'condensed_accepted.txt') 
else: 
	print ('No accepted.txt file found')

# Make geojson with ke as proeprty to last image 