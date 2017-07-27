import os
import json
import numpy as np
from PIL import Image
from PIL.ImageDraw import Draw
import matplotlib.path as mplPath
import numpy as np
import matplotlib.pyplot as plt
topLevelDir = 'HITBatches'

def genConfArrays(folder):
	if not os.path.exists(topLevelDir + '/' + folder + '/data'):
		os.mkdir(topLevelDir + '/' + folder + '/data')
	jsonText = open(topLevelDir + '/' + folder + '/wholeJSON.txt', 'r').readline()
	wholeImg = json.loads(jsonText);
	img = Image.open('imToCut/'+wholeImg['fileName'])
	width, height = img.size
	count = 0
	saveArr = np.empty([height, width, len(wholeImg['objs'])])
	for obj in wholeImg['objs']:
		npArr = np.empty([height, width])
		if (obj['type'] == 'polygon'):
			npArr = processPolygon(npArr, obj['data'])
			print()
		if (obj['type'] == 'line'):
			npArr = processLine(npArr, obj['data'])
		if (obj['type'] == 'point'):
			npArr = processPoint(npArr, obj['data'])
		npArr = npArr.astype(int)
		plt.title(wholeImg['fileName'] + " " + obj['name'] + " Condfidence Map")
		plt.imshow(npArr, cmap='hot', interpolation='nearest')
		plt.savefig(topLevelDir + '/' + folder + '/' +obj['name']+'Conf.png')
		saveArr[:,:,count] = npArr
		count+=1
		print ("Objects Completed: " + str(count))
		np.savez_compressed(topLevelDir + '/'+folder+'/data/'+obj['name']+'.npz', data = npArr)


def processPolygon(arr, data):
	for i in range(0, len(data[0])):
		print("Processed: " +str(i))
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
	blank = Image.new('RGB', (len(arr[0]), len(arr)))
	drawer = Draw(blank, 'RGBA')
	for i in range(0, len(data[0])):
		print("Processed: " +str(i))
		procLine = []
		lx = data[0][i]
		ly = data[1][i]
		for j in range (len(lx)):
			procLine.append((lx[j], ly[j]))
		drawer.line(procLine, (255, 0, 0, 25), width = 5)
	arr = np.asarray(blank)

	arr = arr[:,:,0]
	print(arr.size)
	return arr


def processPoint(arr, coords):
	blank = Image.new('RGB', (len(arr[0]), len(arr)))
	drawer = Draw(blank, 'RGBA')
	elrad = 4
	for i in range(len(coords[0])):
		print("Processed: " +str(i))
		pointArr = []
		pointArr.append(coords[0][i]-elrad)
		pointArr.append(coords[1][i]-elrad)
		pointArr.append(coords[0][i]+elrad)
		pointArr.append(coords[1][i]+elrad)
		drawer.ellipse(pointArr,(255,0,0,25))
	arr = np.asarray(blank)
	print(arr)
	arr = arr[:,:,0]
	print(arr.size)
	return arr



