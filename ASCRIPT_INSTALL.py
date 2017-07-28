"""
Author: Trishul Nagenalli (tn74@duke.edu)
Organization: Duke Energy Data Analytics Lab

Description:
Use this script to help speed the installation process on your computer. The primary purpose of this program is to get 
your firebase site up and running. To do so, you must have installed the Firebase CLI and have created a firebase 
project on https://console.firebase.google.com/

If you have not already done so, please open your terminal, move into this folder and run:
firebase login
and login to the google account associated with your firebase project

You must know your firebase project's ID to run this install script. Enter
firebase list
into the terminal to see all projects associated with your firebase account and their respective IDs. Set 
the variables firebaseProjectID to be the ID you wish to use

Once this script has completed, you will need to add your AWS Access and Secret Access Keys into the config file

Variable Information

firbaseProjectID				- 	The id of your firebase project that will be used to commit host your the 
									annnotation tool online
"""
#====================== Set Variables below
firebaseProjectID = 'Your firebase project id here'
#====================== 



from subprocess import call
import subprocess
import json
import configparser
import os

topLevelDir = 'HITBatches'
if not (os.path.exists('config.ini')):
	config = configparser.RawConfigParser()
	config.add_section('Username Here')
	config.add_section('SetUp')
	config.set('SetUp', 'firebaseSubdomain', firebaseProjectID)
	config.set('Username Here', 'awskey', 'Your AWS Key Here')
	config.set('Username Here', 'awssakey', 'Your AWS Secret Access Key')
	with open('config.ini', 'w') as configfile:
	    config.write(configfile)
if not (os.path.exists(topLevelDir)):
	os.mkdir(topLevelDir)
todump = {}
todump["projects"] = {}
todump["projects"]["default"] = firebaseProjectID
json.dump(todump, open('toWeb/.firebaserc', 'w'))
def subprocess_cmd(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print (proc_stdout)
print('Deploying Site... This may take a few minutes')
subprocess_cmd ('cd toWeb && firebase deploy ')
print('Site Deployed! Installation Finished. Please insert your AWS Access and Secret Access Keys inside the config file')
