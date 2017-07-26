# The MTurk Annotation Tool

### What is it?
The MTurk Annotation tool is a customizable open-source platform that allows you to collect crowdsourced image annotations from users (Turkers) on Amazon Mechanical Turk (MTurk). The program deploys all the images and tools and you need to annotate to a Google Firebase app and interfaces with MTurk through their "External Question" feature. Once Turkers finish annotating your images, you have the ability to approve or reject their work, paying them only for quality work.

### What Can You Do With It?:
- Annotate as many images as you like simultaneously
- Annotate objects insideimages with any of the below tools:
 	- Polygon
 	- Line 
    - Point
    - More If You Code Them (instructions coming soon)
- Annotate for as many objects as you like in a single image
- Provide instructions to Turkers for each object to be annotated
- Specify how many Turkers annotate the same image
- Specify how many images a single Turker sees
- Aspects of HITs including:
  - Reward for Each HIT
  - Location of Turkers
  - Custom Qualifications
  - Anything that can be controlled with Amazon Boto API
- Approve or Reject Turker's Work 

### How Do I Use It?
1. Follow the installation procedures outlined below
2. There are two ways you can use the program as given with ASCRIPT_begin.py
	1. You can annotate a collection of independent and unconnected images
	2. You can annotate a very large image that can be cut into custom size squares before being passed on to Turkers
		- This method was developed to help annotate satellite images covering large swathes of territory for specific features
Open ASCRIPT_begin.py and read the variable information at the head of the file for more information


### Dependencies (Tested With in Parenthesis):
- Python 3.x (3.6)
- pillow (Python Imaging Library/PIL) (4.1.1)
- boto3 (1.4.4) 
- matplotlib (2.0.2)
- numpy (1.12.1)
- Firebase Command Line Tools (from https://firebase.google.com/docs/cli/)

### Installation:
1. Clone this repository and install all dependencies with pip

2. Get the Site deployed on Firebase
	1. Make a Goolge Account if you do not have one (gmail will do)
	2. Install Firebase CLI (See [Link](https://firebase.google.com/docs/cli/)). Complete at least through ```firebase login```
	3. Login to Firebase [Console](https://console.firebase.google.com/)
	4. Create a Firebase Project
	5. Open terminal and move into the MTurkAnnotationTool/toWeb directory
	6. Enter the following commands:
		```bash
		firebase init 
		```
		Select 'Hosting' when asked which Firebase CLI feature you would like to setup, and select the project name from step 4 as your default project
		```bash
		firebase use --add [ProjectId]
		```
		where [ProjectId] is the name of the project you created in step iv
	7. Open config.ini and put the firebase subdomain name in the file under ```[Set Up]``` (Example Below)
		```
		[SetUp]
		firebaseSubdomain = amtannotate
		```
3. Set Up your MTurk Requester Account following these [instructions](http://docs.aws.amazon.com/AWSMechTurk/latest/AWSMechanicalTurkGettingStartedGuide/SetUp.html#setup-aws-account). When making an IAM user, save your AWS Access and Secret Access keys somewhere safe

4. Place your preferred username, AWS Access, and AWS Secret Access Keys inside the config.ini file replacing the lines:
	```
	[Username]
	awskey = Your AWS Key Here
	awssakey = Your AWS Secret Access Key
	```
5. Test If Installation Was Sucessful By Running ASCRIPT_begin.py, visiting one of the links printed into terminal, completing a HIT, and finally running ASCRIPT_finish.py

### What does this repo ship with?
The program is configured to run immediately with example Object/Annotation Type Pairs, Sample Images, and Helpfiles for the following:
- Car: Point
- Building: Polygon
- Road: Line
- Powerplant: Polygon
- Lamp Post: Point
- Tree: Polygon
Feel free to use the existing helpfiles as templates when making your own or make your own from scratch!

***

### How Does It Work?

##### Publishing Hits
1. Place images you would like to annotate in a folder inside ```toWeb/images/``` 
2. Firebase deploys your site
2. ```publish``` a function inside ```pubfolderhits.py``` is called and publishes a HIT to MTurk using your IAM user's access key. 
	- ```pubfolderhits.py``` contains all the functions relevant to creating hits. If you want to change HIT parameters like:
		- Compensation for HIT
		- 

### Adding Functionality

#### Adding Ant Object to Annotate
For every object (let's call it _obj_) you would like to annotate, you must do the following:
1. Provide a sample called obj.png inside toWeb/public/images/sample
2. Provide a help file written in HTML inside toWeb/public/helper
3. Add an entry into fileTypes indicating the tool used to annotate the object in toWeb/public/js/neededJSONS.json
	- If obj were to be annotated with a line,
		```
		fileTypes = '[{"road":"line","powerplant":"polygon"}]' 
		```
	- would become
		```
		fileTypes = '[{"road":"line","powerplant":"polygon","obj":"line"}]'
		```
	- The program ships with support for "polygon", "line", and "point" annotation types


### Thanks To
Developemnt Team:
- Dr. Kyle Bradbury
- Ben Brigman
- Boning Li
- Gouttham Chandrasekar
- Shamikh Hossain
- Trishul Nagenalli

Borrowed Code:
- Dr. Subhransu Maji - Used some of his [Starter Code](http://people.cs.umass.edu/~smaji/projects/mturk/index.html) for Annotating Polygons 




