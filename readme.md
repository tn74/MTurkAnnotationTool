# The MTurk Annotation Tool

### What is it?
The MTurk Annotation tool is a customizable open-source platform that allows you to collect crowdsourced image annotations from users (Turkers) on Amazon Mechanical Turk (MTurk). The program deploys all the images and tools and you need to annotate to a Google Firebase app and interfaces with MTurk through their "External Question" feature. Once Turkers finish annotating your images, you have the ability to approve or reject their work, paying them only for quality work. 

 ** Note: Readme is still under construction **

### What Can You Do With It?:
- Annotate as many images as you like simultaneously
- Annotate objects inside images with any of the below tools:
 	- Polygon
 	- Line 
    - Point
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
1. Install the software according to the instructions later in this ReadMe. By the end, you must have a Firebase account with google, and Amazon Web Services API keys for users that have access to the Turk API.

2. Open up config.ini (which is created by the installation script) and ensure the following
	- ```firebaseSubdomain``` is set equal to the project-id of the firebase project you are using
	- ```[User Name]``` is set to something you would remember (for a person named John, this might be written as ```[John]```)
	- ```awskey``` is set to your IAM user's access key
	- ```awssakey``` is set to your IAM user's secret access key

3. Open ASCRIPT_begin.py. This is a file that will allow you to publish HITS for Turkers to work on. Set the variables at the beginning and run the script to publish the HITs. Running the script will create a folder inside HITBatches that contain all the data relavant to this batch of HITs you have published.

4. Let your turkers work! 

5. Open ASCRIPT_finish.py and set the variables at the start of that script. Run it to download all the data that has been submitted to you.

6. Run ASCRIPT_hit_checker.py from terminal to approve or reject work that Turkers have submitted to you. 

7. Rerun ASCRIPT_finish.py to process the accepted data and produce confidence maps for each image you published. You will get a raw and normalized confidence map for each object you chose to annotate for. The raw map contains, at each pixel, the number of annotators who labeled that pixel as part of an object. The 
	- You can view these confidence maps in HITBatches/[Your Hit Batch Name]/data/[image name] where [Your Hit Batch Name] is the name of the folder created when you published this batch of hits and [image name] is the name of the specific image you would like a confidence map for.
	- You can also see the raw annotation data (like coordinates for your polygons, lines, points, etc) for each image you have received in JSON format inside one of the .txt files. See the Output Documents Section for more information about each of the txt files and the outputs from this program.


