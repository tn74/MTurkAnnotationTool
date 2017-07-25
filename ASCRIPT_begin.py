"""
This program publishes images in large batches to Amazon Mechanical Turk for annotation. Once published, all 
information relevant to this batch will be stored inside folders/[batchName and TimeStamp]
Use ASCRIPT_finish.py to get image annotation results once they have been published with this script

Author: Trishul Nagenalli (tn74@duke.edu)
Organization: Duke Energy Data Analytics Lab
"""

import os
from pubfolderhits import publish
from imCut import cut
from subprocess import call
import subprocess

"""
Variable Information: 

processingOneLargeImage -	True if this folder contains hits for a large image that was cut up before being posted online, 
							indicating that the images on Turk are connected to one another (example: cut a large satellite
							image into pieces before posting online)
							False if this folder contains hits for images that are disconnected from one another (example: 
							images are of powerplants across the United States)

imageToCut				-	Name of large image that needs to be cut if processingOneLargeImage is True. Does not matter 
							if processingOneLargeImage is False

folder					-	Name of folder inside toWeb/public/images that contains the images to be annotated

serverType				-	'developer' if you are testing and want to send hits to developer sandbox
							'production' if you want to post online for real people to annotate
							No other values are valid

imagesPerPerson			-	The number of images a single Turk User would be asked to annotate in one HIT Assignemnt

annotations				-	Array of things you would like the Turk Users to annotate in each image. 
							For Each Annotaiion You Add, You Must (example: for a building):
								Create a helpfile in toWeb/Public/helper with name [object name].html  (toWeb/public/helper/building.html)
								Provide a Sample Annotated Image called [object name].png in 
									toWeb/public/images/sample (toWeb/public/images/sample/building.png)
								Add an entry into fileTypes indicating the tool used to annotate the object in:
									toWeb/public/js/neededJSONS.json
									When Adding a building,
									fileTypes = '[{"road":"line","powerplant":"polygon"}]' 
										would become
									fileTypes = '[{"road":"line","powerplant":"polygon","building":"polygon"}]'

Set the variables below before you run the script
"""
processingOneLargeImage = False
imageToCut = 'Norfolk_01_training.tif'
folder = '030740_nw' 

user = 'Bradbury'
serverType = 'developer'				
imagesPerPerson = 5 
annotations = ['solarArray']



if (processingLargeSatelliteImage):
	imgToCut = '030740_nw.tif'
	iname = imgToCut.split('.')[0]
	if not os.path.exists('toWeb/public/images/'+iname):
		cut(imageToCut)

def subprocess_cmd(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print (proc_stdout)
subprocess_cmd('cd toWeb; cd public; firebase deploy') # Puts toWeb folder online at firebase
publish(folder, imagesPerPerson, serverType, annotations, user) # Create and publish hits to Amazonon



