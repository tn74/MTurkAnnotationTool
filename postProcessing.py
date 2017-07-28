import os
import json
import numpy as np
from PIL import Image
from PIL.ImageDraw import Draw
import matplotlib.path as mplPath
import numpy as np
import matplotlib.pyplot as plt
topLevelDir = 'HITBatches'

def genConfArrays(hitBatch, jsonfile):
	if not os.path.exists(topLevelDir + '/' + hitBatch + '/data'):
		os.mkdir(topLevelDir + '/' + hitBatch + '/data')
	fullFile = open(topLevelDir + '/' + hitBatch + '/'+ jsonfile, 'r')
	for jsonText in fullFile:
		imgJSON = json.loads(jsonText)
		imgnameroot = imgJSON['fileName'].split('/')[len(imgJSON['fileName'].split('/'))-1].split('.')[0]
		outdir = topLevelDir + '/' + hitBatch + '/data/' + imgnameroot
		if not os.path.exists(outdir):
			os.mkdir(outdir)
		try: 
			img = Image.open('imToCut/'+imgJSON['fileName'])
		except: 
			try:
				img = Image.open('toWeb/public/Images/'+imgJSON['fileName'])
			except: 
				raise Exception('Could not find image to develop confidence map: ' + 'toWeb/public/Images/'+imgJSON['fileName'] + ' Make sure hte image is either inside toWeb/Images inside a folder with the other cut images or imToCut')
		width, height = img.size
		count = 0
		saveArr = np.zeros([height, width, len(imgJSON['objs'])])
		for obj in imgJSON['objs']:
			npArr = None
			npArr = np.zeros([height, width])
			if (obj['type'] == 'polygon'):
				npArr = processPolygon(npArr, obj['data'])
			if (obj['type'] == 'line'):
				npArr = processLine(npArr, obj['data'])
			if (obj['type'] == 'point'):
				npArr = processPoint(npArr, obj['data'])
			npArrNorm = (normalizeArr(npArr)*255).astype(np.int8)
			npArr = npArr.astype(np.int8)
			imRaw = Image.fromarray(npArr)
			imNormalized = Image.fromarray(npArrNorm).convert('L')
			imRaw.save(outdir + '/raw_' + obj['name'] + '.png')
			imNormalized.save(outdir + '/normalized_' + obj['name'] + '.jpg')
			# plt.title(imgJSON['fileName'] + " " + obj['name'] + " Confidence Map")
			# plt.imshow(normalizeArr(npArr)*255, cmap='binary', interpolation='nearest')
			# plt.colorbar()
			# plt.savefig(outdir +obj['name']+'Conf.png')
			count+=1


def processPolygon(arr, data):
	for i in range(0, len(data[0])):
		procPoly = []
		px = data[0][i]
		py = data[1][i]
		for j in range (len(px)):
			procPoly.append((px[j], py[j]))
		poly = mplPath.Path(procPoly)
		b = poly.get_extents()
		for r in range(int(b.y0),int(b.y1)):
			for c in range(int(b.x0), int(b.x1)):
				if poly.contains_point((c,r)):
					arr[r,c] += 1
	return arr


def processLine(arr,data):
	blank = Image.new('RGB', (len(arr[0]), len(arr)), color = (0,0,0))
	drawer = Draw(blank, 'RGBA')
	for i in range(0, len(data[0])):
		procLine = []
		lx = data[0][i]
		ly = data[1][i]
		for j in range (len(lx)):
			procLine.append((lx[j], ly[j]))
		drawer.line(procLine, fill = (255,255,255,25), width = 5)
	blank = blank.convert('L')
	arr = np.asarray(blank)
	# plt.title("Line Map")
	# plt.imshow(arr, cmap='binary', interpolation='nearest')
	# plt.colorbar()
	# plt.show()
	# for i in range(0,np.amax(arr)+10):
	# 	if i in arr:
	# 		print('i = ' + str(i) + ' is in arr')
	# 	else:
	# 		print('i = ' + str(i) + ' is not in arr')

	# print ("LEN: " + str(arr.shape))
	# print("Max 2: " + str( np.amax(arr)))
	return arr


def processPoint(arr, coords):
	blank = Image.new('RGB', (len(arr[0]), len(arr)))
	drawer = Draw(blank, 'RGBA')
	elrad = 4
	for i in range(len(coords[0])):
		pointArr = []
		pointArr.append(coords[0][i]-elrad)
		pointArr.append(coords[1][i]-elrad)
		pointArr.append(coords[0][i]+elrad)
		pointArr.append(coords[1][i]+elrad)
		drawer.ellipse(pointArr,(255,255,255,25))
	arr = np.asarray(blank)
	print(arr)
	arr = arr[:,:,0]
	print(arr.size)
	return arr

def normalizeArr(arr):
	return np.divide(arr, np.amax(arr))


