import boto3
import json
import xml.etree.ElementTree as ET
import configparser
# Before connecting to MTurk, set up your AWS account and IAM settings as described here:
# https://blog.mturk.com/how-to-use-iam-to-control-api-access-to-your-mturk-account-76fe2c2e66e2
#
# Follow AWS best practices for setting up credentials here:
# http://boto3.readthedocs.io/en/latest/guide/configuration.html 

# Use the Amazon Mechanical Turk Sandbox to publish test Human Intelligence Tasks (HITs) without paying any money.
# Sign up for a Sandbox account at https://requestersandbox.mturk.com/ with the same credentials as your main MTurk account.


def processResponse(response):
	allfilejsons = [] # Stores the answer data (json text) and for each user who completed a hit
	#print(response.keys())
	allResponses = response["Assignments"]
	# Extracts some XML data inside the answer field
	# Uses an XML library (imported as ET) to treat XML tags as a tree and extract the JSON which is always at position 0,1 inside the XML
	missed = 0
	for assign in allResponses:
		answer = assign["Answer"]
		root = ET.fromstring(answer)
		anslines = root[0][1].text

		for line in anslines.split('\r'):
			if line.lstrip().rstrip() == '': continue
			line = line.rstrip().lstrip()
			
			storingAssignment = {}
			storingAssignment['assignmentID'] = assign['AssignmentId']
			try:
				ans = json.loads(line)
				storingAssignment.update(ans);
				writeText = json.dumps(storingAssignment);
				allfilejsons.append(writeText);
			except:
				print("MISSED: ")
				print(line)
				print()
				#print(line)
				# print('IN EXCEPT ==========')
				# print("LINE: " + str(type('LINE')))
				# line = line[:-1]
				# print('EXCEPT: ' + line)
				# print('made it past line')
				# ans = json.loads(line)
	return allfilejsons


def getResponse(hid):
	response = client.list_assignments_for_hit( # Specifies which hits to get. Currently takes everything
		HITId=hid,
		AssignmentStatuses=[
			'Submitted' or 'Approved' or 'Rejected',
		]
	)
	return response # A dict 

def processAllHits(caseFolder):
	afj = []
	hitfile = open('folders/' + caseFolder + '/hitList.txt','r') # Iterate through every hit specified in hit file, get he apprpriate response and process it
	for line in hitfile:
		line = line[:-1]
		hitid = line.split(', ')[1]
		resp = getResponse(hitid)
		afj = afj + processResponse(resp)
	storeHits(caseFolder, afj)



def storeHits(caseFolder, allfilejsons):
	jsonStore = open('folders/'+caseFolder+'/indJSONS.txt', 'w')
	for js in allfilejsons:
		jsonStore.write(js+'\n')


def retrieve(userName, caseFolder, pubType):
	config = configparser.ConfigParser()
	config.read('config.ini')
	region_name = 'us-east-1'
	#endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

	# Uncomment this line to use in production. 
	# Use opposed to above endpoint url
	# If you published in production mode, you must have this uncommented so that you retrieve data from Amazon's us-east-1 server and not the sandbox
	# If you published in developer mode, the opposite is true ^
	# endpoint_url = 'https://mturk-requester.us-east-1.amazonaws.com'
	if pubType =='developer': 
		eurl = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
	elif pubType == 'production': 
		eurl = 'https://mturk-requester.us-east-1.amazonaws.com'
	else:
		raise NameError('Invalid pubType: production or developer only')
	global client 
	client = boto3.client('mturk',
		endpoint_url = eurl,
		region_name = region_name,
		aws_access_key_id = config[userName]['awskey'], 			## Put Amazon Web Services Access Keys in config.ini File
	    aws_secret_access_key = config[userName]['awssakey'], 
	)
	processAllHits(caseFolder)
