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


### Thanks To
For Developemnt Assitance and Mentorship:
- Dr. Kyle Bradbury
- Ben Brigman
- Boning Li
- Gouttham Chandrasekar
- Shamikh Hossain

For Code:
- Dr. Subhransu Maji - Used his [Starter Code](http://people.cs.umass.edu/~smaji/projects/mturk/index.html) for Annotating Polygons 




