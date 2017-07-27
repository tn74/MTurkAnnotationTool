from subprocess import call
import subprocess
import json

firebaseProjectID = 'Your Project ID HERE'
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
subprocess_cmd ('cd toWeb && firebase deploy')