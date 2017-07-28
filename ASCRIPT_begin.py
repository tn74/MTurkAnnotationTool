"""
This program publishes images in large batches to Amazon Mechanical Turk for annotation. Once published, all 
information relevant to a particular batch will be stored inside HITBatches/[batchName and TimeStamp]
Use ASCRIPT_finish.py to get image annotation results once they have been published with this script

Author: Trishul Nagenalli (tn74@duke.edu)
Organization: Duke Energy Data Analytics Lab

Variable Information: 

folderToPublish			-	Name of folder inside toWeb/public/images that contains the images to be annotated. It must be 
							the name of the image that was cut up without the file extension of processingOneLargeImage is True

serverType				-	'developer' if you are testing and want to send hits to developer sandbox
							'production' if you want to post online for real people to annotate
							No other values are valid

imagesPerPerson			-	The number of images a single Turk User would be asked to annotate in one HIT Assignemnt

annotations				-	Array of things you would like the Turk Users to annotate in each image. 
							For Each Annotaiion You Add, You must do the following (example for a building in parenthesis):
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
#=====================================
folderToPublish = 'Norfolk_01_training' # Must be name of image that was cut if using LargeImage pre and post processing scripts
user = 'Trishul' # Name of user inside config file
serverType = 'developer'				
imagesPerPerson = 2 
annotations = ['building','road','powerplant']

#=====================================

import os
from pubfolderhits import publish
from imCut import cut
from subprocess import call
import subprocess
import configparser
import json

topLevelDir = 'HITBatches'

config = configparser.ConfigParser()
config.read('config.ini')
firebaseProjectID = config['SetUp']['firebaseSubdomain']
todump = {}
todump["projects"] = {}
todump["projects"]["default"] = firebaseProjectID
json.dump(todump, open('toWeb/.firebaserc', 'w'))
def subprocess_cmd(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print (proc_stdout)
print('Deploying Site... This may take a few minutes')
subprocess_cmd ('cd toWeb && firebase deploy') # Puts toWeb folder online at firebase
print('Site deployed')
if not (os.path.exists(topLevelDir)):
	os.mkdir(topLevelDir)
publish(folderToPublish, imagesPerPerson, serverType, annotations, user) # Create and publish hits to Amazonon



