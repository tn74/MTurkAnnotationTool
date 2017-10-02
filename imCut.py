from PIL import Image
import os

## INPUT ITEMS
def cut(inFile, length, overlap):
	"""
	:param inFile: name of image file to cut up for posting on mturk. Image must be inside folder imToCut
	:param length: length of a side of a square for an individual image to be cut up
	:param overlap: overlap between images
	:return: no return. Stores all cut images in toWeb/public/images/[image name without extension]
	"""

	upper = 0
	left = 0 
	count = 0
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
	 
	while upper < height-length:
		while left < width-length:
			bbox = (left, upper, left + length, upper + length)
			working_slice = im.crop(bbox)
			tempw, temph = working_slice.size
			outfilename = os.path.join(outdir, iname + "_" + "U" + str(upper).zfill(4) + "_L" + str(left).zfill(4) + ".jpg")
			working_slice.save(outfilename)
			count +=1
			left += length-overlap
			print("Upper Dimension: " + str(upper) + ", Left Dimension: " + str(left))
		upper += length-overlap
		left = 0
		
	# Right Border Images
	upper = 0
	left = width - length
	while upper < height-length:
		bbox = (left, upper, left + length, upper + length)
		working_slice = im.crop(bbox)
		outfilename = os.path.join(outdir, iname + "_" + "U" + str(upper).zfill(4) + "_L" + str(left).zfill(4) + ".jpg")
		working_slice.save(outfilename)
		print("Upper Dimension: " + str(upper) + ", Left Dimension: " + str(left))
		upper += length-overlap


	
	# Bottom Border Images
	upper = height - length
	left = 0
	while left < width-length:
		bbox = (left, upper, left + length, upper + length)
		working_slice = im.crop(bbox)
		outfilename = os.path.join(outdir, iname + "_" + "U" + str(upper).zfill(4) + "_L" + str(left).zfill(4) + ".jpg")
		working_slice.save(outfilename)
		print("Upper Dimension: " + str(upper) + ", Left Dimension: " + str(left))
		left += length-overlap


	# Bottom Right Image
	left = width-length
	upper = height - length
	bbox = (left, upper, left + length, upper + length)
	working_slice = im.crop(bbox)
	outfilename = os.path.join(outdir, iname + "_" + "U" + str(upper).zfill(4) + "_L" + str(left).zfill(4) + ".jpg")
	working_slice.save(outfilename)
	print("Upper Dimension: " + str(upper) + ", Left Dimension: " + str(left))


	imagename = imagename[:str.rindex(imagename,'.')]
	savejpg = imagename + '.jpg'
	im.save(savejpg)
