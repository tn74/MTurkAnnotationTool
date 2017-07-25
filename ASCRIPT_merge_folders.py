import os
import jsonReader
import usefulImageFunc as uif
import time
import postProcessing as pp


inFolders = ['Norfolk_01_training20170615-180223', 'Norfolk_01_training20170615-180134']
outFolder = 'NorfolkTrainingMerge1'

oPath = 'folders/' + outFolder
try:
	os.mkdir(oPath)
except:
	print("Did not make directory")

hitList = open(oPath+'/hitList.txt', 'w')
indList = open(oPath+'/indJSONS.txt', 'w')

for f in inFolders :
	print("Adding: " + f)
	hitlines = open('folders/' + f + '/hitList.txt', 'r').readlines()
	for line in hitlines:
		hitList.write(line)
	print()
	indlines = open('folders/' + f + '/indJSONS.txt', 'r').readlines()
	for line in indlines:
		indList.write(line)

indList.close()
hitList.close()

jsonReader.condense(outFolder)
uif.annImageWholeJSON(outFolder)
pp.genConfArrays(outFolder)


