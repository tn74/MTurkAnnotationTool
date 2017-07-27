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
user = 'Trishul'
hitBatch = 'Norfolk_01_training20170727-152336' 
serverType = 'developer'
#=====================================


import retrieveFolder 
import jsonReader as jr
import usefulImageFunc as uif
import postProcessing
from PIL import Image
import os
import json

topLevelDir = 'HITBatches'
retrieveFolder.retrieve(user, hitBatch, serverType) 
allSubmittedCondensedDir = 'allSubmittedCondensedImages'
acceptedCondensedDir = 'acceptedCondensedImages'
jr.condense(hitBatch, 'all_submitted.txt')
if not os.path.exists(topLevelDir + '/' + hitBatch + '/' + allSubmittedCondensedDir):
	os.mkdir(topLevelDir + '/'+hitBatch+'/' + allSubmittedCondensedDir)
for line in open(topLevelDir + '/'+hitBatch+'/all_submitted.txt').readlines():
	pilimage = uif.annImageIndi(line)
	js = json.loads(line)
	print(line)
	pilimage.save(topLevelDir + '/'+hitBatch+'/'+ allSubmittedCondensedDir + '/' + js['fileName'].split('/')[1].split('.')[0]+'ANN.jpg')

if os.path.exists(topLevelDir + '/'+hitBatch+'/accepted.txt'):
	jr.condense(hitBatch, 'accepted.txt')
	if not os.path.exists(topLevelDir + '/' + hitBatch + '/' + acceptedCondensedDir):
		os.mkdir(topLevelDir + '/'+hitBatch+'/' + acceptedCondensedDir)
	for line in open(topLevelDir + '/'+hitBatch+'/accepted.txt').readlines():
		pilimage = uif.annImageIndi(line)
		js = json.loads(line)
		print(line)
		pilimage.save(topLevelDir + '/'+hitBatch+'/'+ acceptedCondensedDir + '/' + js['fileName'].split('/')[1].split('.')[0]+'ANN.jpg')


# Make geojson with ke as proeprty to last image 