### Dependencies (Tested Version in Parenthesis):
- Python 3.x (3.6)
- pillow (Python Imaging Library/PIL) (4.1.1)
- boto3 (1.4.4) 
- matplotlib (2.0.2)
- numpy (1.12.1)
- Firebase Command Line Tools (from https://firebase.google.com/docs/cli/)

### Installation:
We recommend conducting this procedure inside a Python Virtual Environment. Please create and activate one with the python package virtualenv or conda if you are using Anaconda.
1. Clone this repository and install all dependencies. For a quick way to do this, try the following: 
````
$ pip install -r requirements.txt
````

2. Get the Site deployed on Firebase
	1. Make a Goolge Account if you do not have one
	2. Install Firebase CLI (See [Link](https://firebase.google.com/docs/cli/)). Complete at least through ```firebase login```
	3. Login to Firebase [Console](https://console.firebase.google.com/)
	4. Create a Firebase Project
	5. Open terminal and move into the MTurkAnnotationTool/toWeb directory
	6. Run ```firebase list``` in terminal and see the project-id for the project that you just created
	7. Open the script ASCRIPT_INSTALL.py
	8. Set the firebaseProjectID equal to your project-id 
	9. Run the ASCRIPT_INSTALL.py

3. Set Up your MTurk Requester Account following these [instructions](http://docs.aws.amazon.com/AWSMechTurk/latest/AWSMechanicalTurkGettingStartedGuide/SetUp.html#setup-aws-account). Make sure you complete all steps through Step 5 (setting up the developer sandbox). When making an IAM user, save your AWS Access and Secret Access keys somewhere safe

4. Place your preferred username (doesn't matter what it is so long as you are consistent in your code), AWS Access, and AWS Secret Access Keys inside the config.ini For example, if you wanted to create access for a user named 'Student' with AWS Key 'ABCD' and AWS Secret Access Key '1234'
	```
	[User name]
	awskey = Your AWS Key Here
	awssakey = Your AWS Secret Access Key
	```
	would become
	```
	[Student]
	awskey = ABCD
	awssakey = 1234

	```
5. Test if installation was successful by running the below scripts in order
	1. EXTENSION_PreprocessLargeImage.py
	2. ASCRIPT_begin.py
	
	Go online to a link posted by the begin script when it is publishing hits. It will take you to the developer sandbox where you can see exactly what your HIT would look like to an actual user without having to pay them for it. Do a couple hits so you can test with data.

	3. Open ASCRIPT_finish.py and change the variable hitBatch to the name of the folder inside hitBatches
	4. Run ASCRIPT_finish.py and see some statistics about your HIT.

	If no crashes occur, you have finished! Explore the images stored inside the data folder

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

#### Some Terms:
	- **Hit Batch**: A group of HITs that go together because they were all created together during a single run of ASCRIPT_begin.py. All the HITs in one hit batch will be for images inside the same subfolder of toWeb/images and will be published at roughly the same time

##### Publishing Hits
1. Place images you would like to annotate in a folder inside ```toWeb/images/``` 
2. Firebase deploys everything inside toWeb/public to your site
3. ```publish()```, a function inside ```pubfolderhits.py``` is called and publishes HITs to MTurk using your IAM user's API keys. 
	- ```pubfolderhits.py``` contains all the functions related to creating hits. If you want to change HIT parameters go to publishHit inside pubfolderhits.py and edit properties (like the ones below) near line 50
		- Compensation for HIT (Currently $0.02)
		- Location Restrictions for a HIT (Currently None)
		- Time to Complete a HIT (Currently 10 minutes)
		- Time HIT will remain online (Currently 2 weeks for production HITs)
4. When ```publish()``` creates a hit, it tells Amazon to display a webpage inside a Turker's workspace. The webpage is hosted on your firebaseapp site. The URL of that webpage specifies the image to be annotated and the objects to be annotated for. More on that in the next section "Turkers Working Online"
3. A folder is created inside HITBatches named with your batch's id. The batch id consists of the name of the image folder published + a timestamp. This folder will contain all the information that is relevant to this **hit batch**) or 
4. A file ```hitList.txt``` is created inside the hit batch folder. Each line is one HIT. A line contains the HIT's ID and the information required to reconstruct the path of the image from ```toWeb/images```

##### Turkers Working Online
1. Turkers work on the web based image annotation platform that is dynamically created with javascript. The platform is dynamically generated according to a url that is structured like below:
	- ```https://[firebaseProjectID].firebaseapp.com/index.html?category-image=[image subfolder]+[image1]+[image2]+[image3]&annotation=[object1]+[object2]```
		- ```[image subfolder]``` is the name of the folder inside ```toWeb/images``` containing the images to be annotated
		- ```[image1]```, ```[image2]```... are the names of the images (including file extension) inside that folder that should all be annotated together in one HIT
		- ```[object1]```,```[object2]```... are the names of objects to be annotated for each image in this HIT.
	- If you have images on your site right now, you can test this out by specifying an image and annotation object and going to that url. It will not affect any HITs you have active
2. Once annotations for one image are complete, a button to the right of the image will take the user to the next image. On the last image, that button will change to say "Submit Results"
3. To understand how the webpage portion works, it may be best to open the html and javascript portions of the page itself. They are inside toWeb/public. The base html is in ```index.html```. The javascript is inside the js folder. The dynamic display of the site is taken care of in ```displays.js```. The annotation javascript is inside ```annotationCode.js```

##### Downloading Data and Approving/Rejecting HITs
1. Run ASCRIPT_finish.py after setting the appropriate variables at the start of the script
2. The annotations for each image submitted to you will be stored in JSON Format (1 line per image) inside all_submitted.txt, a text file inside your specific hit batch folder. Learn more about the JSON format [here](https://github.com/tn74/MTurkAnnotationTool/wiki/all_submitted.txt-&-accepted.txt-JSON-Data-Structure)
3. The JSON for the condensed images will also be stored in condensed_all_submitted.txt
	- A condensed image combines the annotations of everyone who annotated the same image into one line of JSON. For example, if three people annotated powerplants on top of an image independently, a condensed image would have all three polygons in the same line of JSON
	- All condensed JSON is stored in condensed_all_submitted.txt
	- A visual represntation of each condensed image, where each annotated feature is drawn, is stored in allSubmittedCondensedImages.

3. Run ```ASCRIPT_hit_checker.py``` script with the proper variables and accept or reject annotations. The hitcheker:
	- Reads through each line of all_submitted.txt
	- Generates an image of the annotations given the JSON data
	- Displays the image in a window and asks you to accept or reject the annotation
	- Accepts all assignments containing an image that you accepted and rejects those that contained no image that you accepted once you close out the hit_checker GUI.
	 --folder**Note:** The only way to reject an assignment and not provide that Turker compensation is if you reject every image that they annotated. If you offered them 10 images to annotate and you rejected 9 of them, you will still pay them the full compensation for the 1 image you accepted.
 	- Writes the line of JSON for each accepted annotation into accepted.txt

4. Rerun ```ASCRIPT_finish.py``` 
	- Will download new unreviewed data for hit checker to process
	- Creates condensed images using only accepted data. 
		- The JSONS are stored in condensed_accepted.txt 
		- The visual representations are stored in acceptedCondensedImages
	- Will begin populating data folder with confidence maps for each image and annotated object using only accepted data
		- Inside data, a folder will be created for each iamge annotated and it will be named the same as the image without the file extension.
		- Inside the image's folder will be a raw and normalized confidence map for each object annotated
			- The raw map contains, at every pixel, the number of people who thought this was part of a feature
			- The normalized map contains, at every point, the relative confidence of a point being part of a feature with the highest relative confidence having a value of 255, visualized as white, and the lowest having 0, visualized as black. Note that this is a relative confidence. An image that has a maximum of two people annotating any given point as a feature will show 2 as 255. Another image that has a max of 20 people annotating any given point will show 20 as 255. The normalized map is meant as an easy visualization. For data processing purposes, we recommend using the raw map.


### Additional Functionality
#### Adding A New Type Of Object to Annotate
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
	- The program supports "polygon", "line", and "point" annotation types
4. Add the name of the object to annotations list when running ASCRIPT_begin.py

#### Processing Large Satellite Images
	- Info Coming Soon


#### Verifying annotations: Using the Hitchecker (ASCRIPT_hit_checker.py)
You will often want to ensure the validity and accuracy of your annotation dataset by filtering out the occasional human errors, accidental or systematic, made by the Turk users who complete the HITs. To do this, our platform includes a script that launches a basic GUI interface that generates labeled images with the user-submitted annotations and allows you to either Accept or Reject the annotation data for use and to of course pay your Turkers through Amazon for their successful completion of the HIT. The GUI runs on Tkinter, which is part of the standard Python library and thus should run on your machine without specific pip installation, and uses the boto client to interface with the Turk platform- allowing you to pay Turkers immediately on clicking 'Accept' and provide feedback immediately upon rejection (which can be modified). 

- When you click the 'Accept' button, the user who completed the HIT/set of HITs will be compensated. 
- When you click reject, a message ('Sorry, your annotations look incomplete!') is sent to the Turk user who annotated incorrectly. This message can be modified by editing the 'RequesterFeedback' variable in usefulBotoFunctions.py. 
- Both accepted and rejected HITs are transcribed (in their JSON form) to accepted.txt and rejected.txt respectively. 

IMPORTANT: To run the Hitchecker from Terminal, you should provide an input parameter using '-f'/'--folder' to let the script know the location of the JSON file that contains the HITs that you want to evaluate. You should also provide a second input using '-c'/'--clientname' to indicate the name of the Amazon Mechanical Turk client that you want to connect to using the API. 
Example: Say we want to evaluate a recent set of 100 HITs completed by Turkers. The images that we uploaded to Turk for this set and a text file of the json responses are stored in indJSONS.txt in this folder. To run the Hitchecker on this set of HITs, we run the following from Terminal, which will read the indJSONS.txt file from the input folder, and also get the name of the Amazon Mechanical Turk client being used:  
````
$ python ASCRIPT_hit_checker.py --folder images --clientname kyle 
100
````
You should immediately see a printed number indicated the number of HITs inside the text file of jsons. The program will now work to generate and load all the annotated images given the data in this text file, so you will need to wait a few minutes. You will then see the GUI launch with annotated images. To adjust the size of the windows or the resizing of the images, change the lines in the GUI class in ASCRIPT_hit_checker.py under the comment that indicates these options (line 91). 

You can now Accept or Reject HITs, and the program will display "The hit was accepted!" or "The hit was rejected!" if the script is properly able to make requests to the Turk API (boto3). You will ideally want to judge correctness of the annotation on the basis of the object that HIT assigned them to annotate- this will be displayed in a static button above the Accept and Reject button. It will also attempt to delete generated images from memory to be more space efficient, however, this might fail depending on file structure. The GUI will still run and accept/reject HITs just fine. 

After you close the GUI, the terminal will summarize the accepted and rejected work, and the accepted.txt and rejected.txt files will be generated inside the folder. You can also close the GUI and return later- annotations that you have already evaluated will not be revisited when you relaunch the program. As long as the actual HIT has already been dealt with through Amazon (i.e workers have been paid), your work will be saved. 


### Thanks To
Development Team:
- Dr. Kyle Bradbury
- Ben Brigman
- Boning Li
- Gouttham Chandrasekar
- Shamikh Hossain
- Trishul Nagenalli

Borrowed Code:
- Dr. Subhransu Maji - Used some of his [Starter Code](http://people.cs.umass.edu/~smaji/projects/mturk/index.html) for Annotating Polygons 




