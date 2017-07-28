import json
import os
from PIL import Image
from PIL.ImageDraw import Draw

topLevelDir = 'HITBatches'

def consolidateLargeImage(hitBatch, jsonFileToConsolidate):
	"""
	:param hitBatch: String - name of hitBatch (inside HITBatches) to process.
	:param jsonFileToConsolidate: String - name of file containing annotations in json form that should be consolidated into a larger image
	:return: None - Method processes indJSON.txt file inside hitBatch and produces the wholeJSON.txt
	"""
	img = {'fileName':'', 'annotations':[], 'objs':[]}
	contentstring = open(topLevelDir + '/'+hitBatch+'/' + jsonFileToConsolidate, "r").readlines()
	print(topLevelDir + '/' + hitBatch + '/' + jsonFileToConsolidate)
	print (contentstring)
	num_lines = len(contentstring)
	for x in range(0, num_lines):
		# FINDS THE INCREMENT VALUE FOR X AND Y
		currline = contentstring[x]
		cont = json.loads(currline)
		filepath = cont['fileName'].split('/')
		filename = filepath[len(filepath)-1][0:str.rindex(str(filepath[len(filepath)-1]),'.')]
		print (filename)
		last = len(filename)
		leftVal = int(filename[(last-4):last])
		topVal = int(filename[(last-10):last-6])
		print (str(leftVal) + " " + str(topVal))
		filename = filename[:-12]
		img['fileName']=filename+'.jpg'

		# ADD POSITION VALUE TO EACH HIT 
		for obj in cont['objs']:
			obj['data'][0] = convertDataRecurse(obj['data'][0], leftVal)
			obj['data'][1] = convertDataRecurse(obj['data'][1], topVal)

		# Merge data arrays for each object
		for obj in cont['objs']:
			if not(obj['name'] in img['annotations']):
				img['annotations'].append(obj['name'])
				img['objs'].append(obj)
			else:
				for annObj in img['objs']:
					if (annObj['name'] == obj['name']):
						print(annObj)
						print(obj)
						annObj['data'][0] = annObj['data'][0] + obj['data'][0]
						annObj['data'][1] = annObj['data'][1] + obj['data'][1]


	#Write to file
	writeFileName = topLevelDir + '/' + hitBatch + '/pieced_' + jsonFileToConsolidate
	writeFile = open(writeFileName, 'w')
	fullImgjson = json.dumps(img)
	writeFile.write(fullImgjson)

# Draw all the annotations on the original and save it


def condense(hitBatch, fileToCondense):
	"""
	
	"""
	allFiles = {}
	for line in open(topLevelDir + '/'+hitBatch+'/' + fileToCondense).readlines():
		indObj = json.loads(line)
		if (indObj['fileName'] not in allFiles):
			allFiles[indObj['fileName']] = indObj
		else:
			for i in range(0, len(allFiles[indObj['fileName']]['objs'])):
				annObj = allFiles[indObj['fileName']]['objs'][i]
				obj = indObj['objs'][i]
				if (annObj['name'] == obj['name']):
					annObj['data'][0] = annObj['data'][0] + obj['data'][0]
					annObj['data'][1] = annObj['data'][1] + obj['data'][1]
					if (not obj['name'] in allFiles[indObj['fileName']]['annotations']):
						allFiles[indObj['fileName']]['annotations'].append(obj['name'])
					break
	writeFileName = topLevelDir + '/' + hitBatch + '/condensed_' + fileToCondense
	writeFile = open(writeFileName, 'w')
	for key in allFiles:
		jsontext = json.dumps(allFiles[key])
		writeFile.write(jsontext+'\n')



def convertDataRecurse(data, addVal):
	"""
	Method is used to convert an annotation on an individual image to its corresponding one on the larger uncut image
	by adding the pixel coordinates of the top left corner of the smaller (cut) image to each of the annotations
	:param data: Multidimensional numeric array. It is either data[0] (x coordinates) or data [1] (y coordinates) of
	the annotation
	:param addVal: value to add to each number (x or y coordinate of cut image's top left corner)
	:return: same as data with changed values
	"""
	if (not (isinstance(data, list))):
		return data + addVal
	for i in range(0,len(data)):
		data[i] = convertDataRecurse(data[i], addVal)
	return data









