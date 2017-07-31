import boto3
import json
import xml.etree.ElementTree as ET
import configparser
import datetime
# Before connecting to MTurk, set up your AWS account and IAM settings as described here:
# https://blog.mturk.com/how-to-use-iam-to-control-api-access-to-your-mturk-account-76fe2c2e66e2
#
# Follow AWS best practices for setting up credentials here:
# http://boto3.readthedocs.io/en/latest/guide/configuration.html 

# Use the Amazon Mechanical Turk Sandbox to publish test Human Intelligence Tasks (HITs) without paying any money.
# Sign up for a Sandbox account at https://requestersandbox.mturk.com/ with the same credentials as your main MTurk account.
topLevelDir = 'HITBatches'

def processResponse(response):
	allfilejsons = [] # Stores the answer data (json text) and for each user who completed a hit
	allResponses = response["Assignments"]
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
	return allfilejsons


def getResponse(hid):
	response = client.list_assignments_for_hit( # Specifies which hits to get. Currently takes everything
		HITId=hid,
		AssignmentStatuses=[
			'Submitted', 'Approved', 'Rejected'
		]
	)
	return response # A dict 

def getAcceptedResponse(hid):
	response = client.list_assignments_for_hit( # Specifies which hits to get
		HITId=hid,
		AssignmentStatuses=[
			'Approved'
		]
	)
	return response # A dict 

def processAllHits(hitBatch):
	hitsProcessed = 0
	assignmentsViewed = 0
	imagesProcessed = 0
	pendingReview = 0
	totalAssignmentsAvailable = 0
	assignmentsComplete = 0
	intendedMax = 0
	afj = []
	print()
	print('Downloading HIT Data')
	hitfile = open(topLevelDir + '/' + hitBatch + '/hitList.txt','r') # Iterate through every hit specified in hit file, get he apprpriate response and process it
	for line in hitfile:
		line = line[:-1]
		hitid = line.split(', ')[1]
		resp = getResponse(hitid)
		processed = processResponse(resp)
		afj = afj + processed
		hitsProcessed += 1
		assignmentsViewed += resp['NumResults']
		imagesProcessed += len(processed)
		
		hitInfo = client.get_hit(HITId = hitid)['HIT']
		intendedMax += hitInfo['MaxAssignments']
		pendingReview += hitInfo['NumberOfAssignmentsPending']
		totalAssignmentsAvailable += hitInfo['NumberOfAssignmentsAvailable']
		assignmentsComplete += hitInfo['NumberOfAssignmentsCompleted']
		
		print ('Hits Viewed: ' + str(hitsProcessed) + ', ' + 'Assignments Submitted: ' + str(assignmentsViewed) + ', ' + 'Images Processed: ' + str(imagesProcessed) , end ="\r")
	print ('Hits Viewed: ' + str(hitsProcessed) + ', ' + 'Assignments Submitted: ' + str(assignmentsViewed) + ', ' + 'Images Processed: ' + str(imagesProcessed))
	storeHits(hitBatch, afj)
	print ('Intended Total Number of Assignments:\t' + str(intendedMax))
	print ('Assignments Submitted:\t\t\t' + str(assignmentsViewed))
	print ('Assignments Missing: \t\t\t' + str(intendedMax-assignmentsViewed))
	print ('Assignments We Haven\'t Reviewed:\t' + str(assignmentsViewed - assignmentsComplete))
	print ('Assignments Presently Available:\t' + str(totalAssignmentsAvailable))
	print ('Assignments Presently Reviewed:\t\t' + str(assignmentsComplete))
	print ('Completed Download. Created all_submitted.txt')
	print()



def storeHits(hitBatch, allfilejsons):
	jsonStore = open(topLevelDir + '/'+hitBatch+'/all_submitted.txt', 'w')
	for js in allfilejsons:
		jsonStore.write(js+'\n')

def getAndStoreAcceptedHits(hitBatch):
	print('Downloading Accepted Hit Data')
	aj = []
	hitfile = open(topLevelDir + '/' + hitBatch + '/hitList.txt','r') # Iterate through every hit specified in hit file, get he apprpriate response and process it
	hitsProcessed = 0
	assignmentsViewed = 0
	imagesProcessed = 0
	for line in hitfile:
		line = line[:-1]
		hitid = line.split(', ')[1]
		resp = getAcceptedResponse(hitid)
		processed = processResponse(resp)
		aj = aj + processed
		hitsProcessed += 1
		assignmentsViewed += resp['NumResults']
		imagesProcessed += len(processed)
		print ('Hits Viewed: ' + str(hitsProcessed) + ', ' + 'Assignments Received: ' + str(assignmentsViewed) + ', ' + 'Accepted Images: ' + str(imagesProcessed) , end ="\r")
	print ('Hits Viewed: ' + str(hitsProcessed) + ', ' + 'Assignments Received: ' + str(assignmentsViewed) + ', ' + 'Accepted Images: ' + str(imagesProcessed))
	jsonStore = open(topLevelDir + '/'+hitBatch+'/accepted.txt', 'w')
	for js in aj:
		jsonStore.write(js+'\n')
	print ('Created accepted.txt file from known accepted hits')
	print()

def retrieve(userName, hitBatch, pubType):
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
	print()
	print('Batch Metadata: ')
	print(getMetaData(hitBatch))
	processAllHits(hitBatch)
	getAndStoreAcceptedHits(hitBatch)

def getMetaData(hitBatch):
	hitid = open(topLevelDir + '/' + hitBatch + '/hitList.txt','r').readline().split(', ')[1][:-1]
	response = client.get_hit(HITId=hitid)['HIT']
		 
	metaDataString = ('Batch ID: \t\t' + hitBatch 
		+ '\nCreation Time:   \t' + response['CreationTime'].strftime('%m/%d/%Y at %I:%M:%S %p %Z') 
		+ '\nExpiration Time: \t' + response['Expiration'].strftime('%m/%d/%Y at %I:%M:%S %p %Z') 
		+ '\nEarliest Auto-Approval: ' + (response['CreationTime'] + datetime.timedelta(0,response['AutoApprovalDelayInSeconds'])).strftime('%m/%d/%Y at %I:%M:%S %p %Z') 
		+ '\nMax Assignments: \t' + str(response['MaxAssignments']) 
		+ '\nReward: \t\t' + str(response['Reward']) 
		)
	return metaDataString

