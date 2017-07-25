Code Flow:

The publishing code is run with publishImg.py
The retrieving and visualizing code is run with finish.py

Publishing process (for a new image): 
1. imCut.py is called. It is passed the name of an image file (lets call it img).
2. imCut looks for the file inside the folder imToCut
3. The image is cut up according to the length and overlap variables specified at the top of imCut.py
4. The images pieces are stored inside toWeb/images/imageName/imageName_UupperCoordinate_LleftCoordinate.jpg
	where imageName is the name of the image originally passed to be cut without the file extension (we shall use imageName henceforth to refer to the image file name without the extension)
	upperCoordinate is the y-coordinate of the top left corner of this sub-image with 0,0 being the top left of the large image
	leftCoordinate is the corresponding x-coordinate.

5. The toWeb folder is published to heroku via bash commands

6. pubfolderhits.py is called
7. It iterates through each image inside a folder specified as a parameter. 
	This folder is the name of the original image file without the extension
	It creates a hit for each image. The hit outline contains information about cost, how many people should do the same hit, etc
	The "question" form is xml text that contains a link to the herokuapp site
		The image is specified by changing the url parameters in the link.
		The folder and image name must be specified in the URL parameters.
	For every hit that it creates, pubfolderhits.py stores the path to the image and its corresponding hitId in a 'hitfile'
	The file is saved as imageName + timestamp.txt inside the folder hitfiles

8. The Turk users work (on index.html)
	Annotations made by turkers are stored as a javascript object with the following fields:
		poly: a 3d array where poly[0] contains all the x-coordinate arrays for each polygon and poly[1] contains all the y.
		poly[0][0] and poly[1][0] together form the coordinates for a single polygon
		lines: a 3d array with same principal as poly
		points: 2d array where points[0] stores all x-coordinates of poitns and points[1] stores all y

9. retrieveFolder.py is called. It must be passed the name of a hitFile, stored inside the folder hitFiles
	It obtains every hitid in that file and gets the json output for each of those hits.
	It writes each json it obtained as one line of text into a file.
	It saves that file inside the folder storeJSON as "JSONS"+ hitFile name (let's call it retJSON)

10. jsonReader is called with a specified retJSON
	a. Just as each small image's annotations can be treated as an object with parameters: filename, polys, lines, points
	each big one can too. jsonReader creates a object with those paramters for each large image present in the retJSON file
	b. This means that developers can publish 100 5k x 5k images at the same time without worrying about having to associate a small image with a larger one
	c. jsonReader reads through each line and
		reads the hit's image file name and determines the offset by which to adjust the polygons, lines, and points (and adjusts them)
		stores the adjusted polygons in the polygon field of the larger object, lines in lines, etc...
	d. jsonReader writes each of the new large-image jsons as one line into a text file
	e. jsonReader saves the file as imageName.txt in wholejsons
	f. jsonReader generates an image depicting the annotations for the original large image. 
		Using the drawImage library from PIL, python draws over the original image using the annotationsObject for the large image and saves it as imageName+'REALANN.png' inside the imToCut folder.





