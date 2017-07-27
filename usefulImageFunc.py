import json
import os
from PIL import Image
from PIL.ImageDraw import Draw

topLevelDir = 'HITBatches'

def annImageWholeJSON(folder, annotationFile):
	"""
	Generates and saves a fully annoted version of the fullSatellite image inside folder
	:param folder: folder name containing a wholeJSON.txt file and where annotated image will be saved
	:return: None. Saves the full satelite image annotated with everything inside the wholeJSON.txt file
	"""
	contentstring = open(topLevelDir + '/' + folder + '/' + annotationFile, "r").readlines()
	annotationFileBase = annotationFile.split('.')[0]
	im = None
	for line in contentstring:
		linejson = json.loads(line)
		im = annImage('imToCut/'+linejson['fileName'], line)
	im.save(topLevelDir + '/' + folder + '/' + annotationFileBase + '_annotations.png')

def annImageIndi(jsonText):
	"""
	Returns a PIL Image object with all the annotations for a given taskImage
	:param jsonText: String - jsonObject text describing 
	:return:
	"""
	jsonObject = json.loads(jsonText)
	return annImage('toWeb/public/images/'+jsonObject['fileName'], jsonText)


def annImage(imgPath, jsonText, **kwargs):
	if ('fillColorArr' in kwargs): fillColor = kwargs['fillColorArr']
	else: fillColorArr = ['blue', 'red', 'green', 'orange', 'brown']
	imFile = Image.open(imgPath)
	inf = json.loads(jsonText)
	for i in range(len(inf['objs'])):
		obj = inf['objs'][i]
		if (obj['type'] == 'polygon'):
			imFile = drawPolygonObjects(imFile, obj['data'], fillColor = fillColorArr[i])
		if (obj['type'] == 'line'):
			imFile = drawLineObjects(imFile, obj['data'], fillColor = fillColorArr[i])
		if (obj['type'] == 'point'):
			imFile = drawPointObjects(imFile, obj['data'], fillColor = fillColorArr[i])
	return imFile

def gen_Image(imgPath, jsonText, **kwargs): # for hit checker
	if ('fillColorArr' in kwargs): fillColor = kwargs['fillColorArr']
	else: fillColorArr = ['blue', 'red', 'green', 'orange', 'brown']
	imFile = Image.open(imgPath)
	inf = json.loads(jsonText)
	for i in range(len(inf['objs'])):
		obj = inf['objs'][i]
		if (obj['type'] == 'polygon'):
			imFile = drawPolygonObjects(imFile, obj['data'], fillColor = fillColorArr[i])
		if (obj['type'] == 'line'):
			imFile = drawLineObjects(imFile, obj['data'], fillColor = fillColorArr[i])
		if (obj['type'] == 'point'):
			imFile = drawPointObjects(imFile, obj['data'], fillColor = fillColorArr[i])
	name = imgPath + ".jpg"
	imFile.save(imgPath + ".jpg")
	return name


def drawPolygonObjects(im, data, **kwargs):
	if ('fillColor' in kwargs): fillColor = kwargs['fillColor']
	else: fillColor = 'blue'

	drawIm = Draw(im)
	for ind in range(0, len(data[0])):
		im = drawPoly(im, [data[0][ind], data[1][ind]], drawIm = drawIm, fillColor = fillColor)
	return im;

def drawPoly(im, coords, **kwargs):
	# May or may not be taken care of by kwargs
	if not('drawIm' in kwargs): drawIm = kwargs['drawIm']
	else: drawIm = Draw(im)

	if ('fillColor' in kwargs): fillColor = kwargs['fillColor']
	else: fillColor = 'blue'

	polyArr = []
	for j in range(len(coords[0])):
		polyArr.append(coords[0][j])
		polyArr.append(coords[1][j])

	drawIm.line(polyArr, fill = fillColor, width = 5)
	drawIm.line([polyArr[len(polyArr)-2], polyArr[len(polyArr)-1], polyArr[0], polyArr[1]], fill = fillColor, width = 5)
	return im

def drawLineObjects(im, data, **kwargs):
	if ('fillColor' in kwargs): fillColor = kwargs['fillColor']
	else: fillColor = 'blue'

	drawIm = Draw(im)
	for ind in range(0, len(data[0])):
		im = drawLine(im, [data[0][ind], data[1][ind]], drawIm = drawIm, fillColor = fillColor)
	return im;

def drawLine(im, coords, **kwargs):
	# May or may not be taken care of by kwargs
	if not('drawIm' in kwargs): drawIm = kwargs['drawIm']
	else: drawIm = Draw(im)

	if ('fillColor' in kwargs): fillColor = kwargs['fillColor']
	else: fillColor = 'blue'

	polyArr = []
	for j in range(len(coords[0])):
		polyArr.append(coords[0][j])
		polyArr.append(coords[1][j])

	drawIm.line(polyArr, fill = fillColor, width = 5)
	return im

def drawPointObjects(im, data, **kwargs):
	if ('drawIm' in kwargs): drawIm = kwargs['drawIm']
	else: drawIm = Draw(im)

	if ('fillColor' in kwargs): fillColor = kwargs['fillColor']
	else: fillColor = 'red'

	if ('elrad' in kwargs): fillColor = kwargs['elrad']
	else: elrad = 3

	coords = data
	for i in range(len(coords[0])):
		pointArr = []
		pointArr.append(coords[0][i]-elrad)
		pointArr.append(coords[1][i]-elrad)
		pointArr.append(coords[0][i]+elrad)
		pointArr.append(coords[1][i]+elrad)
		drawIm.ellipse(pointArr, fill = fillColor)
	return im

