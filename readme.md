# The MTurk Annotation Tool

### What is it?
The MTurk Annotation tool is a customizable open-source platform that allows you to collect crowdsourced image annotations from users (Turkers) on Amazon Mechanical Turk (MTurk). The program deploys all the images and tools and you need to annotate to a Google Firebase app and interfaces with MTurk through their "External Question" feature. Once Turkers finish annotating your images, you have the ability to approve or reject their work, paying them only for quality work.

### What Can You Do With It?:
- Annotate Objects With Any of the Below Tools:
 	- Polygon
 	- Line 
    - Point
    - More If You Code Them (instructions coming soon)
- Provide Instructions to Turkers For Each Object to be Annotated
- Annotate for as many objects as you like in a single image
- Specify how many Turkers annotate the same image
- Specify how many images a single Turkers sees
- Annotate All Images Simultaneously
- Aspects of HITs including:
  - Reward for Each HIT
  - Location of Turkers
  - Custom Qualifications
  - Anything that can be controlled with Amazon Boto API

### Installation:
1. Clone this repository and install all dependencies with pip

2. Get the Site deployed on Firebase
	1. Make a Goolge Account if you do not have one (gmail will do)
	2. Install Firebase CLI (See [Link](https://firebase.google.com/docs/cli/)). Complete at least through ```firebase login```
	3. Login to Firebase [Console](https://console.firebase.google.com/)
	4. Create a Firebase Project and remember what you name it
	5. Open terminal and move into the MTurkAnnotationTool/toWeb directory
	6. Enter the following commands:
		```bash
		firebase init 
		```
		Select 'Hosting' when asked which Firebase CLI feature you would like to setup
		```bash
		firebase use --add [ProjectName]
		```
		where [ProjectName] is the name of the project you created in step iv
	7. Open config.ini and put the firebase subdomain name in the file under ```[Set Up]``` (Example Below)
		```
		[SetUp]
		firebaseSubdomain = amtannotate
		```
3. Set Up your MTurk Requester Account following these [instructions](http://docs.aws.amazon.com/AWSMechTurk/latest/AWSMechanicalTurkGettingStartedGuide/SetUp.html#accountlinking). When making an IAM user save your AWS Access and Secret Access keys somewhere safe

4. Place your AWS Access and Secret Access Keys inside the config.ini file replacing the lines:
	```
	[Username]
	awskey = Your AWS Key Here
	awssakey = Your AWS Secret Access Key
	```


### Dependencies (Tested With in Parenthesis):
- Python 3.x (3.6)
- pillow (Python Imaging Library/PIL) (4.1.1)
- boto3 (1.4.4) 
- matplotlib (2.0.2)
- numpy (1.12.1)
- Firebase Command Line Tools (from https://firebase.google.com/docs/cli/)

Code Flow:  

- The publishing code is run with publishImg.py
- The retrieving and visualizing code is run with finish.py

Publishing process (for a new image):   
1. imCut.py is called. It is passed the name of an image file (lets call it img).
2. imCut looks for the file inside the folder imToCut
3. The image is cut up according to the length and overlap variables specified at the top of imCut.py
4. The images pieces are stored inside toWeb/images/imageName/imageName_UupperCoordinate_LleftCoordinate.jpg
	where imageName is the name of the image originally passed to be cut without the file extension (we shall use imageName henceforth to refer to the image file name without the extension). upperCoordinate is the y-coordinate of the top left corner of this sub-image with 0,0 being the top left of the large image
	leftCoordinate is the corresponding x-coordinate.

5. The toWeb folder is published to heroku via bash commands

6. pubfolderhits.py is called
7. It iterates through each image inside a folder specified as a parameter. 
	- This folder is the name of the original image file without the extension
	- It creates a hit for each image. The hit outline contains information about cost, how many people should do the same hit, etc
	- The "question" form is xml text that contains a link to the herokuapp site
		- The image is specified by changing the url parameters in the link.
		- The folder and image name must be specified in the URL parameters.
	- For every hit that it creates, pubfolderhits.py stores the path to the image and its corresponding hitId in a 'hitfile'
	- The file is saved as imageName + timestamp.txt inside the folder hitfiles

8. The Turk users work (on index.html)
- Annotations made by turkers are stored as a javascript object with the following fields:
- poly: a 3d array where poly[0] contains all the x-coordinate arrays for each polygon and poly[1] contains all the y.
		poly[0][0] and poly[1][0] together form the coordinates for a single polygon
- lines: a 3d array with same principal as poly
- points: 2d array where points[0] stores all x-coordinates of poitns and points[1] stores all y

9. retrieveFolder.py is called. It must be passed the name of a hitFile, stored inside the folder hitFiles
	- It obtains every hitid in that file and gets the json output for each of those hits.
	- It writes each json it obtained as one line of text into a file.
	- It saves that file inside the folder storeJSON as "JSONS"+ hitFile name (let's call it retJSON)

10. jsonReader is called with a specified retJSON
	- Just as each small image's annotations can be treated as an object with parameters: filename, polys, lines, points
	each big one can too. jsonReader creates a object with those paramters for each large image present in the retJSON file
	- This means that developers can publish 100 5k x 5k images at the same time without worrying about having to associate a small image with a larger one
	- jsonReader reads through each line and
		reads the hit's image file name and determines the offset by which to adjust the polygons, lines, and points (and adjusts them)
		stores the adjusted polygons in the polygon field of the larger object, lines in lines, etc...
	- jsonReader writes each of the new large-image jsons as one line into a text file
	- jsonReader saves the file as imageName.txt in wholejsons
	- jsonReader generates an image depicting the annotations for the original large image. 
	- Using the drawImage library from PIL, python draws over the original image using the annotationsObject for the large image and saves it as imageName+'REALANN.png' inside the imToCut folder.


### Thanks To
For Developemnt Assitance and Mentorship:
- Dr. Kyle Bradbury
- Ben Brigman
- Boning Li
- Gouttham Chandrasekar
- Shamikh Hossain

For Code:
- Dr. Subhransu Maji - Used his [Starter Code](http://people.cs.umass.edu/~smaji/projects/mturk/index.html) for Annotating Polygons 




