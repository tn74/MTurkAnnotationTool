from PIL import Image
import os

## INPUT ITEMS
def cut(inFile):
	"""
	:param inFile: name of image file to cut up for posting on mturk. Image must be inside folder imToCut
	:return: no return. Stores all cut images in toWeb/public/images/[image name without extension]
	"""
	upper = 0
	left = 0 
	count = 0
	length  = 400
	overlap = 100

	imagename = 'imToCut/'+inFile	 # INSERT THE IMAGE NAME THAT YOU WANT TO CUT HERE
	direc = imagename.split('/')
	iname = direc[len(direc)-1].split('.')[0]
	print(iname)
	im = Image.open(imagename).convert("RGB")
	outdir = os.path.join(os.path.dirname(os.path.realpath(__file__)),'toWeb/public/images', iname)
	if not os.path.exists(outdir):
	    os.makedirs(outdir)
	width, height = im.size
	imagesize = width
	 
	while upper < height:
		while left < width:
			bbox = (left, upper, left + length, upper + length)
			working_slice = im.crop(bbox)
			tempw, temph = working_slice.size
			#print ("Temp: " + str(tempw) + " " + str(temph))
			if (left+length)<=imagesize and (upper+length)<=imagesize:	
				outfilename = os.path.join(outdir, iname + "_" + "U" + str(upper).zfill(4) + "_L" + str(left).zfill(4) + ".jpg")
				working_slice.save(outfilename)
			count +=1
			left += length-overlap
		upper += length-overlap
		left = 0
		print("Upper Dimension: " + str(upper))

	imagename = imagename[:str.rindex(imagename,'.')]
	savejpg = imagename + '.jpg'
	im.save(savejpg)
