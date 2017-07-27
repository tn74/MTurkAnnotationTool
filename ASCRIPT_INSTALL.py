from subprocess import call
import subprocess
import json
<<<<<<< HEAD
import configparser


firebaseProjectID = 'amtannotate3'

config = configparser.RawConfigParser()
config.add_section('Username Here')
config.add_section('SetUp')
config.set('SetUp', 'firebaseSubdomain', firebaseProjectID)
config.set('Username Here', 'awskey', 'Your AWS Key Here')
config.set('Username Here', 'awssakey', 'Your AWS Secret Access Key')
with open('config.ini', 'w') as configfile:
    config.write(configfile)
=======

firebaseProjectID = 'Your Project ID HERE'
>>>>>>> 27ef332dd9e208d9105de391530d9537ba962a4f
todump = {}
todump["projects"] = {}
todump["projects"]["default"] = firebaseProjectID
json.dump(todump, open('toWeb/.firebaserc', 'w'))
def subprocess_cmd(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print (proc_stdout)
    proc_stdout = process.communicate()[0].strip()
print('Deploying Site... This may take a few minutes')
<<<<<<< HEAD
subprocess_cmd ('cd toWeb && firebase deploy ')
=======
subprocess_cmd ('cd toWeb && firebase deploy')
>>>>>>> 27ef332dd9e208d9105de391530d9537ba962a4f
